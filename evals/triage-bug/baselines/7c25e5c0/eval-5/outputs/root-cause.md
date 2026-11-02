# Step 4 -- Root Cause Analysis

## Root Cause

The dark mode user preference is not persisted to durable browser storage (such as `localStorage`) when toggled. The most likely root cause is one of:

1. **Primary hypothesis -- `sessionStorage` instead of `localStorage`**: The theme preference is being written to `sessionStorage`, which is cleared when the browser session ends. When the user closes and reopens the browser, the stored preference is lost, and the application falls back to the default light mode theme.

2. **Alternative hypothesis -- No persistence at all**: The dark mode toggle updates only in-memory application state (e.g., a component state variable or global store) without writing to any persistent storage. On page reload or new session, the state initializes to the default (light mode).

## Impact

- **User impact**: Every user who enables dark mode must re-enable it each time they open the application. This degrades the user experience, especially for users who prefer dark mode for accessibility or comfort reasons.
- **Scope**: Affects all users of the application who use the dark mode feature.
- **Severity**: Low-to-medium -- functionality exists but does not persist, causing repeated manual action.

## Suggested Fix

1. Ensure the dark mode preference is written to `localStorage` (not `sessionStorage`) when the toggle is changed.
2. On application initialization, read the stored preference from `localStorage` and apply the corresponding theme before the first render.
3. Add a test that verifies the preference survives a simulated session restart (clear in-memory state, reinitialize, assert dark mode is still active).
