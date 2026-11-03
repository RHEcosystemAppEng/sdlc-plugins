# Step 5 – Generated Task (simulated `jira.create_issue`)

**Project**: ACME
**Issue Type**: Task
**Summary**: Persist dark mode preference across browser sessions (fixes ACME-511)
**Labels**: `ai-generated-jira`
**Link (Step 5b)**: link type `Blocks`. Inward = <created-task-key> (blocks), outward = ACME-511 (is blocked by)
**Digest (Step 5c)**: after creation, re-fetch the description, run `python3 scripts/sha256-digest.py`, and post `[sdlc-workflow] Description digest: <tagged-digest>` as a standalone comment (no footnote)

---

## Repository
acme-backend

## Target Branch
main

## Description
Fixes ACME-511. A user's dark mode preference, set under Settings > Appearance, is lost when
the browser is fully closed and reopened. The app falls back to light mode and the toggle
resets to OFF. This task makes the theme preference persist across browser sessions and
restores it when the app starts. A reproducer test proves the bug and guards against regression.

Note: triage could not find the theme or preference code in the registered repository
(acme-backend, a Rust backend service). Before implementing, confirm which repository owns
the Settings > Appearance UI. If it is a separate frontend repository, re-target this task
(and add that repository to the Repository Registry).

## Files to Modify
- Not determined during triage. The available repository context had no files related to
  theme or preference handling. The implementer must find:
  - the Settings > Appearance "Dark Mode" toggle handler, and
  - the app's theme initialization/bootstrap logic,
  - and, if preferences are stored per user on the server, the user-preferences
    endpoint/model in acme-backend.

## Implementation Notes
- **Traceability**: Fixes ACME-511.
- **Trigger scenario**: open the app -> Settings > Appearance -> turn "Dark Mode" ON -> close
  the browser completely -> reopen and go back to the app.
- **Incorrect behavior (Actual Result), which the reproducer should first show failing**:
  the app loads in light mode and the Dark Mode toggle is OFF.
- **Correct behavior (Expected Result), which the reproducer asserts after the fix**: the app
  loads in dark mode and the toggle is ON, matching the user's last choice.
- **Likely root cause (unconfirmed)**: the preference lives only in memory or `sessionStorage`
  (cleared on browser close), or it is saved but never read back before the default theme is
  applied at startup.
- **Fix direction**:
  1. When the toggle changes, write the preference to durable storage: `localStorage` or a
     long-lived cookie for a client-only preference, or a per-user backend preference if
     settings should follow the user across devices.
  2. During app initialization, read the saved preference and apply it **before the first
     render** to avoid a light-mode flash. Use light only when no saved value exists.
  3. Keep the toggle's displayed state in sync with the restored preference.
- **Patterns/conventions**: no existing patterns, reusable utilities or test files were found
  for this area during triage, and there is no CONVENTIONS.md at the repository root. Follow
  the repository's existing state-management and storage patterns once the owning code is found.
- **Data migration**: not needed. No incorrect values were persisted earlier.

## Acceptance Criteria
- [ ] A reproducer test turns dark mode ON, simulates a new browser session (clears in-memory
      state and `sessionStorage` but keeps durable storage), re-initializes the app and
      asserts dark mode is active and the toggle is ON. The test fails before the fix and
      passes after.
- [ ] Turning Dark Mode ON or OFF saves the preference to storage that survives a full browser restart.
- [ ] On startup the saved theme preference is applied before the first render; light mode is
      the default only when no preference is saved.
- [ ] The Dark Mode toggle state matches the restored preference after a restart.
- [ ] No regression in existing tests.

## Test Requirements
- [ ] Reproducer test (first): with empty storage, assert the default is light; turn Dark Mode
      ON; simulate a browser restart (reset app state and `sessionStorage`, keep
      `localStorage`/cookies/backend preference); re-initialize; assert the theme is dark and
      the toggle is ON. Before the fix this assertion fails (the app shows light/OFF, matching
      the Actual Result in ACME-511).
- [ ] Test that turning Dark Mode back OFF and restarting restores light mode, so the
      preference round-trips both ways.
- [ ] Test that with no saved preference, the app starts in light mode.
- [ ] If server-side persistence is used: an API test that the theme preference is stored and
      returned for the authenticated user.

## Bug Context

- **Bug**: [ACME-511](https://mock-jira.example.com/browse/ACME-511)
- **Steps to Reproduce**: Open the app -> Settings > Appearance -> turn "Dark Mode" ON -> close the browser completely -> reopen and go back to the app.
- **Expected Result**: The application should load in dark mode, matching the user's last preference.
- **Actual Result**: The application loads in light mode. The dark mode toggle is reset to OFF.
- **Root Cause**: Not confirmed in code (no theme/preference code in the available repository context). Most likely the dark mode preference is held only in memory or `sessionStorage`, or is not restored at startup, so the default light theme is applied after a browser restart.
- **Affects Version**: Could not be determined. The Environment / Version section says "Not sure which version — using whatever is deployed on staging". A gap comment was posted on ACME-511 asking for it to be set manually.

---

## Step 7 – Report (simulated)

- Created Task: `<created-task-key>` (simulated), linked as **Blocks** -> ACME-511.
- Root cause: the dark mode preference is not kept across sessions (likely session-only
  storage or no restore at startup). Low confidence, because the theme code was not found in
  the registered repository.
- Reproducer strategy: toggle dark mode, simulate a browser restart while keeping durable
  storage, and assert dark mode and toggle ON.
- Affects Version: not set. A gap comment was posted.
- Next step: run `/implement-task <created-task-key>` to implement the fix.
