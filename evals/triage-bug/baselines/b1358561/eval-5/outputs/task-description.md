# Step 5 – Generated Task for ACME-511

**Summary**: Fix dark mode preference not persisting across browser sessions
**Project**: ACME
**Issue type**: Task
**Labels**: ai-generated-jira
**Link**: Task blocks ACME-511 (link type: Blocks; inward = Task, outward = ACME-511)

> Triage note: the codebase investigation could not locate the dark-mode code in
> the registered repository, so file paths below are not asserted. The implementer
> must first locate the toggle handler and theme initialization (see
> Implementation Notes). Repository is listed as acme-backend because it is the
> only registered repository; if the defect is purely front-end, the Task should be
> re-targeted to the front-end repository once it is added to the Registry.

---

## Repository
acme-backend

## Target Branch
main

## Description
Fixes ACME-511. When a user enables dark mode in Settings > Appearance and then
closes and reopens the browser, the application loads in light mode and the toggle
is reset to OFF. The user's theme preference must be durably persisted and
restored on application load so it survives a full browser restart.

## Files to Modify
- To be determined — the Dark Mode toggle handler (Settings > Appearance), the
  theme initialization run at application startup, and, if applicable, the
  acme-backend user-preferences handler. These were not present in the
  investigated repository context; locate them before making changes.

## Implementation Notes
Fixes ACME-511.

1. **Locate the code paths** (not found during triage):
   - Search for the toggle: Grep for `dark`, `darkMode`, `theme`, `Appearance`.
   - Search for storage: Grep for `sessionStorage`, `localStorage`, `cookie`,
     and any user-preferences API client/endpoint (`preferences`, `settings`).
   - Search for startup theme setup: theme provider / app bootstrap code.
2. **Determine which candidate cause applies** (see Bug Context → Root Cause):
   - Preference held only in memory or `sessionStorage` → move to durable storage
     (localStorage/persistent cookie, or backend user preferences if the app
     already syncs user settings server-side).
   - Preference persisted but startup ignores it / overwrites with default → read
     the stored value during initialization before first render; default to light
     only when no stored value exists.
   - Backend drops the theme field → persist and return it from the
     user-preferences endpoint in acme-backend.
3. **Reproducer test guidance**:
   - Trigger: set dark mode ON via the toggle handler, then simulate a new browser
     session (reset in-memory app state and `sessionStorage`; keep durable
     storage, or re-fetch preferences from the backend), then re-initialize the app.
   - Before fix (Actual Result): active theme is `light`, toggle reads OFF.
   - After fix (Expected Result): active theme is `dark`, toggle reads ON.
   - Follow the existing test conventions of whichever repository holds the code
     (no relevant test files were identified during triage).
4. **Persistence impact**: not established during triage. If a backend preference
   column exists and was simply never written, no data migration is needed. If
   existing rows hold incorrect theme values, add a migration following the
   repository's existing migration conventions.
5. No CONVENTIONS.md exists at the acme-backend root.

## Acceptance Criteria
- [ ] A reproducer test sets dark mode ON, simulates a new browser session, re-initializes the app, and asserts the theme is dark and the toggle is ON — it fails before the fix and passes after
- [ ] The dark mode preference is stored in a durable location that survives a full browser restart
- [ ] On application load, the stored theme preference is applied before first render and the Settings > Appearance toggle reflects it
- [ ] When no preference is stored, the application defaults to light mode
- [ ] Toggling dark mode OFF is also persisted and restored across sessions
- [ ] No regression in existing tests

## Test Requirements
- [ ] Reproducer test: toggle dark mode ON → simulate browser restart (clear in-memory state and sessionStorage, retain durable storage / re-fetch backend preferences) → re-initialize app → assert theme == `dark` and toggle == ON (initially fails with theme `light`, toggle OFF per ACME-511 Actual Result)
- [ ] Test that toggling OFF then restarting restores light mode
- [ ] Test that with no stored preference the app initializes in light mode
- [ ] If the backend user-preferences store is involved: test that saving `theme=dark` and reading it back in a fresh request returns `dark`

## Bug Context

- **Bug**: [ACME-511](https://mock-jira.example.com/browse/ACME-511)
- **Steps to Reproduce**: Open the app → Settings > Appearance → toggle Dark Mode ON → close the browser completely → reopen and navigate back to the app.
- **Expected Result**: The application should load in dark mode, matching the user's last preference.
- **Actual Result**: The application loads in light mode. The dark mode toggle is reset to OFF.
- **Root Cause**: Unconfirmed (low confidence). The theme preference is most likely held only in non-durable state (memory/sessionStorage) or is not read during app initialization, so a new browser session falls back to the light default. Dark-mode code was not found in the registered repository during triage.
- **Affects Version**: Not determined — Environment / Version section ("Not sure which version — using whatever is deployed on staging") contained no version identifier; a gap comment was posted asking for manual setting.
