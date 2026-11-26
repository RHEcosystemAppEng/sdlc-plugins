# Step 5 – Generated Task (not actually created — eval mode)

## Jira create_issue parameters

| Parameter | Value |
|---|---|
| Project key | ACME |
| Issue type | Task |
| Summary | Fix dark mode preference not persisting across browser sessions |
| Labels | `ai-generated-jira` |

## Step 5b – Link (would be created)

`jira.create_issue_link(link_type="Blocks", inward_issue_key=<new-task-key>, outward_issue_key="ACME-511")`
— the Task blocks the Bug.

## Step 5c – Digest (would be posted)

After creation, re-fetch the Task description, compute
`python3 scripts/sha256-digest.py /tmp/desc-<task-key>.txt`, and post a standalone comment
`[sdlc-workflow] Description digest: <tagged-digest>` (no footnote).

---

## Task description

## Repository
acme-backend

## Target Branch
main

## Description
Fixes ACME-511. When a user enables Dark Mode in Settings > Appearance and then fully closes
and reopens the browser, the application reverts to light mode and the toggle resets to OFF.
The user's theme preference must be durably persisted when toggled and restored on
application startup so the app loads in the user's last-selected theme.

Note: triage could not locate the affected code in the investigated repository context
(root-cause confidence is low). The first step of this task is to confirm where theme state
is stored and initialized. If that code lives in a frontend repository rather than
acme-backend, re-target this task to that repository (and add it to the Repository
Registry) before implementing.

## Files to Modify
- Not identified during triage. Locate and modify:
  - the Settings > Appearance dark-mode toggle handler (write preference to durable storage)
  - the application theme initialization / bootstrap code (read preference before first render)
  - if preferences are server-side in acme-backend: the user-settings save/load handler(s)
    so the theme field is stored and returned

## Implementation Notes
- Fixes ACME-511.
- Start by searching the codebase for `dark`, `theme`, `appearance`, `localStorage`,
  `sessionStorage`, and `preferences`/`user_settings` to find (a) where the toggle writes
  state and (b) where the initial theme is chosen on load. The investigated repository
  context contained no matches for these terms.
- Likely defects to check (from root cause analysis):
  1. Toggle updates only in-memory state or `sessionStorage` (cleared on browser close)
     instead of durable storage.
  2. Preference is stored, but startup applies a hard-coded light default and never reads
     it back; the toggle component also initializes from the default.
  3. Server-side save is not called, fails silently, or the load response omits the theme.
- Fix direction: persist on toggle using the project's existing preference-storage
  mechanism (do not introduce a new one if one exists); hydrate theme and toggle state from
  that storage during app initialization, before first render, to avoid a light-mode flash.
- Reproducer test guidance:
  - Trigger: set dark mode ON via the toggle code path, then simulate a new browser session
    (reset in-memory app state and `sessionStorage`; keep `localStorage`/cookies or
    re-fetch user settings from the backend), then re-initialize the app.
  - Before fix (Actual Result): theme is light and the toggle is OFF.
  - After fix (Expected Result): theme is dark and the toggle is ON.
- Follow the existing test layout and assertion patterns of the repository that owns the
  theme code (none were found during triage).
- No CONVENTIONS.md exists at the acme-backend repository root.
- Data migration: not expected — the bug is a missing/unread preference, not an incorrect
  persisted value. Re-check if an existing persisted theme column turns out to be written
  with a wrong value.

## Acceptance Criteria
- [ ] A reproducer test sets Dark Mode ON, simulates a new browser session, re-initializes the app, and asserts dark theme and toggle ON — it fails before the fix and passes after
- [ ] Toggling Dark Mode writes the preference to durable storage (survives full browser restart)
- [ ] On application startup the stored preference is applied before first render, and the toggle reflects the stored value
- [ ] Toggling Dark Mode OFF is likewise persisted and restored (light mode after restart)
- [ ] When no preference is stored, the app keeps its current default theme
- [ ] No regression in existing tests

## Test Requirements
- [ ] Reproducer test: set dark mode ON via the toggle path, clear in-memory/session state while keeping durable storage, re-initialize the app; assert theme == dark and toggle == ON (before fix this observes light / OFF)
- [ ] Test that turning dark mode OFF persists across a simulated new session
- [ ] Test that with no stored preference the default theme is applied
- [ ] If server-side persistence is used: test that the user-settings save stores the theme and the load returns it

## Bug Context

- **Bug**: [ACME-511](https://mock-jira.example.com/browse/ACME-511)
- **Steps to Reproduce**: Open the app; go to Settings > Appearance; toggle Dark Mode ON; close the browser completely; reopen and navigate back to the app.
- **Expected Result**: The application should load in dark mode, matching the user's last preference.
- **Actual Result**: The application loads in light mode. The dark mode toggle is reset to OFF.
- **Root Cause**: (Low confidence, not confirmed in code) The dark-mode preference is not durably persisted and/or not restored at startup, so after a browser restart the app falls back to light mode. Affected files were not identified in the investigated repository context.
