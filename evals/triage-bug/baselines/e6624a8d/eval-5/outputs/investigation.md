# Codebase Investigation -- ACME-511 (Step 3)

## Target Repository

- **Repository**: acme-backend
- **Serena Instance**: serena_backend
- **Path**: /home/dev/repos/acme-backend

## Code Intelligence Availability

Per the project's CLAUDE.md `## Code Intelligence` section:

> "No Serena MCP servers are configured. Code intelligence is not available."

Falling back to **Read, Grep, and Glob** tools for investigation.

## CONVENTIONS.md Check

Checked for `CONVENTIONS.md` at repository root `/home/dev/repos/acme-backend/CONVENTIONS.md` -- **not found**. No project conventions to import into Implementation Notes.

## Investigation Strategy

The bug reports that a user's dark mode preference is lost when the browser is
fully closed and reopened. The toggle works within a session (the UI switches to
dark mode) but the setting does not survive a session boundary. This strongly
indicates a missing or broken **client-side persistence layer** -- typically
`localStorage`, `sessionStorage`, or a cookie.

Key areas to investigate:

1. The theme toggle / dark mode setting component
2. Where the theme preference is stored (in-memory state vs. durable storage)
3. The application bootstrap / initialization sequence (where the stored theme is read on load)
4. Existing test coverage for persistence behavior

## Investigation Findings

### 1. Theme/Appearance Component

Searched for files related to dark mode, theme, and appearance settings:

```
Glob: **/settings/**/*.{ts,tsx,js,jsx}
Glob: **/theme/**/*.{ts,tsx,js,jsx}
Glob: **/appearance/**/*.{ts,tsx,js,jsx}
Grep: "darkMode" | "dark-mode" | "theme" | "appearance"
```

**Found**: `src/components/settings/AppearancePanel.tsx`

The `AppearancePanel` component contains a `DarkModeToggle` element. The toggle's
state is managed via a React context (`ThemeContext`) and updates the `isDarkMode`
boolean through the context's in-memory state:

```
// Approximate discovered pattern
const { isDarkMode, setDarkMode } = useThemeContext();

function handleToggle(checked: boolean) {
  setDarkMode(checked);           // updates in-memory context only
  // no localStorage.setItem() call
}
```

**Finding**: The `handleToggle` function only updates the React context. It does
**not** write the preference to `localStorage` or any other durable store.

### 2. ThemeContext / ThemeProvider

**Found**: `src/context/ThemeContext.tsx`

The `ThemeContext` initializes `isDarkMode` from a hardcoded default (`false`, i.e.,
light mode) rather than reading from `localStorage`:

```
// Approximate discovered pattern
const [isDarkMode, setDarkMode] = useState(false);
// Expected pattern (missing):
// const [isDarkMode, setDarkMode] = useState(
//   localStorage.getItem('theme') === 'dark'
// );
```

**Finding**: On every page load (including after a full browser close/reopen),
`isDarkMode` is initialized to `false`. Any previously toggled preference is lost
because it was never written to `localStorage`.

### 3. Application Bootstrap

**Found**: `src/App.tsx`

The root application component wraps the tree in `<ThemeProvider>`. There is no
effect or initializer that reads a persisted theme value from `localStorage` before
rendering.

**Finding**: Confirms that no read-from-storage step exists at startup.

### 4. Existing Test Coverage

```
Grep: "darkMode" | "DarkModeToggle" in **/*.test.{ts,tsx}
```

**Found**: `src/components/settings/__tests__/AppearancePanel.test.tsx`

Existing tests assert that the toggle changes in-memory context state, but no test
exercises a page-reload scenario or checks `localStorage` interaction. The
persistence path is entirely untested.

### 5. Persistence-Impact Analysis

The dark mode preference is **not written to the database** -- it is a client-side
UI preference managed entirely in the browser. There is no ingestion-time
persistence boundary. The fix corrects the client-side read/write to `localStorage`.

**Result**: No data migration required. The bug is purely in the frontend
persistence layer.

## Affected Files and Symbols

| File | Symbol | Issue |
|------|--------|-------|
| `src/components/settings/AppearancePanel.tsx` | `handleToggle` | Does not write to `localStorage` after setting context |
| `src/context/ThemeContext.tsx` | `ThemeContext` / `useState` initializer | Initializes from hardcoded default, not from `localStorage` |
| `src/App.tsx` | `App` (root component) | No startup read of persisted theme |
| `src/components/settings/__tests__/AppearancePanel.test.tsx` | (test file) | Existing tests -- no coverage for persistence or reload scenario |

## Reuse Candidates

- `src/context/ThemeContext.tsx` -- the `ThemeContext` and `ThemeProvider` are the
  central state hub; the fix modifies this file's initializer and optionally adds
  a `useEffect` to sync writes
- `src/components/settings/__tests__/AppearancePanel.test.tsx` -- existing test
  setup can be extended to add the reproducer test (mock `localStorage` using
  `jest-localstorage-mock` or `vi.spyOn(window.localStorage, 'setItem')`)
