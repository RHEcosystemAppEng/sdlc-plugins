# Step 4 – Root Cause Analysis: ACME-511

## Confidence

**Low. The code-level root cause is not confirmed.** The available repository context has no code related to theme or dark-mode persistence (see `investigation.md`). The analysis below is limited to what the bug report supports. Candidate causes are labelled as hypotheses, not findings.

## 1. What is broken

The user's dark-mode preference does not survive a full browser restart. After a restart the app falls back to the default light theme, and the Settings > Appearance toggle shows OFF.

## 2. Why it is broken (hypotheses, ranked)

The toggle works within a session, and the Steps to Reproduce only fail after the browser is closed completely. So the preference is either kept only in session-scoped state or never read back at startup. Candidate causes:

1. **Session-scoped storage**: the preference is written to `sessionStorage`, in-memory app state, or a session cookie with no `Expires`/`Max-Age`. All of these are cleared when the browser closes. This hypothesis fits the "close the browser completely" step best.
2. **Write never persisted**: the toggle handler updates the UI theme but never calls the save routine, whether that is local storage or a user-preferences API call on acme-backend.
3. **Read path missing or overridden at bootstrap**: the preference is saved, but theme initialization never reads it, or it applies a hard-coded light default (or the OS `prefers-color-scheme` value) after the saved value loads.
4. **Backend preference not saved/returned** (only if preferences live server-side in acme-backend): the preferences endpoint drops the theme field on write or leaves it out of the read response.

## 3. Where it is broken

**Not determined.** No affected files or symbols were found. The registered repository (acme-backend, a Rust backend) is unlikely to hold the Settings UI. The provided context covers an unrelated bug (ACME-500, CONVENTIONS.md heading whitespace in `plugins/sdlc-workflow/skills/plan-feature/SKILL.md`). That code is **not** the cause of ACME-511 and is deliberately left out of this analysis.

Where to look next:
- The theme toggle change handler in the Settings > Appearance component.
- App bootstrap and theme provider initialization.
- Any client storage helper wrapping `localStorage`, `sessionStorage`, or cookies.
- If preferences are stored server-side, the acme-backend user-preferences handler and its model.

## 4. How to verify the fix (reproducer strategy)

- **Scenario**: set the dark-mode preference to ON through the same code path as the Settings toggle, then simulate a new browser session. That means clearing in-memory state and `sessionStorage` and dropping session-only cookies while keeping persistent storage. Then re-initialize the app or theme provider.
- **Before the fix (reflects the Actual Result)**: the resolved theme is `light` and the toggle state is OFF.
- **After the fix (reflects the Expected Result)**: the resolved theme is `dark` and the toggle state is ON.
- **Additional check**: with no saved preference, the app still defaults to light mode (no regression for new users).

## Persistence impact

No database-persisted wrong values are expected. The bug is about a value that is missing, not one that is incorrect, so no data migration is recommended (still to be confirmed once the write path is found).

## Decomposition

This is a single root cause on the preference save/restore path. Step 6 is not triggered.

---

## Jira comment that would be posted on ACME-511 (not executed in this eval)

`jira.add_comment("ACME-511", <ADF>)`. The content is rendered here as markdown and would be sent as ADF with the footnote nodes appended:

> **Root Cause**
> The dark-mode preference does not survive a full browser restart. The code-level cause is **not yet confirmed**: the available codebase context (registry entry acme-backend, a Rust backend service) has no Settings/theme code. The most likely cause is that the preference is kept only in session-scoped state (sessionStorage, in-memory state, or a session cookie with no expiry) or is not read back during app bootstrap. Other possibilities: the toggle never saves the value, or a backend preferences endpoint drops the theme field.
>
> **Affected Files**
> Not identified. The frontend repository with the Settings > Appearance UI and theme bootstrap is not registered in the project's Repository Registry. Please add it so the investigation can be completed.
>
> **Suggested Approach**
> Save the theme preference to durable storage (localStorage, a persistent cookie, or the user-preferences API) when the toggle changes. Read it during app initialization before the first render. Keep light mode as the default only when no saved value exists.
>
> **Reproducer Strategy**
> Set dark mode ON through the toggle code path, simulate a new browser session (clear session-scoped state, keep persistent storage), re-initialize the theme, and assert the theme is `dark` and the toggle is ON. Before the fix this resolves to `light`/OFF.
>
> ---
> This comment was AI-generated by [sdlc-workflow/triage-bug](https://github.com/RHEcosystemAppEng/sdlc-plugins) v0.13.10.
