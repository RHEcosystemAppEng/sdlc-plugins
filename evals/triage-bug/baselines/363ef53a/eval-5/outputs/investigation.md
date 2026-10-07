# Codebase Investigation

**Bug**: ACME-511 -- Dark mode toggle does not persist across browser sessions
**Repository**: acme-backend

## Investigation Summary

The bug reports that enabling dark mode via Settings > Appearance does not persist
across browser sessions. When the user closes and reopens the browser, the application
reverts to light mode and the toggle resets to OFF.

This indicates a failure in the preference persistence mechanism. The user's dark mode
setting is either:

1. Not being saved to persistent storage (e.g., localStorage, a cookie, or a backend
   user-preferences endpoint) when toggled, or
2. Being saved but not read back on application initialization, or
3. Being stored in session-scoped storage (e.g., sessionStorage) that is cleared when
   the browser closes.

## Relevant Code Paths

Based on the repository context and the nature of this bug, the investigation would
target the following areas:

### Settings / Appearance UI

The component handling the dark mode toggle in the Settings > Appearance panel. This is
where the toggle event fires and should trigger a write to persistent storage.

### Preference Persistence Layer

The mechanism responsible for storing user preferences. A common pattern is to use
`localStorage` for client-side persistence or a backend API endpoint (e.g.,
`PUT /api/user/preferences`) for server-side persistence. If `sessionStorage` is used
instead of `localStorage`, preferences would not survive a browser close.

### Application Initialization

The startup logic that reads the persisted preference and applies it before or during
the initial render. If this read is missing or reads from the wrong storage key, the
application would default to light mode.

## Findings

The repository context available (repo-context-mock.md) describes code paths related to
the plan-feature skill's convention conformance analysis, which involves heading
extraction and trailing whitespace in CONVENTIONS.md parsing. This context is relevant
to ACME-500 (a different bug) rather than ACME-511.

No Serena MCP servers are configured for code intelligence, so deep code search across
the repository is not available.

**Conclusion**: The root cause is most likely in the preference persistence layer --
either the dark mode preference is written to session-scoped storage instead of
persistent storage, or the initialization code does not read the stored preference on
app load. A targeted investigation of the settings component and its storage calls
would confirm which scenario applies.
