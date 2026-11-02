## Repository
acme-backend

## Target Branch
main

## Description
Fix dark mode toggle persistence so the user's theme preference survives browser session restarts. Currently, enabling dark mode via Settings > Appearance does not persist the preference to durable storage, causing the application to revert to light mode when the browser is closed and reopened (ACME-511).

## Files to Modify
- `src/components/settings/Appearance.tsx` -- Update the dark mode toggle handler to persist the preference to `localStorage`
- `src/theme/ThemeProvider.tsx` -- Read the stored theme preference from `localStorage` on initialization and apply it before first render

## Implementation Notes
- Use `localStorage.setItem('theme-preference', 'dark' | 'light')` to persist the user's choice when the toggle changes.
- On application startup, read `localStorage.getItem('theme-preference')` and set the initial theme state accordingly. If no stored value exists, default to `'light'`.
- Do NOT use `sessionStorage` -- it is scoped to the browser session and is cleared when the browser closes, which is the likely root cause of this bug.
- If a `useTheme` hook or `ThemeContext` already exists, integrate the persistence logic there to keep theme management centralized.

## Acceptance Criteria
- [ ] Enabling dark mode and restarting the browser preserves the dark mode preference
- [ ] Disabling dark mode and restarting the browser preserves the light mode preference
- [ ] When no stored preference exists (first visit), the application defaults to light mode
- [ ] The toggle in Settings > Appearance reflects the persisted state on page load

## Test Requirements
- [ ] Unit test: toggling dark mode writes the correct value to `localStorage`
- [ ] Unit test: application initialization reads theme preference from `localStorage`
- [ ] Integration test: simulate a session restart (clear in-memory state, reinitialize component) and verify theme persists

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
- **Root Cause**: The dark mode preference is not persisted to durable browser storage (`localStorage`). It is either stored only in memory or in `sessionStorage`, both of which are lost when the browser session ends.
