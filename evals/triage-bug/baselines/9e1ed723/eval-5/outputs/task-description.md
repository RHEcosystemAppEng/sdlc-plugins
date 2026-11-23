# Step 5 – Generated Task (ACME-511 fix)

**Would be created via `jira.create_issue` (not sent — eval mode):**

- Project: ACME
- Issue type: Task
- Summary: Fix dark mode preference not persisting across browser sessions (ACME-511)
- Labels: `ai-generated-jira`
- Link (Step 5b): link type `Blocks` — inward = <created-task-key> (blocker), outward = ACME-511 (blocked)
- Digest (Step 5c): after creation, re-fetch the description, run `python3 scripts/sha256-digest.py /tmp/desc-<task-key>.txt`, and post `[sdlc-workflow] Description digest: <tagged-digest>` as a standalone comment (no footnote)

---

## Repository
acme-backend

> Note: acme-backend is the only repository in the Repository Registry. If the theme
> preference turns out to be stored client-side only, this task must be retargeted to the
> frontend repository, which should be added to the Registry first.

## Target Branch
main

## Description
Fixes ACME-511. After a user turns on dark mode in Settings > Appearance and then closes
and reopens the browser, the app loads in light mode and the toggle is reset to OFF. The
preference must persist across browser sessions: the app should load in the user's last
selected theme.

Root cause (provisional): the dark mode preference is not round-tripped through
persistent storage. Either it is kept only in memory or `sessionStorage`, or startup does
not read the stored value and initializes to a hardcoded light default.

## Files to Modify
The triage investigation could not identify concrete file paths. The provided repository
context had no theme or preference code. Before changing anything, locate and confirm:
- The Settings > Appearance dark mode toggle handler — so it writes the preference to durable storage
- The theme provider / app bootstrap initialization — so it reads the stored preference before first render
- (If server-side) The user-preferences save/load endpoint and model in acme-backend — so the theme field is saved and returned

## Implementation Notes
- Fixes ACME-511.
- **Find the code first.** Search for: `theme`, `darkMode`, `dark_mode`, `ThemeProvider`,
  `useTheme`, `preferences`, `UserPreferences`, `appearance`, and for storage usage:
  `localStorage`, `sessionStorage`, `document.cookie`, `prefers-color-scheme`, `data-theme`.
  In acme-backend, look for preferences/settings handlers and models.
- **Decide where the preference lives:**
  - Client-side: write the value to `localStorage` (not `sessionStorage`, not memory only)
    when the toggle changes. On startup, read it before the first render.
  - Server-side: make sure the toggle calls the preferences save endpoint, the backend
    stores the theme field, and the preferences response used on startup includes it. The
    frontend must apply it on load.
- **Default behavior:** fall back to light mode only when no stored preference exists. A
  stored preference must never be overwritten with the default during initialization.
- **Reproducer test guidance** (from Steps to Reproduce and Expected vs Actual Result):
  - Trigger: set dark mode ON through the toggle's code path, then simulate a browser
    restart (tear down app state, clear in-memory and session-scoped state, keep durable
    storage), then re-initialize the app.
  - Before fix (Actual Result): the theme resolves to light and the toggle reads OFF.
  - After fix (Expected Result): the theme resolves to dark and the toggle reads ON.
- **Test patterns:** the investigation found no existing theme or UI tests. Follow the
  test framework and layout of the repository where the fix lands (Rust `#[test]`/
  integration tests for acme-backend, or the frontend's existing component/unit test setup).
- **Conventions:** acme-backend has no CONVENTIONS.md at its root.
- **Data migration:** not required. The defect leaves the preference missing; it does not
  write wrong values to a database, so there are no stale records to correct. Revisit only
  if the code shows a wrong theme value is saved at write time.
- **Affects Version:** unknown. The reporter was on "whatever is deployed on staging". A
  gap comment was posted on ACME-511 asking for the version to be set manually.

## Acceptance Criteria
- [ ] A reproducer test enables dark mode, simulates a new browser session (clearing in-memory/session state but keeping durable storage), re-initializes the app, and asserts the theme is dark and the toggle is ON. It fails before the fix and passes after.
- [ ] Toggling dark mode in Settings > Appearance saves the preference to durable storage (`localStorage` or the backend user-preferences record).
- [ ] On startup, the stored theme preference is read and applied before the first render, with no flash or reset to light mode.
- [ ] With no stored preference, the app defaults to light mode (current default behavior is kept).
- [ ] Turning dark mode OFF is also saved: after a restart the app loads in light mode.
- [ ] No regression in existing tests.

## Test Requirements
- [ ] Reproducer test (first, required): set the theme to dark through the toggle path, simulate a browser restart by resetting all non-durable state, re-initialize, and assert `theme == dark` and toggle state == ON. Before the fix it should observe `light`/OFF (the Actual Result); after the fix it must assert `dark`/ON (the Expected Result).
- [ ] Test that with empty storage the app initializes to light mode.
- [ ] Test that dark -> light is saved and restored after a simulated restart.
- [ ] If server-side storage is involved: a backend test that saves a user's theme preference and confirms a later, separate fetch returns `dark`.

## Dependencies
- None. (Prerequisite: confirm the repository that owns the theme toggle; register it in
  the Repository Registry if it is not acme-backend.)

## Bug Context

- **Bug**: [ACME-511](https://mock-jira.example.com/browse/ACME-511)
- **Steps to Reproduce**: Open the app -> Settings > Appearance -> turn "Dark Mode" ON -> close the browser completely -> reopen it and go back to the app.
- **Expected Result**: The application should load in dark mode, matching the user's last preference.
- **Actual Result**: The application loads in light mode. The dark mode toggle is reset to OFF.
- **Root Cause**: Provisional, low confidence. The dark mode preference is not round-tripped through persistent storage: it is either kept only in memory/`sessionStorage` or not read back on startup, so the app falls back to the light default. The exact files were not identified during triage.
