## Repository
acme-backend

## Target Branch
main

## Description
Fix dark mode preference persistence so the user's theme selection survives browser
restarts. Currently, toggling dark mode ON and closing the browser causes the
application to revert to light mode on next load. The preference must be written to
persistent storage (e.g., localStorage or a backend user-preferences endpoint) and
read back during application initialization to restore the user's last selected theme.

## Files to Modify
- `src/components/settings/AppearanceSettings.{tsx,vue,js}` -- update the dark mode toggle handler to write the preference to persistent storage (localStorage or backend API) instead of session-scoped or in-memory-only state
- `src/app/init.{ts,js}` -- add or fix the preference read on application startup so the stored dark mode value is applied before first render

## Acceptance Criteria
- [ ] Toggling dark mode to ON and restarting the browser preserves the dark mode setting
- [ ] Toggling dark mode to OFF and restarting the browser preserves the light mode setting
- [ ] The toggle reflects the persisted state on page load (not just the theme)
- [ ] No regression in dark mode behavior within a single session (toggle still works instantly)

## Test Requirements
- [ ] Unit test: toggling dark mode writes the preference to persistent storage
- [ ] Unit test: application initialization reads the persisted preference and applies the correct theme
- [ ] Unit test: when no persisted preference exists, the application defaults to light mode
- [ ] Integration/E2E test: toggle dark mode ON, simulate browser restart (clear session but retain localStorage), verify dark mode loads on next visit

## Bug Context
- **Bug Key**: ACME-511
- **Steps to Reproduce**:
  1. Open the application in a browser.
  2. Navigate to Settings > Appearance.
  3. Toggle "Dark Mode" to ON.
  4. Close the browser completely.
  5. Reopen the browser and navigate back to the application.
- **Expected Result**: The application should load in dark mode, matching the user's last preference.
- **Actual Result**: The application loads in light mode. The dark mode toggle is reset to OFF.
- **Root Cause**: The dark mode preference is stored in session-scoped storage (or not persisted at all) rather than in persistent storage such as localStorage. On browser restart, the session is cleared and the application defaults to light mode.
