# Steps 2-3 -- Codebase Investigation

## Bug Summary

ACME-511 reports that the dark mode toggle in Settings > Appearance does not persist across browser sessions. When a user enables dark mode, closes the browser, and reopens it, the application reverts to light mode.

## Investigation Findings

### Likely Affected Areas

Based on the bug description, the dark mode persistence issue involves:

1. **Settings / Appearance UI component** -- The toggle that sets the dark mode preference. This component likely dispatches a state change but may not trigger persistence to durable storage.

2. **Theme persistence layer** -- The mechanism responsible for saving the user's theme preference. Common approaches include:
   - `localStorage` or `sessionStorage` in the browser
   - A user preferences API endpoint (server-side persistence)
   - Cookie-based storage

3. **Application initialization / theme hydration** -- The startup code that reads the persisted theme preference and applies it before rendering. If this code does not check the persistence layer (or checks the wrong key), the default light mode would be applied.

### Hypotheses

1. **`sessionStorage` used instead of `localStorage`**: If the preference is stored in `sessionStorage`, it would be cleared when the browser is closed, explaining the observed behavior exactly. `sessionStorage` is scoped to the browser tab/session, while `localStorage` persists across sessions.

2. **Preference not written at all**: The toggle may update in-memory state (e.g., a React/Redux store) without persisting to any storage mechanism.

3. **Initialization does not read stored preference**: The app startup may not check for a previously stored preference, always defaulting to light mode.

4. **Storage key mismatch**: The write path may use a different key (e.g., `darkMode`) than the read path (e.g., `theme-preference`), causing the stored value to be ignored on reload.

### Files Likely Involved

Without Serena code intelligence available, the following file patterns would be investigated:

- `src/components/settings/Appearance.*` -- Settings panel UI
- `src/theme/*` or `src/hooks/useTheme.*` -- Theme management
- `src/utils/storage.*` or `src/services/preferences.*` -- Persistence utilities
- `src/App.*` or `src/index.*` -- Application initialization and theme hydration
