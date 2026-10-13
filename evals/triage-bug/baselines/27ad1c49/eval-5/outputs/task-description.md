## Repository
acme-backend

## Target Branch
main

## Description
Fix dark mode preference persistence so that the user's theme choice survives
browser session restarts. Currently the preference is stored only in ephemeral
state and is lost when the browser is closed. The fix must add a durable write
path (persist on toggle) and a read path (restore on load). Fixes ACME-511.

## Files to Modify
- `src/frontend/components/Settings/AppearancePanel.tsx` -- add persistence call when dark mode toggle changes
- `src/frontend/hooks/useTheme.ts` -- add logic to read stored preference on initialization
- `src/frontend/app/ThemeProvider.tsx` -- initialize theme from stored preference before first render

## Implementation Notes
The dark mode toggle in the Settings > Appearance panel currently updates only
in-memory state. Two changes are needed:

1. **Write path (persist on toggle):** When the user toggles dark mode, persist
   the preference to `localStorage` under a well-known key (e.g.,
   `user-preference:theme`). If a backend user preferences API exists
   (e.g., `PUT /api/v1/user/preferences`), also call it to persist server-side.

2. **Read path (restore on load):** During application initialization (in the
   theme provider or hook), check `localStorage` for a stored theme preference
   before falling back to the default (light) theme. If a backend API is used,
   fetch the preference on load and reconcile with the localStorage value.

**Reproducer test guidance:**
- The Steps to Reproduce describe: open app, navigate to Settings > Appearance,
  toggle dark mode ON, close browser, reopen and navigate back.
- The Actual Result is: app loads in light mode, toggle reset to OFF.
- The Expected Result is: app loads in dark mode matching the saved preference.
- The reproducer test should simulate this flow: toggle dark mode ON, clear
  ephemeral state (component unmount / page teardown), reinitialize the app,
  and assert the theme is dark mode with the toggle ON.

No CONVENTIONS.md was found in the repository root.

No data migration is needed -- the bug is about preferences not being persisted
at all, so there are no stale records to correct.

## Acceptance Criteria
- [ ] A reproducer test demonstrates the bug: toggles dark mode ON, simulates a session restart (clears ephemeral state, reloads), and asserts the theme reverts to light mode (fails before fix, passes after fix by asserting dark mode persists)
- [ ] Dark mode preference is written to durable storage (localStorage and/or backend API) when the user toggles the setting
- [ ] On application load, the stored dark mode preference is read and applied before the default theme renders
- [ ] The dark mode toggle reflects the persisted state (ON) after a session restart
- [ ] No regression in existing tests

## Test Requirements
- [ ] Reproducer test: toggle dark mode ON, simulate session restart (clear ephemeral state, reinitialize app), assert theme is dark mode and toggle shows ON. This test must fail before the fix and pass after.
- [ ] Unit test for the persistence write path: verify that changing the toggle calls `localStorage.setItem` (or the backend API) with the correct value
- [ ] Unit test for the persistence read path: verify that on initialization, the theme hook/provider reads from `localStorage` (or backend API) and returns the stored preference
- [ ] Edge case test: verify that when no stored preference exists (first-time user), the application defaults to light mode

## Bug Context

- **Bug**: [ACME-511](https://mock-jira.example.com/browse/ACME-511)
- **Steps to Reproduce**: Open app, navigate to Settings > Appearance, toggle dark mode ON, close browser completely, reopen and navigate back to the app
- **Expected Result**: Application loads in dark mode matching the user's last preference
- **Actual Result**: Application loads in light mode; dark mode toggle is reset to OFF
- **Root Cause**: Dark mode preference is stored only in ephemeral state (component state or sessionStorage) and not written to durable storage. On browser close the ephemeral state is destroyed, causing the application to default to light mode on next load.
