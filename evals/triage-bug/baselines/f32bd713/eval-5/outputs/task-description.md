# Step 5 -- Generated Task Description: ACME-511

## Task Metadata

- **Summary:** Fix dark mode preference persistence across browser sessions (ACME-511)
- **Project:** ACME
- **Issue Type:** Task
- **Labels:** ai-generated-jira
- **Link:** Blocks ACME-511 (Bug-to-Task link type: Blocks)

## Task Description

```
## Repository
acme-backend

## Target Branch
main

## Description
Fix the dark mode toggle to persist the user's preference across browser sessions. Currently, toggling dark mode ON in Settings > Appearance only updates in-memory state. When the browser is closed and reopened, the preference is lost and the application defaults to light mode. The fix requires adding both a write path (persist preference on toggle) and a read path (restore preference on app load). Fixes ACME-511.

## Files to Modify
- `src/components/Settings/Appearance.tsx` — add localStorage write to the dark mode toggle handler to persist the preference
- `src/providers/ThemeProvider.tsx` — read stored preference from localStorage on initialization instead of defaulting to light mode

## Implementation Notes
The dark mode toggle handler currently dispatches a state update to the theme context but does not persist the value. Two changes are needed:

1. **Write path (toggle handler):** After updating in-memory state, call `localStorage.setItem("theme-preference", "dark")` (or `"light"` when toggling off). Use a consistent storage key.

2. **Read path (theme provider init):** On application load, the theme provider should check `localStorage.getItem("theme-preference")` before falling back to the default `"light"` value. If a stored preference exists, use it as the initial theme state.

The reproducer test should simulate the full cycle described in the Steps to Reproduce:
- **Trigger:** Toggle dark mode to ON via the Settings > Appearance panel
- **Incorrect behavior (before fix):** After simulating a browser reload (re-initializing the theme provider), the application loads in light mode with the toggle reset to OFF
- **Correct behavior (after fix):** After simulating a browser reload, the application loads in dark mode with the toggle set to ON, matching the user's last preference

No CONVENTIONS.md was found in the repository root.

## Acceptance Criteria
- [ ] Reproducer test: a test that toggles dark mode ON, simulates a browser session restart (re-initializes the theme provider), and asserts the application loads in dark mode -- this test must fail before the fix and pass after
- [ ] The dark mode preference is written to localStorage when the user toggles dark mode
- [ ] The theme provider reads the stored preference from localStorage on initialization and applies it
- [ ] Toggling dark mode OFF also persists the light mode preference correctly
- [ ] No regression in existing tests

## Test Requirements
- [ ] Reproducer test: toggle dark mode ON, verify localStorage is written with the preference, re-initialize the theme provider (simulating browser restart), assert the initial theme is dark mode -- assert the toggle state reflects the stored preference. Before the fix, the theme provider ignores localStorage and defaults to light mode (test fails). After the fix, the theme provider reads localStorage and initializes with dark mode (test passes).
- [ ] Test that toggling dark mode OFF persists the light mode preference and is correctly restored on reload
- [ ] Test that when no stored preference exists, the application defaults to light mode (backward compatibility)

## Bug Context

- **Bug**: [ACME-511](https://mock-jira.example.com/browse/ACME-511)
- **Steps to Reproduce**: Open the application, navigate to Settings > Appearance, toggle Dark Mode to ON, close the browser completely, reopen and navigate back to the application.
- **Expected Result**: The application should load in dark mode, matching the user's last preference.
- **Actual Result**: The application loads in light mode. The dark mode toggle is reset to OFF.
- **Root Cause**: The dark mode toggle updates in-memory theme state but does not persist the preference to durable storage (localStorage). On browser restart, the in-memory state is lost and the application defaults to light mode. Both the write path (saving on toggle) and the read path (restoring on load) are missing.
```
