<!--
jira_project: ACME
jira_issue_type_id: 10016
jira_parent_key: ACME-511
jira_link_type: Blocks
-->

## Repository
acme-backend

## Target Branch
main

## Description
Fix dark mode preference persistence so the user's theme choice survives browser session closure. Currently, when a user enables dark mode via Settings > Appearance and then closes and reopens the browser, the application reverts to light mode because the preference is not written to persistent storage (or is written to sessionStorage, which is cleared on browser close). The fix must ensure the preference is stored in localStorage (or equivalent persistent storage) and read back on application initialization.

## Files to Modify
- Settings/Appearance toggle handler — add or fix the persistence write to `localStorage`
- Theme provider / application initialization — ensure the stored preference is read from `localStorage` on startup and applied before first render

## Implementation Notes
The dark mode toggle currently updates in-memory or session-scoped state but does not persist the preference across browser sessions. The fix should:

1. In the toggle handler, write the user's theme preference to `localStorage` using a well-defined key (e.g., `user-theme-preference`).
2. In the application initialization / theme provider, read from the same `localStorage` key and apply the stored theme before the first render to avoid a flash of incorrect theme.
3. If the stored value is missing or invalid, fall back to the system default (light mode).

Front-load the reproducer test (see Test Requirements) so the failing behavior is captured before the fix is applied.

## Acceptance Criteria
- [ ] Dark mode preference persists across browser sessions (close and reopen browser)
- [ ] Light mode preference also persists correctly when toggled back
- [ ] Application loads with the correct theme on startup without a visible flash of the wrong theme
- [ ] Falling back to light mode when no preference is stored works correctly

## Test Requirements
- [ ] **Reproducer test (write first)**: Test that toggles dark mode ON, simulates a session boundary (clear in-memory state, re-initialize), and asserts the preference is still dark mode — this test should fail before the fix and pass after
- [ ] Test that verifies `localStorage` is written when the dark mode toggle is changed
- [ ] Test that verifies the application reads the theme preference from `localStorage` on initialization
- [ ] Test that verifies the default theme (light mode) is applied when no stored preference exists

## Bug Context
- **Bug**: [ACME-511](https://mock-jira.example.com/browse/ACME-511) — Dark mode toggle does not persist across browser sessions
- **Steps to Reproduce**:
  1. Open the application in a browser.
  2. Navigate to Settings > Appearance.
  3. Toggle "Dark Mode" to ON.
  4. Close the browser completely.
  5. Reopen the browser and navigate back to the application.
- **Expected Result**: The application should load in dark mode, matching the user's last preference.
- **Actual Result**: The application loads in light mode. The dark mode toggle is reset to OFF.
- **Root Cause**: The dark mode preference is not persisted to a storage mechanism that survives browser session closure. The toggle handler updates in-memory/session state without writing to localStorage or equivalent persistent storage. On reload, the application finds no persisted preference and defaults to light mode.
