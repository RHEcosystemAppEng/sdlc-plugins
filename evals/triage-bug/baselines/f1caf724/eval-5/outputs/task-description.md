## Repository
acme-backend

## Target Branch
main

## Description
Fix dark mode preference persistence so that the user's theme choice survives browser restarts. The toggle handler currently updates only in-memory state without writing to a durable store, causing the preference to be lost when the browser is closed. This task adds persistent storage for the dark mode preference and restores it on application initialization. Fixes ACME-511.

## Files to Modify
- `src/components/settings/appearance.rs` -- add persistent storage write when dark mode is toggled
- `src/app/init.rs` -- read persisted dark mode preference on application startup and apply it before rendering

## Implementation Notes
The dark mode toggle handler needs to write the preference to a persistent store (e.g., localStorage on the client side or a user_preferences API endpoint on the server side) whenever the toggle state changes. The application initialization code must read this stored preference and apply the dark mode theme before the first render to avoid a flash of light mode.

Key guidance for the reproducer test:
- **Input/scenario that triggers the bug**: Toggle dark mode ON, then simulate a fresh application load (clear in-memory state).
- **Incorrect behavior (Actual Result)**: After fresh load, the application is in light mode and the toggle is OFF -- the preference was not persisted or not restored.
- **Correct behavior (Expected Result)**: After fresh load, the application is in dark mode and the toggle is ON -- the preference was persisted and restored.
- The reproducer test must fail before the fix and pass after the fix.

The repository does not have a CONVENTIONS.md, so no repo-specific conventions apply.

## Acceptance Criteria
- [ ] A reproducer test demonstrates the bug: it toggles dark mode ON, simulates a fresh application load, and asserts that the preference is NOT restored (fails before fix, passes after fix with corrected assertion)
- [ ] The dark mode toggle handler persists the preference to durable storage when toggled
- [ ] Application initialization reads the persisted dark mode preference and applies it before rendering
- [ ] Toggling dark mode OFF also persists correctly (preference cleared or set to light mode)
- [ ] No regression in existing tests

## Test Requirements
- [ ] Reproducer test: toggle dark mode ON, verify the preference value is written to the persistent store, simulate a fresh application load (reset in-memory state), verify the preference is read from the store and dark mode is applied. This test must fail before the fix and pass after it.
- [ ] Test that toggling dark mode OFF persists the "off" state and is restored correctly on fresh load
- [ ] Test that when no persisted preference exists, the application defaults to light mode (existing behavior preserved)

## Bug Context

- **Bug**: [ACME-511](https://mock-jira.example.com/browse/ACME-511)
- **Steps to Reproduce**: Open application, navigate to Settings > Appearance, toggle Dark Mode ON, close browser completely, reopen browser and navigate back to the application.
- **Expected Result**: The application should load in dark mode, matching the user's last preference.
- **Actual Result**: The application loads in light mode. The dark mode toggle is reset to OFF.
- **Root Cause**: The dark mode toggle updates in-memory state but does not persist the preference to durable storage. On browser restart, in-memory state is lost and the application defaults to light mode.
