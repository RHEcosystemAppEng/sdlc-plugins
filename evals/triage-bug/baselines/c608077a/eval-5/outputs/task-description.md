# Generated Task (Step 5), would be created in project ACME

**Summary:** Fix dark mode preference not persisting across browser sessions (ACME-511)
**Issue type:** Task
**Labels:** `ai-generated-jira`
**Link (Step 5b):** link type `Blocks`, inward = <created Task> (blocker), outward = ACME-511 (blocked)
**Digest (Step 5c):** after creation, re-fetch the description, run `python3 scripts/sha256-digest.py /tmp/desc-<task-key>.txt`, and post `[sdlc-workflow] Description digest: <tagged-digest>` as a standalone comment with no footnote. Not executed in this eval.

---

## Repository
acme-backend

> Note: acme-backend is the only repository in the Registry, so the task targets it. The bug is a browser UI behavior, and the theme toggle and theme initialization code probably live in a frontend repository that is not registered. Before implementing, confirm which repository owns the Settings > Appearance panel. If it is a frontend repo, register it and retarget this task.

## Target Branch
main

## Description
Fixes ACME-511. When a user turns on Dark Mode in Settings > Appearance, closes the browser completely, and reopens the app, the app loads in light mode and the toggle shows OFF. The preference must survive browser restarts: the app should load in the user's last chosen theme. Triage could not confirm the root cause from code. The most likely cause is that the preference is held in session-scoped or in-memory storage, or is saved but never read back during app initialization.

## Files to Modify
- Not yet identified. The investigation found no theme, dark-mode, or user-preferences code in the available repository context. As a first step, locate:
  - the Settings > Appearance Dark Mode toggle and its change handler (where the preference is written)
  - the theme provider / app initialization (where the initial theme is chosen)
  - in acme-backend, any user-preferences endpoint, handler, and model, if preferences are stored on the server

## Implementation Notes
- Fixes ACME-511.
- Investigation starting points: search for `darkMode|dark_mode|theme|colorScheme|appearance|prefers-color-scheme`, and for `localStorage|sessionStorage|document.cookie` near theme code. In acme-backend, search for preference/settings models and handlers (e.g. `Preference`, `UserSettings`, `Theme`).
- Check these hypotheses in order:
  1. The preference is written to `sessionStorage`, a session cookie (no `Expires`/`Max-Age`), or in-memory state only. Fix: write it to durable storage (`localStorage`, a persistent cookie, or the user-preferences API).
  2. The preference is written durably but not read at startup. Fix: read it during theme provider initialization, before the first render, and fall back to `light` only when no stored preference exists.
  3. The backend preferences update is not committed, or the theme field is missing from the read response. Fix the handler or serialization.
- Reproducer guidance (from Steps to Reproduce and Expected/Actual Result):
  - Trigger: set Dark Mode ON through the toggle handler or preferences API, then simulate a new browser session (clear session-scoped storage and in-memory state; keep durable storage or the server-side record), then re-initialize the app or theme provider.
  - Before the fix (Actual Result): active theme is `light` and the toggle is OFF.
  - After the fix (Expected Result): active theme is `dark` and the toggle is ON.
- Base the reproducer on the existing tests for the settings panel, theme provider, or preferences API. None were identified during triage, so find them as part of locating the code.
- Data migration: none expected. The defect appears to be a missing durable write or read, not a wrong persisted value. If a preferences table turns out to hold wrong or defaulted theme values, add a migration that follows the repository's existing migration conventions.
- CONVENTIONS.md: none at the acme-backend root.
- Keep this fix separate from ACME-500 (the CONVENTIONS.md heading-whitespace bug in `plugins/sdlc-workflow/skills/plan-feature/SKILL.md`). It is unrelated.

## Acceptance Criteria
- [ ] A reproducer test enables Dark Mode, simulates a new browser session (session/in-memory state cleared, durable storage kept), re-initializes the app, and asserts the theme is `dark` and the toggle is ON. It fails before the fix and passes after.
- [ ] Toggling Dark Mode writes the preference to durable storage that survives a browser restart.
- [ ] On app load, the stored theme preference is read and applied before the first render. Light mode is used only when no preference has been stored.
- [ ] Turning Dark Mode OFF also persists (after a restart, the app loads in light mode and the toggle shows OFF).
- [ ] No regressions in existing tests.

## Test Requirements
- [ ] Reproducer test: set Dark Mode ON, clear session-scoped and in-memory state while keeping durable storage or the server-side record, re-initialize the app/theme provider, and assert `theme === "dark"` and the toggle is ON. Before the fix it should observe `light`/OFF (Actual Result); after the fix, `dark`/ON (Expected Result).
- [ ] Test that with no stored preference, the app defaults to light mode.
- [ ] Test that switching back to light mode persists across a simulated session restart.
- [ ] If preferences are server-side: an API test that updates the theme preference, fetches it with a fresh session, and asserts the stored value comes back.

## Bug Context

- **Bug**: [ACME-511](https://mock-jira.example.com/browse/ACME-511)
- **Steps to Reproduce**: Open the app → Settings > Appearance → toggle Dark Mode ON → close the browser completely → reopen the browser and go back to the app.
- **Expected Result**: The application should load in dark mode, matching the user's last preference.
- **Actual Result**: The application loads in light mode. The dark mode toggle is reset to OFF.
- **Root Cause**: Not confirmed from code (low confidence). Most likely the dark mode preference is stored in session-scoped or in-memory state, or is saved but not read back during app initialization, so the theme falls back to the light default after a browser restart. The affected files could not be identified: no frontend repository is registered, and the provided context had no theme or preferences code.
- **Affects Version**: Not determined. The reporter wrote "Not sure which version — using whatever is deployed on staging". A gap comment was posted asking for it to be set manually.
