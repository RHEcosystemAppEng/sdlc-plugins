## Repository
acme-backend

## Target Branch
main

## Description
Persist the dark mode user preference across browser sessions so that the selected theme survives browser restarts. Currently the preference is stored only in volatile in-memory state and is lost when the browser is closed, causing the application to revert to light mode. Fixes ACME-511.

## Files to Modify
- Settings panel toggle handler -- add a write to persistent storage (e.g., localStorage) when the user toggles dark mode
- Application initialization/bootstrap module -- add logic to read the persisted theme preference on startup and apply it before first render

## Implementation Notes
The root cause is that the dark mode toggle handler updates only in-memory state without writing to any persistent storage. The application initialization code does not check for a saved preference and defaults to light mode.

**Fix approach:**

1. In the settings panel toggle handler, after updating the in-memory theme state, persist the preference to `localStorage` (or the application's preferred storage mechanism). Use a well-defined key (e.g., `user-theme-preference`).
2. In the application initialization/bootstrap code, before rendering, check `localStorage` for a saved theme preference. If found, apply it to the application state so the UI renders with the correct theme immediately.
3. Handle the edge case where no saved preference exists (first-time users) -- default to light mode as current behavior.

**Reproducer test guidance (derived from Steps to Reproduce):**
- The reproducer must simulate the full cycle: toggle dark mode ON, persist, clear in-memory state (simulating browser restart), re-initialize the application, and assert dark mode is active.
- **Input/trigger**: Toggle dark mode to ON via the settings panel.
- **Incorrect behavior (before fix)**: After simulated restart, the application loads in light mode and the toggle is OFF because no preference was persisted.
- **Correct behavior (after fix)**: After simulated restart, the application loads in dark mode and the toggle is ON because the preference was read from persistent storage.

Fixes [ACME-511](https://mock-jira.example.com/browse/ACME-511).

## Acceptance Criteria
- [ ] A reproducer test exists that toggles dark mode ON, simulates a browser session restart (clears in-memory state, re-initializes the application), and asserts the application loads in dark mode with the toggle in the ON position. This test fails before the fix and passes after the fix.
- [ ] When a user toggles dark mode ON and closes the browser, reopening the application loads in dark mode matching the last preference.
- [ ] When a user toggles dark mode OFF and closes the browser, reopening the application loads in light mode.
- [ ] First-time users with no saved preference see light mode as the default.
- [ ] No regression in existing tests.

## Test Requirements
- [ ] Reproducer test: simulate enabling dark mode, persist the preference, clear in-memory state (simulating session restart), re-initialize the application, and assert that (a) the application renders in dark mode and (b) the dark mode toggle is in the ON position. Before the fix, the test must fail (application defaults to light mode). After the fix, the test must pass.
- [ ] Test that toggling dark mode OFF and restarting loads light mode.
- [ ] Test that a first-time user with no stored preference gets light mode by default.
- [ ] Test that corrupted or missing storage values are handled gracefully (fallback to light mode).

## Bug Context

- **Bug**: [ACME-511](https://mock-jira.example.com/browse/ACME-511)
- **Steps to Reproduce**: 1) Open the application in a browser. 2) Navigate to Settings > Appearance. 3) Toggle "Dark Mode" to ON. 4) Close the browser completely. 5) Reopen the browser and navigate back to the application.
- **Expected Result**: The application should load in dark mode, matching the user's last preference.
- **Actual Result**: The application loads in light mode. The dark mode toggle is reset to OFF.
- **Root Cause**: The dark mode preference is stored only in volatile in-memory state. No code path persists the preference to durable storage. On browser restart, the state is lost and the application defaults to light mode.
