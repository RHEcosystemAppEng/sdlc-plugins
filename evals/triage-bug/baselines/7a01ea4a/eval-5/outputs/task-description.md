# Task: Fix dark mode preference persistence across browser sessions

**Labels**: ai-generated-jira

## Repository
acme-backend

## Target Branch
main

## Description
Fix the dark mode toggle so that the user's preference persists across browser sessions. Currently, enabling dark mode via Settings > Appearance and then closing and reopening the browser causes the application to revert to light mode. The preference must be written to durable storage (e.g., localStorage) on change and restored on application initialization. Fixes ACME-511.

## Files to Modify
- `src/settings/appearance.rs` (or equivalent settings module) -- add persistence logic to the dark mode toggle handler
- `src/app/init.rs` (or equivalent initialization module) -- read persisted dark mode preference on startup and apply it before rendering

## Files to Create
- `tests/settings/test_dark_mode_persistence.rs` -- reproducer test for dark mode persistence across sessions

## Implementation Notes
The dark mode toggle handler in the Settings/Appearance module currently updates only in-memory state. The fix requires two changes:

1. **Persist on change**: When the user toggles dark mode, write the preference to a durable store (e.g., localStorage via a browser storage API, or a backend user preferences endpoint). Ensure the write happens synchronously or is awaited before confirming the toggle.

2. **Restore on init**: During application initialization (before the UI renders), read the persisted dark mode preference. If a persisted value exists, apply it as the initial theme. If no persisted value exists, default to light mode (current behavior).

**Reproducer test guidance**: The test should:
- Set up the application in its default state (light mode).
- Simulate toggling dark mode to ON via the Settings > Appearance path.
- Verify the preference is written to the persistence layer.
- Simulate a session restart: clear in-memory application state while preserving the persistence layer.
- Re-initialize the application.
- Assert that the application loads in dark mode (the toggle is ON and the theme is dark).

This test should FAIL before the fix (preference not persisted, application reverts to light mode) and PASS after the fix.

Related pattern discovered during investigation: the convention heading extraction in `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` uses `line[3:]` without stripping trailing whitespace, causing exact-match failures. While this is a different code path, it illustrates the same class of issue -- values not normalized before comparison/storage.

Fixes ACME-511.

## Acceptance Criteria
- [ ] A reproducer test demonstrates the bug: enables dark mode, simulates session restart, and asserts dark mode is restored (fails before fix, passes after)
- [ ] Dark mode preference is persisted to durable storage when the user toggles it
- [ ] On application startup, the persisted dark mode preference is read and applied before rendering
- [ ] The dark mode toggle UI reflects the persisted state after a session restart
- [ ] No regression in existing tests

## Test Requirements
- [ ] Reproducer test: enable dark mode via Settings > Appearance, simulate session close/reopen (clear in-memory state, preserve persistent storage), re-initialize application, assert dark mode is active and toggle shows ON. Must fail before fix and pass after.
- [ ] Unit test for the persistence write: verify that toggling dark mode writes the correct value to the storage layer
- [ ] Unit test for the persistence read: verify that application initialization reads the stored preference and applies it
- [ ] Edge case test: verify that when no persisted preference exists, the application defaults to light mode

## Verification Commands
- `cargo test test_dark_mode_persistence` -- should pass after the fix, confirming dark mode preference survives session restart

## Bug Context

- **Bug**: [ACME-511](https://mock-jira.example.com/browse/ACME-511)
- **Steps to Reproduce**: Open app, navigate to Settings > Appearance, toggle Dark Mode ON, close browser completely, reopen browser and navigate back to app.
- **Expected Result**: The application should load in dark mode, matching the user's last preference.
- **Actual Result**: The application loads in light mode. The dark mode toggle is reset to OFF.
- **Root Cause**: The dark mode preference is not persisted to durable storage. The toggle state is held only in in-memory application state, which is lost when the browser session ends. No write to persistent storage occurs on preference change, and no read occurs on application initialization.
