# Generated Task Description -- Step 5

**Summary**: Fix dark mode preference persistence across browser sessions

**Labels**: ai-generated-jira

**Link**: Task blocks ACME-511 (link type: Blocks)

---

## Repository
acme-backend

## Target Branch
main

## Description
Fix the dark mode toggle to persist the user's preference across browser sessions. Currently, enabling dark mode via Settings > Appearance only updates the in-memory theme state without writing to localStorage. On application restart, the preference is lost and the app defaults to light mode. This task adds persistence writes on toggle change and persistence reads on initialization. Fixes ACME-511.

## Files to Modify
- Settings > Appearance component (toggle handler) -- add `localStorage.setItem()` call to persist theme preference when the user toggles dark mode
- Application initialization / theme provider -- add `localStorage.getItem()` call to read stored theme preference on startup and apply it before first render

## Implementation Notes
The fix requires two changes that address a single root cause (missing preference persistence):

1. **Persist on toggle**: In the dark mode toggle event handler, after updating the in-memory theme state, call `localStorage.setItem('theme', 'dark')` (or `'light'` when toggling off). This ensures the preference survives browser restarts.

2. **Restore on initialization**: In the application entry point or theme provider component, before the initial render, call `localStorage.getItem('theme')` and set the theme state accordingly. If no stored value is found, default to `'light'` (preserving current default behavior for first-time users).

**Reproducer test guidance** (derived from Steps to Reproduce):
- **Input scenario**: Toggle dark mode to ON via Settings > Appearance
- **Incorrect behavior (Actual Result)**: After simulated restart, app loads in light mode with toggle reset to OFF -- the preference was not stored
- **Correct behavior (Expected Result)**: After simulated restart, app loads in dark mode matching the user's last preference -- the preference was read from localStorage
- **Test approach**: Mock or use localStorage in the test environment. Toggle dark mode, assert `localStorage.getItem('theme') === 'dark'`. Clear in-memory state and re-initialize the theme provider. Assert the theme state is dark mode.

No CONVENTIONS.md was found at the repository root. No data migration is needed (client-side preference, no database persistence boundary).

## Acceptance Criteria
- [ ] A reproducer test exists that toggles dark mode ON, simulates a browser restart (clears in-memory state), and asserts the preference is restored from localStorage -- this test fails before the fix and passes after
- [ ] The dark mode toggle handler persists the preference to localStorage when the user toggles dark mode ON or OFF
- [ ] The application initialization reads the stored theme preference from localStorage and applies it before first render
- [ ] When no stored preference exists (first-time user), the application defaults to light mode
- [ ] No regression in existing tests

## Test Requirements
- [ ] Reproducer test: toggle dark mode to ON, verify `localStorage.setItem` is called with the correct value, clear in-memory state, reinitialize the theme provider, and assert the theme is restored to dark mode from localStorage. Reverse the test: toggle to OFF, restart, assert light mode is restored.
- [ ] Test that first-time users (no localStorage entry) see light mode by default
- [ ] Test that toggling dark mode ON and OFF multiple times always persists the latest preference

## Bug Context

- **Bug**: [ACME-511](https://mock-jira.example.com/browse/ACME-511)
- **Steps to Reproduce**: (1) Open the application, (2) navigate to Settings > Appearance, (3) toggle Dark Mode to ON, (4) close the browser completely, (5) reopen the browser and navigate back to the application
- **Expected Result**: The application should load in dark mode, matching the user's last preference.
- **Actual Result**: The application loads in light mode. The dark mode toggle is reset to OFF.
- **Root Cause**: The dark mode toggle updates in-memory theme state but does not persist the preference to localStorage. On startup, no stored preference is read -- the app unconditionally defaults to light mode.
