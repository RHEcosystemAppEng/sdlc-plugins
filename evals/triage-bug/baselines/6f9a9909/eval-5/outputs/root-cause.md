# Root Cause Analysis: ACME-511

## Bug

Dark mode toggle does not persist across browser sessions.

## Root Cause Summary

The user's dark mode preference is not persisted to a storage mechanism that survives browser session closure. When the user toggles dark mode ON, the preference is applied to the current session's UI state but is either:

1. **Not written to persistent storage at all** — the toggle handler updates in-memory/component state without a corresponding write to localStorage or a backend user-preferences API, or
2. **Written to sessionStorage instead of localStorage** — sessionStorage is scoped to the browser tab/session and is cleared when the browser is closed, so the preference is lost.

On application reload, the initialization code finds no persisted preference (or reads from the wrong key) and falls back to the default theme, which is light mode.

## Impact

- Every user who enables dark mode will have their preference reset each time they close and reopen the browser.
- This is a user-facing regression in preference persistence, impacting user experience.

## Suggested Fix Direction

1. Ensure the dark mode toggle handler writes the preference to `localStorage` (or a server-side user preferences store) rather than `sessionStorage` or in-memory state only.
2. Ensure the application initialization reads the persisted preference from the same storage location and applies it before first render.
3. Add a test that verifies the preference value is written to persistent storage when the toggle is changed, and that it is read back correctly on initialization.

## Confidence

Medium — the root cause is inferred from the bug symptoms (preference lost on browser close) and common patterns for this class of bug. No code intelligence was available to confirm the exact storage mechanism in use.
