# Step 5 – Generated Task (ACME-511)

**Project**: ACME
**Issue type**: Task
**Summary**: Persist dark mode preference across browser sessions (fixes ACME-511)
**Labels**: ai-generated-jira
**Link**: this Task **Blocks** ACME-511 (inward = Task, outward = ACME-511)

> Triage caveat: the root cause could not be confirmed against code. The registered
> repository (acme-backend) contained no theme/preference code in the analysed
> context. File paths below are left for the implementer to find instead of being
> invented. If the toggle is in a frontend repository, add that repository to the
> Repository Registry and re-target this Task.

---

## Repository
acme-backend

## Target Branch
main

## Description
Fixes ACME-511. When a user turns on dark mode in Settings > Appearance and then
closes and reopens the browser, the application loads in light mode and the toggle
is reset to OFF. The preference must be saved to storage that outlives the browser
session, and read and applied when the application starts, so the app loads in the
user's last chosen theme.

## Files to Modify
- Not determined during triage. No files related to dark mode, theme state, the
  Settings/Appearance panel or user-preference persistence were found in the
  analysed repository context. The implementer must first locate:
  - the Settings > Appearance "Dark Mode" toggle handler
  - the theme state/store/provider initialisation (app startup)
  - any user-preferences/settings API endpoint and storage in acme-backend, if
    preferences are saved on the server

## Implementation Notes
- Fixes ACME-511.
- **Locate the code first.** Grep the repository for `dark`, `darkMode`,
  `dark_mode`, `theme`, `Appearance`, `prefers-color-scheme`, `localStorage`,
  `sessionStorage`, `cookie`, `preferences`, `user_settings`. If nothing related is
  in acme-backend, the fix belongs in the frontend repository. Stop and report back
  so the Task can be re-targeted.
- **Likely causes to check, in order:**
  1. The toggle only updates in-memory state, `sessionStorage`, or a session cookie
     with no `Expires`/`Max-Age`. These are cleared when the browser closes. Switch
     to persistent storage (`localStorage`, a persistent cookie, or the backend user
     preferences).
  2. The value is saved, but app initialisation always applies the default (light)
     theme or overwrites the stored value. Read the persisted preference during
     initialisation, before first render, and only use the default when no value is
     stored.
  3. Server-side preferences: the settings update doesn't send or store the theme,
     or the user-settings response used at startup doesn't include it.
- **Reproducer scenario (from Steps to Reproduce):** open the app, go to Settings >
  Appearance, toggle Dark Mode ON, simulate a full browser restart (clear in-memory
  state, `sessionStorage` and session cookies, but keep persistent storage), then
  load the app again.
  - Before the fix, the test observes the Actual Result: light theme, toggle OFF.
  - After the fix, the test asserts the Expected Result: dark theme, toggle ON.
- **Persistence impact:** the defect appears to be that no value is persisted, not
  that a wrong value is persisted. No data migration is expected. If a backend
  preferences column turns out to hold incorrect values, add a migration that
  follows the repository's existing migration conventions.
- No CONVENTIONS.md exists at the repository root. Follow existing patterns in the
  code that handles settings/preferences once it is located.
- Respect existing behaviour such as `prefers-color-scheme` defaults when no stored
  preference exists.

## Acceptance Criteria
- [ ] A reproducer test enables dark mode, simulates a new browser session (keeping
      persistent storage) and asserts that the app loads in dark mode with the
      toggle ON. The test fails before the fix and passes after.
- [ ] Turning dark mode ON or OFF saves the preference to storage that survives a
      browser restart.
- [ ] On startup, the app reads the saved preference and applies it before first
      render, with no flash of the wrong theme where feasible.
- [ ] When no preference is saved, the app uses the existing default theme.
- [ ] Switching dark mode back OFF is also saved, and the app reloads in light mode.
- [ ] No regression in existing tests.

## Test Requirements
- [ ] Reproducer test (first): toggle Dark Mode ON through Settings > Appearance,
      reset the session (clear in-memory state, `sessionStorage` and session cookies;
      keep `localStorage`/persistent cookies/backend preferences), reload or re-mount
      the app, and assert that the active theme is dark and the toggle is ON. Before
      the fix, this assertion fails (theme is light, toggle OFF, as in ACME-511's
      Actual Result).
- [ ] Test that the default theme is used when no preference is stored.
- [ ] Test that turning dark mode OFF is saved and restored as light mode.
- [ ] If the backend saves preferences, add an API/integration test that the theme
      value round-trips through the user-preferences endpoint.

## Bug Context

- **Bug**: [ACME-511](https://mock-jira.example.com/browse/ACME-511)
- **Steps to Reproduce**: Open the app, go to Settings > Appearance, toggle "Dark
  Mode" ON, close the browser completely, reopen it and go back to the app.
- **Expected Result**: The application should load in dark mode, matching the
  user's last preference.
- **Actual Result**: The application loads in light mode. The dark mode toggle is
  reset to OFF.
- **Root Cause**: Not confirmed in code (low confidence). The dark mode preference
  is either kept only in session-scoped or in-memory state, or saved but not read
  back during app initialisation, so the theme falls back to the light default. No
  related code was found in the registered acme-backend repository context. The UI
  code is likely in an unregistered frontend repository.
- **Affects Version**: Not determined. The Environment / Version section says "Not
  sure which version — using whatever is deployed on staging". A gap comment was
  posted on ACME-511 asking for it to be set manually.

---

## Follow-up Jira operations (not executed in eval)

1. `jira.create_issue(project="ACME", issuetype="Task", summary=..., description=<above>, additional_fields={"labels": ["ai-generated-jira"]})`
2. `jira.create_issue_link(link_type="Blocks", inward_issue_key=<new-task-key>, outward_issue_key="ACME-511")`
3. Step 5c: re-fetch the created task's description, run `python3 scripts/sha256-digest.py`
   on it, and post a standalone comment `[sdlc-workflow] Description digest: <tagged-digest>`
   (no footnote).
4. Step 7: suggest "Run `/implement-task <task-key>` to implement the fix."
