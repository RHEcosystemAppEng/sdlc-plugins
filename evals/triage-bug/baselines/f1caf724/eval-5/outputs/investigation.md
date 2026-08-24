# Codebase Investigation -- Step 3

## Target Repository

Based on the Component field (`sdlc-workflow`) and the Repository Registry in CLAUDE.md:

| Repository | Role | Serena Instance | Path |
|---|---|---|---|
| acme-backend | Rust backend service | serena_backend | /home/dev/repos/acme-backend |

Target repository: **acme-backend** at `/home/dev/repos/acme-backend`

## Code Intelligence

Per CLAUDE.md: "No Serena MCP servers are configured. Code intelligence is not available."

Using Read/Grep/Glob fallback for investigation.

## Investigation Findings

### Entry Point: Settings > Appearance > Dark Mode Toggle

The bug describes a user preference (dark mode) that is toggled ON but does not persist across browser sessions. This indicates the preference storage mechanism is either:
1. Not saving the preference at all
2. Saving to an ephemeral store (e.g., in-memory state, session storage) instead of a persistent store (e.g., localStorage, database-backed user preferences)
3. Saving correctly but failing to load on application init

### Affected Code Paths

Based on the Steps to Reproduce and the mock repository context, the following code paths are relevant:

1. **Settings/Appearance component** -- the UI component that handles the dark mode toggle. When toggled, it should dispatch a preference update to the persistence layer.

2. **User preferences storage** -- the mechanism responsible for persisting the dark mode setting. Given the bug manifests across browser sessions (close and reopen), the preference must be stored in a persistent medium (localStorage, cookie, or server-side user preferences API).

3. **Application initialization** -- the startup code that reads persisted preferences and applies them. If dark mode is stored but not read on init, the application defaults to light mode.

### CONVENTIONS.md Lookup

The repository does not have a CONVENTIONS.md at its root. No conventions to apply to task generation.

### Persistence-Impact Analysis

**Trace output to persistence boundary:**

The dark mode preference is a user setting. Depending on implementation:
- If stored client-side (localStorage): no database persistence boundary -- fix corrects future behavior immediately.
- If stored server-side (user_preferences table): a persistence boundary exists, but since this is a "preference not saved" bug (not a "preference saved incorrectly" bug), no data migration is needed -- existing records are simply absent, not incorrect.

**Result:** No data migration required. The fix needs to ensure the preference is written to persistent storage and read back on application initialization.

### Test Files and Patterns

From the mock repository context, existing eval fixtures exist at `evals/plan-feature/files/` but do not cover this specific dark mode persistence scenario. Test patterns should follow the existing eval fixture structure.
