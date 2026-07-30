# Root Cause Analysis -- ACME-511 (Step 4)

## Summary

The dark mode preference is stored only in React in-memory state (via `ThemeContext`)
and is never written to a durable browser storage mechanism (e.g., `localStorage`).
Because the context re-initializes from a hardcoded default (`false`) on every page
load, the user's toggle preference is lost whenever the browser session ends.

## Root Cause

**What is broken**: The dark mode toggle updates in-memory React context state but
does not persist the preference to `localStorage` (or any other durable store).
Additionally, the `ThemeContext` initializer reads from a hardcoded default (`false`)
rather than from a previously persisted value, so no stored preference can be
recovered at startup.

**Why it is broken**: The `handleToggle` handler in `AppearancePanel.tsx` calls
`setDarkMode(checked)` to update the context, but lacks a corresponding
`localStorage.setItem('theme', checked ? 'dark' : 'light')` call. The `ThemeContext`'s
`useState` initializer uses `false` as the default instead of
`localStorage.getItem('theme') === 'dark'`. These two omissions together mean:

1. The preference is never durably written when the user toggles.
2. Even if a value were somehow in `localStorage`, the context would not read it.

**Where it is broken**:

| File | Symbol | Specific Gap |
|------|--------|--------------|
| `src/context/ThemeContext.tsx` | `useState` initializer | Reads hardcoded `false` instead of `localStorage` value |
| `src/components/settings/AppearancePanel.tsx` | `handleToggle` | Does not call `localStorage.setItem` after updating context |

**Persistence impact**: None -- this is a client-side only preference. No database
records are written and no data migration is required.

## Affected Files

- `src/context/ThemeContext.tsx` -- primary fix location (initializer + sync effect)
- `src/components/settings/AppearancePanel.tsx` -- secondary fix location (write on toggle)
- `src/components/settings/__tests__/AppearancePanel.test.tsx` -- location for reproducer test

## Suggested Approach (without writing code)

1. In `ThemeContext.tsx`, change the `useState` initializer to read from
   `localStorage.getItem('theme')` (defaulting to `'light'` if absent).
2. Add a `useEffect` (or inline write in the setter) that calls
   `localStorage.setItem('theme', ...)` whenever `isDarkMode` changes.
3. Alternatively, consolidate both the read and the write into the `handleToggle`
   handler in `AppearancePanel.tsx` and the context initializer -- whichever pattern
   is more consistent with the existing codebase style.

## Reproducer Strategy

A reproducer test should:

1. Render the application (or `ThemeProvider` + `AppearancePanel` in isolation).
2. Simulate toggling dark mode ON (the toggle interaction or direct context call).
3. Simulate a page reload by unmounting and remounting the component tree (clearing
   in-memory React state while preserving any `localStorage` writes).
4. Assert that after remount, the app is in dark mode (context value `isDarkMode === true`
   and the toggle appears ON).

This test should **fail before the fix** (no `localStorage` write) and **pass after**
(preference read from `localStorage` on reinitialize).

---

*This root cause analysis would be posted as a comment on ACME-511 via `jira.add_comment`
in a live execution. The comment would include the ADF footnote for `sdlc-workflow/triage-bug`.*
