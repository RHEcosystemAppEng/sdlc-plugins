# Task: Fix dark mode preference persistence across browser sessions

**Labels**: ai-generated-jira

## Repository
acme-backend

## Target Branch
main

## Description
Fix the dark mode toggle so that the user's theme preference persists across browser
sessions. Currently the preference is held only in runtime state and is lost when the
browser is closed. The toggle handler must write the preference to durable client-side
storage (e.g., localStorage), and the theme initialization logic must read the stored
preference on startup. Fixes ACME-511.

## Files to Modify
- Settings/Appearance component -- add localStorage write when dark mode is toggled
- Theme initialization module -- add localStorage read on application startup to restore the saved theme preference

## Implementation Notes
The dark mode toggle currently updates only in-memory/component state. To fix:

1. **Toggle handler**: when the user toggles dark mode ON or OFF, write the preference
   to `localStorage` (e.g., `localStorage.setItem('theme', 'dark')` or `'light'`).
2. **Theme initialization**: on application startup (before first render), read the
   stored theme preference from `localStorage`. If a value exists, apply it as the
   initial theme. If no value exists, fall back to the default (light mode).
3. **Consistency**: ensure the toggle UI state reflects the persisted value on page load,
   not just the default.

Search for existing theme/preference utilities in the codebase that may already handle
other persistent settings -- reuse the same storage pattern for consistency.

Note: During investigation, a trailing whitespace bug was found in the convention heading
extraction at `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` (`line[3:]` does not
strip trailing whitespace). This is unrelated to the dark mode bug and should be tracked
separately.

Fixes ACME-511.

## Acceptance Criteria
- [ ] A reproducer test demonstrates the bug: enables dark mode, simulates session restart (clears runtime state while preserving localStorage), and asserts the application loads in dark mode -- this test fails before the fix and passes after
- [ ] The dark mode toggle writes the user's preference to persistent client-side storage (e.g., localStorage) on every toggle
- [ ] The application reads the stored theme preference on startup and applies it before rendering
- [ ] The dark mode toggle UI reflects the persisted preference on page load
- [ ] No regression in existing tests

## Test Requirements
- [ ] Reproducer test: enable dark mode, clear runtime state (simulating browser restart), re-initialize the application, and assert that (a) the theme is dark mode, (b) the toggle shows ON. The test should initially fail (demonstrating the bug) and pass after the fix is applied.
- [ ] Test that toggling dark mode OFF also persists correctly (application loads in light mode after restart)
- [ ] Test that when no stored preference exists, the application defaults to light mode
- [ ] Test that the stored preference survives across multiple simulated session restarts

## Bug Context

- **Bug**: [ACME-511](https://mock-jira.example.com/browse/ACME-511)
- **Steps to Reproduce**: Open the application, navigate to Settings > Appearance, toggle Dark Mode to ON, close the browser completely, reopen and navigate back to the application.
- **Expected Result**: The application should load in dark mode, matching the user's last preference.
- **Actual Result**: The application loads in light mode. The dark mode toggle is reset to OFF.
- **Root Cause**: The dark mode preference is stored only in application runtime state and is not persisted to durable client-side storage. When the browser session ends, the preference is lost and the application defaults to light mode.
