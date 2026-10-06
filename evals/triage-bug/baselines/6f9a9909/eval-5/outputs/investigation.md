# Codebase Investigation: ACME-511

## Bug Summary

Dark mode toggle does not persist across browser sessions. When a user enables dark mode and closes the browser, the preference is lost and the application reverts to light mode on next visit.

## Investigation Scope

Repository: acme-backend

## Findings

### Preference Persistence Mechanism

The bug describes a client-side user preference (dark mode) that is not surviving browser session boundaries. This indicates the preference is likely stored in a transient storage mechanism (such as in-memory state or sessionStorage) rather than a persistent one (such as localStorage, a cookie with appropriate expiry, or server-side storage).

Key areas to investigate:
- **Settings/Appearance UI component**: The component handling the dark mode toggle in Settings > Appearance. This is where the toggle state change is initiated and should trigger persistence.
- **Theme/preference storage layer**: The mechanism used to read and write the user's theme preference. If this uses sessionStorage or in-memory state only, the preference will be lost when the browser is closed.
- **Application initialization**: The startup code that reads the persisted preference and applies the theme. If the read path is missing or reads from the wrong storage key, the default (light mode) will be applied.

### Available Repository Context

The mock repository context provided (`repo-context-mock.md`) documents code paths in `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` related to convention heading extraction with trailing whitespace. This does not directly relate to the dark mode persistence bug but is part of the broader acme-backend codebase.

No Serena code intelligence is configured for this repository, so symbol-level search was not available.

### Likely Root Cause Areas

1. **Storage mechanism**: The dark mode preference may be stored using `sessionStorage` (which is cleared when the browser closes) instead of `localStorage` (which persists across sessions).
2. **Missing persistence call**: The toggle handler may update the UI state but fail to write the preference to persistent storage.
3. **Initialization logic**: The application may not read the stored preference on startup, defaulting to light mode.

## Files to Investigate

Without code intelligence available, the following file patterns would need manual investigation:
- Settings/Appearance component (toggle handler and persistence call)
- Theme provider or context (where the current theme state is managed)
- Application entry point (where stored preferences are loaded on startup)
