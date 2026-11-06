# Step 5 – Generated Task (ACME-511)

**Would be created via `jira.create_issue`.** Not executed, because this is an eval run.

- Project: `ACME`
- Issue type: Task
- Summary: `Fix dark mode preference not persisting across browser sessions (ACME-511)`
- Labels: `["ai-generated-jira"]`
- Link (Step 5b): `jira.create_issue_link(link_type="Blocks", inward_issue_key=<new-task-key>, outward_issue_key="ACME-511")`, so the Task blocks the Bug
- Digest (Step 5c): re-fetch the created description, run `python3 scripts/sha256-digest.py /tmp/desc-<task-key>.txt`, and post `[sdlc-workflow] Description digest: <tagged-digest>` as a standalone comment with no footnote

---

## Repository
acme-backend

> Note: acme-backend is the only repository in the Repository Registry. The bug is a
> front-end UI behavior, so if the theme toggle lives in a separate front-end repository
> that is not registered, re-target this Task to that repository before implementation.

## Target Branch
main

## Description
Fixes ACME-511. When a user turns on dark mode in Settings > Appearance, the preference
is lost after a full browser restart. The app loads in light mode and the toggle shows
OFF. This task makes the dark-mode preference persist across browser sessions: it is
stored durably when toggled, and read back and applied when the app starts.

## Files to Modify
- Not determined during triage. The investigated repository context had no settings,
  theme, or preference-persistence code. The implementer must locate:
  - the Appearance settings / dark-mode toggle handler
  - the theme provider or app bootstrap code that sets the initial theme
  - any user-preferences persistence layer (client storage helper or backend preferences
    endpoint/model)

## Implementation Notes
- Fixes ACME-511. Reference this key in the commit and PR.
- **Locate the code first.** Triage could not confirm file paths. Suggested searches:
  `darkMode`, `dark_mode`, `theme`, `Appearance`, `prefers-color-scheme`, `localStorage`,
  `sessionStorage`, `document.cookie`, and in `acme-backend`: `preference`, `settings`,
  `theme`.
- **Likely defect (unconfirmed):** the preference is not round-tripped through durable
  storage. Check for these cases, in order:
  1. The toggle writes only to in-memory state or `sessionStorage`, which are cleared on browser close.
  2. The theme initializer ignores the stored value and always uses a hard-coded `light`
     default, or applies the stored value and then overwrites it with the default.
  3. A backend preferences API exists, but it is not called on toggle or not fetched on load.
- **Fix direction:** write the preference to durable storage when toggled (`localStorage`,
  or the user's backend preference record if preferences are account-scoped). At startup,
  read it and apply it before or at first render, using `light` only when no value is stored.
- **Reproducer scenario (from Steps to Reproduce):**
  - Trigger: set dark mode ON through the same code path the Settings > Appearance toggle uses.
  - Simulate browser close/reopen: clear in-memory state and `sessionStorage`, keep durable
    storage, then re-initialize the app or theme provider.
  - Before the fix (Actual Result): theme resolves to `light` and the toggle reads OFF.
  - After the fix (Expected Result): theme resolves to `dark` and the toggle reads ON.
- **Persistence impact:** no corrective data migration is expected, because the defect is a
  missing or ignored value, not an incorrect persisted value. If the fix adds a new
  server-side preference column or table, add a schema migration that follows the
  repository's existing migration naming convention (find it by searching for
  `migrations/` directories).
- No `CONVENTIONS.md` exists at the repository root, so follow the existing patterns in the
  files you modify.
- No existing theme or preference tests were found during triage. Put the reproducer next
  to the toggle or theme provider's existing unit tests, or create a test file that
  follows the repository's test layout.

## Acceptance Criteria
- [ ] A reproducer test enables dark mode, simulates a new browser session (in-memory and
      session state reset, durable storage kept), and asserts that the theme is `dark` and the
      toggle is ON. It fails before the fix and passes after.
- [ ] Toggling dark mode ON or OFF writes the preference to durable storage that survives a
      browser restart.
- [ ] On startup, the app reads the stored preference and applies it at or before first
      render, with no flash of the wrong theme after the stored value loads.
- [ ] With no stored preference, the app falls back to the existing default (light mode).
- [ ] All existing tests pass with no regressions.

## Test Requirements
- [ ] Reproducer test for ACME-511: set dark mode ON through the toggle's code path,
      reset in-memory and `sessionStorage` state to simulate closing and reopening the browser,
      re-initialize the app or theme provider, then assert `theme === "dark"` and the toggle
      state is ON. Before the fix it should observe `light` / OFF (Actual Result). After the
      fix it must observe `dark` / ON (Expected Result).
- [ ] Test that toggling dark mode OFF after it was ON persists `light` across a simulated
      session restart.
- [ ] Test that a first-time user with no stored preference gets the default light theme.

## Bug Context

- **Bug**: [ACME-511](https://mock-jira.example.com/browse/ACME-511)
- **Steps to Reproduce**: Open the app, go to Settings > Appearance, toggle "Dark Mode"
  ON, fully close the browser, then reopen it and go back to the app.
- **Expected Result**: The application should load in dark mode, matching the user's last
  preference.
- **Actual Result**: The application loads in light mode. The dark mode toggle is reset to
  OFF.
- **Root Cause**: The dark-mode preference is not round-tripped through persistent storage.
  It is either kept only in session or in-memory state, or not read back and applied at
  startup (falling back to the `light` default). The exact file and symbol could not be
  confirmed during triage because the investigated repository context had no theme or
  preference code. Affects Version is unknown: the reporter said "whatever is deployed on
  staging", and a gap comment asks for it to be set manually.
