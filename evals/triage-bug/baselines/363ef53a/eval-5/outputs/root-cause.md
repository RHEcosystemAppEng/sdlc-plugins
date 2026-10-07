# Root Cause Analysis

**Bug**: ACME-511 -- Dark mode toggle does not persist across browser sessions

## Summary

The dark mode preference does not survive browser restarts. The user toggles dark mode
ON, closes the browser, reopens it, and the application loads in light mode with the
toggle reset to OFF.

## Root Cause

The most probable root cause is that the dark mode preference is either:

1. **Stored in session-scoped storage**: The preference is written to `sessionStorage`
   (or an equivalent session-scoped mechanism) rather than `localStorage` or a backend
   persistence layer. `sessionStorage` is cleared when the browser tab/window is closed,
   which matches the reported behavior exactly.

2. **Not persisted at all**: The toggle updates in-memory application state (e.g., a
   React context or Redux store) but never triggers a write to any persistent storage.
   On reload, the state initializes to the default (light mode).

A secondary possibility is that the preference IS written to `localStorage` but the
application initialization code does not read it back, defaulting to light mode on
every fresh load.

## Confidence

Medium -- without code intelligence (no Serena instances configured), the exact storage
mechanism cannot be confirmed. The behavioral evidence strongly points to a persistence
gap rather than a read-back issue, since the toggle also resets to OFF (suggesting the
stored value is lost, not just unread).

## Affected Area

- Settings / Appearance UI component (toggle handler)
- Preference persistence layer (storage writes)
- Application initialization (storage reads and theme application)
