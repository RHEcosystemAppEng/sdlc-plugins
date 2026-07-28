## Repository
acme-backend

## Target Branch
main

## Description
Persist the user's dark mode preference to `localStorage` so it survives full browser
close and reopen. Currently the `ThemeContext` initializes from a hardcoded default
(`false`) and the toggle handler never writes to durable storage, so the preference
is lost on every new browser session. This task adds the read-on-init and write-on-change
calls to `localStorage`, and adds a reproducer test that confirms the preference survives
a simulated page reload.

Fixes ACME-511.

## Files to Modify
- `src/context/ThemeContext.tsx` — change `useState` initializer to read from
  `localStorage.getItem('theme')` and add a write (via `useEffect` or inline setter)
  whenever `isDarkMode` changes
- `src/components/settings/AppearancePanel.tsx` — confirm `handleToggle` triggers the
  context update that reaches the persistence write; add direct `localStorage.setItem`
  call here if the context-level fix is not sufficient
- `src/components/settings/__tests__/AppearancePanel.test.tsx` — add reproducer test
  covering the persist-and-reload scenario

## Implementation Notes

### Root Cause Recap (Fixes ACME-511)

The `ThemeContext` in `src/context/ThemeContext.tsx` initializes `isDarkMode` from a
hardcoded `false` default instead of reading from `localStorage`. The `handleToggle`
handler in `AppearancePanel.tsx` calls `setDarkMode(checked)` (updating React context
only) without a corresponding `localStorage.setItem('theme', checked ? 'dark' : 'light')`.
These two omissions together mean: (1) the preference is never durably written, and
(2) even if it were, it would not be read back on startup.

### Fix Guidance

**In `src/context/ThemeContext.tsx`**:
- Change the `useState` initializer from `useState(false)` to
  `useState(() => localStorage.getItem('theme') === 'dark')` so the preference is
  restored on every mount.
- Add a `useEffect(() => { localStorage.setItem('theme', isDarkMode ? 'dark' : 'light'); }, [isDarkMode])`
  to sync any future changes to `localStorage`. This keeps the write logic in the context
  layer, co-located with state ownership.

**In `src/components/settings/AppearancePanel.tsx`**:
- Verify that `handleToggle` calls `setDarkMode(checked)` which feeds the `useEffect`
  above. No additional change needed if the context-level write is in place.
- If the project pattern is to write from the handler rather than a `useEffect`, add
  `localStorage.setItem('theme', checked ? 'dark' : 'light')` directly in `handleToggle`.

### Reproducer Test Guidance

Extend `src/components/settings/__tests__/AppearancePanel.test.tsx`:

1. Before the fix, assert the bug: render with `localStorage` cleared, toggle dark mode
   ON, then unmount and remount (simulating a page reload by discarding React state
   while keeping any `localStorage` writes). Assert that after remount, `isDarkMode`
   is `false` (the broken state — preference lost).
2. After the fix, the same sequence should result in `isDarkMode === true` after remount.

Useful test utilities already in the repo:
- Mock `localStorage` with `vi.spyOn(window.localStorage, 'setItem')` /
  `vi.spyOn(window.localStorage, 'getItem')` or a `jest-localstorage-mock` setup —
  check the existing test setup in `AppearancePanel.test.tsx` for the mocking pattern.
- Unmount/remount the `ThemeProvider` subtree to simulate a page reload (all React
  state is re-initialized; only external stores like `localStorage` persist).

### No CONVENTIONS.md

The `acme-backend` repository does not contain a `CONVENTIONS.md` at its root.
Follow the patterns observed in the existing test file `AppearancePanel.test.tsx`
for assertion style, describe/it block naming, and import conventions.

### No Data Migration Required

The dark mode preference is a client-side UI preference and is not persisted to
any database. Only `localStorage` is involved. No data migration is needed.

## Reuse Candidates
- `src/context/ThemeContext.tsx::ThemeContext` — the existing context is the primary
  fix target; the initializer and setter are the two touch points
- `src/components/settings/__tests__/AppearancePanel.test.tsx` — extend the existing
  test file rather than creating a new one; the render setup and mocks are already present

## Acceptance Criteria
- [ ] **Reproducer test**: a test exists that (a) toggles dark mode ON, (b) simulates
  a page reload by unmounting and remounting `ThemeProvider`, and (c) asserts the app
  initializes in dark mode after the reload — this test must fail before the fix and
  pass after
- [ ] Toggling dark mode ON and performing a full browser close/reopen (or equivalent
  hard refresh) results in the application loading in dark mode
- [ ] Toggling dark mode OFF and reloading results in the application loading in
  light mode (the reset case also works correctly)
- [ ] The dark mode toggle in Settings > Appearance reflects the persisted preference
  on load (toggle appears ON when dark mode was previously enabled)
- [ ] No regression in existing `AppearancePanel` tests

## Test Requirements
- [ ] **Reproducer test** (first): mount `ThemeProvider` + `AppearancePanel`, toggle
  dark mode ON, unmount, remount (clearing React state but not `localStorage`), assert
  `isDarkMode === true` — this test must fail before the fix and pass after
- [ ] Test that toggling dark mode OFF after it was ON is also persisted correctly
  (regression of the opposite state)
- [ ] Test that the initial state when no `localStorage` entry exists defaults to
  light mode (`isDarkMode === false`)
- [ ] Confirm `localStorage.setItem` is called with `'theme'` and `'dark'` when
  dark mode is toggled ON (spy assertion)

## Verification Commands
- `npm test src/components/settings/__tests__/AppearancePanel.test.tsx` — all tests
  including the new reproducer test should pass
- `npm run build` — build must succeed without TypeScript errors

## Bug Context

- **Bug**: [ACME-511](https://mock-jira.example.com/browse/ACME-511)
- **Steps to Reproduce**:
  1. Open the application in a browser.
  2. Navigate to Settings > Appearance.
  3. Toggle "Dark Mode" to ON.
  4. Close the browser completely.
  5. Reopen the browser and navigate back to the application.
- **Expected Result**: The application should load in dark mode, matching the user's
  last preference.
- **Actual Result**: The application loads in light mode. The dark mode toggle is
  reset to OFF.
- **Root Cause**: `ThemeContext` initializes `isDarkMode` from a hardcoded `false`
  default (not from `localStorage`), and `AppearancePanel.handleToggle` updates only
  the in-memory React context without writing to `localStorage`. The preference is
  therefore never durably stored and is lost on every browser session end.
