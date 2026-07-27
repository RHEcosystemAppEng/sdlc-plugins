## Repository
acme-backend

## Target Branch
main

## Description
Persist the dark mode user preference across browser sessions by writing the theme
selection to localStorage on toggle and reading it back on application initialization.
Fixes ACME-511.

## Files to Modify
- Settings / Appearance component (dark mode toggle handler) -- add localStorage write on toggle change
- Application initialization / theme provider -- add localStorage read on startup to restore persisted theme preference

## Implementation Notes
The dark mode toggle currently updates only ephemeral in-memory state (component state
or store). The fix requires two changes:

1. **Persist on toggle**: When the user changes the dark mode toggle in Settings >
   Appearance, write the preference value to `localStorage` (e.g.,
   `localStorage.setItem('theme-preference', 'dark')` or equivalent). This must happen
   in the same handler that updates the in-memory state.

2. **Restore on init**: During application initialization (before or during first
   render), read the stored preference from `localStorage`. If a stored value exists,
   apply it as the active theme and set the toggle state accordingly. If no stored
   value exists, fall back to the default (light mode).

Key considerations:
- Handle the case where localStorage is unavailable (private browsing, storage full)
  gracefully -- fall back to default theme without errors
- The persisted key name should be consistent and documented
- Consider using a constants file for the localStorage key name to avoid magic strings

Fixes [ACME-511](https://mock-jira.example.com/browse/ACME-511).

## Acceptance Criteria
- [ ] A reproducer test demonstrates the bug: toggling dark mode ON, simulating a new session (clearing in-memory state), and verifying the application reverts to light mode WITHOUT the fix (fails before fix, passes after fix with persistence implemented)
- [ ] Dark mode preference is written to persistent storage (localStorage) when the user toggles the setting
- [ ] On application load, the persisted theme preference is read and applied before first render
- [ ] The dark mode toggle UI reflects the persisted state on load (shows ON if dark mode was previously selected)
- [ ] If no persisted preference exists, the application defaults to light mode
- [ ] No regression in existing tests

## Test Requirements
- [ ] Reproducer test: toggle dark mode ON, verify preference is written to localStorage, clear in-memory state, re-initialize the application, assert dark mode is active and toggle shows ON. This test must fail before the fix (demonstrating the persistence gap) and pass after
- [ ] Test that toggling dark mode OFF removes or updates the persisted preference, and a new session loads in light mode
- [ ] Test graceful fallback when localStorage is unavailable (e.g., mock localStorage to throw) -- application should default to light mode without errors
- [ ] Test that the toggle UI state matches the persisted preference on initial load

## Verification Commands
- Run the application locally, toggle dark mode ON in Settings > Appearance, close and reopen the browser, verify the application loads in dark mode

## Bug Context

- **Bug**: [ACME-511](https://mock-jira.example.com/browse/ACME-511)
- **Steps to Reproduce**: Open the application, navigate to Settings > Appearance, toggle Dark Mode to ON, close the browser, reopen and navigate back to the application
- **Expected Result**: The application should load in dark mode, matching the user's last preference
- **Actual Result**: The application loads in light mode; the dark mode toggle is reset to OFF
- **Root Cause**: The dark mode preference is stored only in ephemeral component state with no persistence mechanism. When the browser session ends, the state is lost and the application defaults to light mode on the next load.
