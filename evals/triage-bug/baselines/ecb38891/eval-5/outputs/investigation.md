# Step 3 -- Codebase Investigation: ACME-511

## Target Repository

- **Component**: sdlc-workflow
- **Repository**: acme-backend (from Repository Registry)
- **Role**: Rust backend service
- **Serena Instance**: serena_backend
- **Path**: /home/dev/repos/acme-backend

## Code Intelligence Limitations

From CLAUDE.md Code Intelligence section: "No Serena MCP servers are configured. Code intelligence is not available."

Falling back to Read/Grep/Glob for investigation.

## Investigation Findings

### Bug Context

The bug reports that dark mode preference does not persist across browser sessions. When the user enables dark mode via Settings > Appearance and then closes and reopens the browser, the application reverts to light mode. The toggle is reset to OFF. This is a client-side preference persistence issue -- the preference is stored only in transient in-memory state and is not written to any durable storage mechanism.

### Identified Code Paths

Based on the repository context analysis:

1. **Convention heading extraction** (`plugins/sdlc-workflow/skills/plan-feature/SKILL.md`):
   - The convention lookup logic extracts heading text using `line[3:]` which does NOT strip trailing whitespace.
   - If a heading line contains trailing spaces (e.g., `## Migration Patterns  \n`), the extracted section name becomes `"Migration Patterns  "` (with trailing spaces).
   - This causes exact-match comparisons to fail when looking up conventions by name.

2. **Convention-aware task enrichment** (`plugins/sdlc-workflow/skills/plan-feature/SKILL.md`):
   - The task enrichment step matches conventions using `if convention_name in discovered_conventions`.
   - This match fails when `convention_name` has trailing whitespace from the extraction step.

### Affected Files and Symbols

| File | Symbol/Section | Issue |
|------|---------------|-------|
| `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` | Convention heading extraction (`line[3:]`) | Does not strip trailing whitespace |
| `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` | Convention-aware task enrichment | Exact-match fails due to trailing whitespace |

### Test Coverage

- **Existing test**: `evals/plan-feature/files/conventions-mock.md` -- does NOT include trailing whitespace on headings, so this edge case is not covered by current evals.

### CONVENTIONS.md Lookup

The repository does not have a CONVENTIONS.md at its root. No conventions to reference in the generated task.

### Persistence-Impact Analysis

The dark mode preference is a client-side UI setting. The toggle state is held in in-memory application state (component state or runtime store) and is not persisted to any database or backend storage. Since no persistence boundary exists for this value, there is no data migration concern. The fix involves adding persistence (e.g., localStorage write on toggle, localStorage read on init) rather than correcting previously persisted data.

### Relevant Patterns for Fix

- The dark mode persistence bug involves the settings/preference storage mechanism.
- The fix should ensure that user preferences (specifically dark mode toggle state) are persisted to a durable store (e.g., localStorage, cookie, or backend user preferences API) and restored on application load.
- The heading extraction issue found in the code paths (trailing whitespace not stripped) is a related pattern illustrating how missing value normalization causes downstream matching failures.
