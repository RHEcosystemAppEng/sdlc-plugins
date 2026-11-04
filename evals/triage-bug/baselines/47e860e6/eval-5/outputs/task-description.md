# Step 5 – Generated Task for ACME-511

## Jira create_issue parameters (not executed in this eval)

| Field | Value |
|---|---|
| Project | ACME |
| Issue type | Task |
| Summary | Persist dark mode preference across browser sessions (fixes ACME-511) |
| Labels | `ai-generated-jira` |
| Description | Below |

> Triage note: the code-level root cause could not be confirmed. The registered repository context has no theme or settings code (see `investigation.md`). The file paths below are therefore not listed as discovered paths. They are left for the implementer to locate. Before running `/implement-task`, a human should confirm the repository and, if needed, register the frontend repository.

---

## Repository
acme-backend

(This is the only repository in the Repository Registry. If the Settings > Appearance UI lives in a separate frontend repository, re-target this task to that repository once it is registered.)

## Target Branch
main

## Description
Fixes ACME-511. When a user turns on dark mode in Settings > Appearance and then fully closes and reopens the browser, the application loads in light mode and the toggle shows OFF. The user's theme preference must be saved durably and restored at application start, so the app loads in the theme the user last chose.

## Files to Modify
No affected files were found during triage. The provided repository context has no theme or settings code, and the repository source was not accessible. The implementer must locate:
- The Settings > Appearance dark-mode toggle change handler, to save the preference durably.
- The app bootstrap / theme initialization code, to read the saved preference before the first render.
- The storage layer used for the preference. This is either a client storage helper (localStorage, sessionStorage, or cookie) or, if preferences are server-side, the acme-backend user-preferences handler and model.

## Implementation Notes
- Fixes ACME-511.
- **Likely cause to check first**: the preference is stored only in session-scoped state (`sessionStorage`, in-memory store, or a cookie with no `Expires`/`Max-Age`), so it is cleared when the browser closes. Also check whether the toggle handler ever calls a save routine, and whether bootstrap reads the stored value or overwrites it with a hard-coded `light` default or the OS `prefers-color-scheme`.
- **Fix direction**: on toggle change, write the preference to durable storage. Use the mechanism the app already uses for other user settings, such as `localStorage`, a persistent cookie, or the user-preferences API. On app init, read the saved value before the first render and apply it. Fall back to light mode only when nothing is saved.
- If preferences are stored server-side in acme-backend, make sure the theme field is both saved on update and returned on read by the preferences endpoint.
- **Reproducer guidance** (from the Steps to Reproduce):
  - Trigger: set dark mode ON through the same code path as the Settings toggle, then simulate a fresh browser session. Clear in-memory state, `sessionStorage`, and session-only cookies, keep persistent storage, and re-initialize the app or theme provider.
  - Before the fix (Actual Result): the resolved theme is `light` and the toggle is OFF.
  - After the fix (Expected Result): the resolved theme is `dark` and the toggle is ON.
- No existing test files or assertion patterns for theme or settings persistence were found during triage. Follow the test framework and file layout already used in the repository that holds the Settings UI.
- No CONVENTIONS.md exists at the repository root.
- Persistence impact: no wrongly persisted database values are expected (the preference is missing, not incorrect), so no data migration is needed. If the preference turns out to be written server-side with an incorrect value, revisit this.

## Acceptance Criteria
- [ ] A reproducer test sets dark mode ON, simulates a new browser session, and asserts the app restores dark mode. The test fails before the fix (resolves to light/OFF) and passes after it (resolves to dark/ON).
- [ ] Toggling dark mode in Settings > Appearance saves the preference to storage that survives a full browser restart.
- [ ] On application start, the saved theme preference is read and applied before the first render, and the toggle reflects the saved state.
- [ ] With no saved preference, the application still defaults to light mode.
- [ ] Turning dark mode OFF is also saved and restored (the app loads in light mode after a restart).
- [ ] No regressions in existing tests.

## Test Requirements
- [ ] Reproducer test (first): set the dark-mode preference ON through the toggle's code path, clear session-scoped state (in-memory store, `sessionStorage`, session cookies) while keeping persistent storage, and re-initialize the theme or app. Assert theme == `dark` and toggle == ON. Confirm this assertion fails against the current code (which yields `light`/OFF).
- [ ] Test that with no saved preference, initialization yields theme == `light` and toggle == OFF.
- [ ] Test that setting dark mode OFF after ON is saved, so that after a simulated session restart theme == `light`.
- [ ] If preferences are stored server-side: a backend test that updating the user preferences with theme `dark` and then reading them returns theme `dark`.

## Bug Context

- **Bug**: [ACME-511](https://mock-jira.example.com/browse/ACME-511)
- **Steps to Reproduce**: Open the app → Settings > Appearance → toggle "Dark Mode" ON → close the browser completely → reopen and navigate back to the app.
- **Expected Result**: The application should load in dark mode, matching the user's last preference.
- **Actual Result**: The application loads in light mode. The dark mode toggle is reset to OFF.
- **Root Cause**: Not confirmed at code level. The dark-mode preference does not survive a browser restart. Most likely it is held only in session-scoped state, or it is not read back during app bootstrap. No affected files were found in the available repository context. Affects Version is unknown (the reporter gave no version, and a gap comment was posted).

---

## Step 5b – Link Task to Bug (not executed)

```
jira.create_issue_link(
  link_type="Blocks",
  inward_issue_key=<created-task-key>,   # Task (blocker)
  outward_issue_key="ACME-511"           # Bug (blocked)
)
```

## Step 5c – Digest comment (not executed)

After creation, the skill would re-fetch the task, write its description to `/tmp/desc-<task-key>.txt`, run `python3 scripts/sha256-digest.py /tmp/desc-<task-key>.txt`, and post a standalone comment `[sdlc-workflow] Description digest: <tagged-digest>` with no footnote.

## Step 6 – Decomposition Guard

Not triggered. There is one symptom and one root cause on the preference save/restore path.

## Step 7 – Report

- Task: `<created-task-key>` (would be linked as blocking ACME-511)
- Root cause summary: the dark-mode preference does not survive a browser restart. The likely cause is session-scoped storage or a missing read at bootstrap. This is unconfirmed because no theme or settings code was available in the registered repository context.
- Reproducer strategy: set dark ON, simulate a new session that keeps persistent storage, and assert dark/ON is restored.
- Follow-ups for a human: (1) set Affects Version manually on ACME-511; (2) confirm or register the frontend repository that holds the Settings UI.
- Next step: "Run `/implement-task <task-key>` to implement the fix."
