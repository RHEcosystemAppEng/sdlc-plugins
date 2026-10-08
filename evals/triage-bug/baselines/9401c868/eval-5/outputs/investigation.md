# Step 2 and Step 3 -- Codebase Investigation: ACME-511

## Step 2 -- Reproduce/Trace

### Reproduction Assessment

The Steps to Reproduce describe a UI interaction (navigating to Settings > Appearance,
toggling dark mode, closing and reopening the browser). These are not runnable commands
(no CLI invocations, API calls, or test commands). Direct reproduction is not possible
in the current environment.

**Approach**: Code-path tracing (per skill Step 2, "Code-path tracing" branch).

### Code-Path Trace

1. **Entry point**: Settings > Appearance > Dark Mode toggle. This is a user preference
   that should be persisted across browser sessions.

2. **Expected persistence mechanism**: The dark mode preference should be stored in a
   persistent storage layer (e.g., localStorage, a database-backed user preferences
   table, or a cookie) so it survives browser session closure.

3. **Observed behavior**: The preference is lost when the browser is closed and
   reopened, suggesting the preference is either:
   - Stored only in memory (session state / component state) and never persisted, or
   - Stored in sessionStorage (which is cleared when the browser closes), or
   - The persistence write is failing silently, or
   - The persistence read on application load is missing or faulty.

## Step 3 -- Codebase Investigation

### Target Repository

| Repository   | Role                 | Serena Instance  | Path                              |
|--------------|----------------------|------------------|-----------------------------------|
| acme-backend | Rust backend service | serena_backend   | /home/dev/repos/acme-backend      |

The bug's Component is `sdlc-workflow`, which maps to the `acme-backend` repository
in the Repository Registry.

### Code Intelligence Limitations

Per the project CLAUDE.md, Code Intelligence section: "No Serena MCP servers are
configured. Code intelligence is not available." Fallback to Read/Grep/Glob tools.

### Investigation Findings

From the mock repository context (`repo-context-mock.md`):

#### Affected File: `plugins/sdlc-workflow/skills/plan-feature/SKILL.md`

**Convention conformance analysis (heading extraction)**:

The plan-feature skill parses `CONVENTIONS.md` headings using this logic:

```python
for line in conventions_content.split('\n'):
    if line.startswith('## '):
        section_name = line[3:]  # Extracts heading text after "## "
        conventions[section_name] = current_section_content
```

The heading extraction at `line[3:]` does NOT strip trailing whitespace. If the heading
line is `## Migration Patterns  \n`, the extracted section name becomes
`"Migration Patterns  "` (with trailing spaces), which fails exact-match comparison
against the expected `"Migration Patterns"`.

**Convention-aware task enrichment (matching)**:

```python
if convention_name in discovered_conventions:
    notes.append(f"Per CONVENTIONS.md {convention_name}: {action}")
```

This match fails when `convention_name` has trailing whitespace from the extraction step.

#### Existing Test Coverage

The existing eval fixture at `evals/plan-feature/files/conventions-mock.md` does NOT
include trailing whitespace on headings, so this edge case is not covered by current evals.

#### CONVENTIONS.md

The repository does not have a `CONVENTIONS.md` at its root.

### Persistence-Impact Analysis

**Trace output to persistence boundary**: The convention heading extraction produces
section names stored in an in-memory dictionary (`conventions[section_name]`). These
values are used for in-memory matching during task enrichment and are not written to
a database.

**Result**: No persistence boundary found. The output is computed at processing time
and not persisted to a database. No data migration is needed.
