# Step 3 -- Codebase Investigation

## Target Repository

- **Repository**: acme-backend
- **Role**: Rust backend service
- **Serena Instance**: serena_backend
- **Path**: /home/dev/repos/acme-backend
- **Component match**: Bug component is `sdlc-workflow`, matching the plugins/sdlc-workflow directory within the repository.

## Code Intelligence

Per CLAUDE.md: "No Serena MCP servers are configured. Code intelligence is not available."
Falling back to Read/Grep/Glob for investigation.

## Investigation Findings

### Convention conformance analysis

**File**: `plugins/sdlc-workflow/skills/plan-feature/SKILL.md`

The plan-feature skill reads `CONVENTIONS.md` headings using this logic:

```python
for line in conventions_content.split('\n'):
    if line.startswith('## '):
        section_name = line[3:]  # Extracts heading text after "## "
        conventions[section_name] = current_section_content
```

**Defect identified**: The heading extraction at `line[3:]` does NOT strip trailing whitespace. If the heading line is `## Migration Patterns  \n`, the extracted section name becomes `"Migration Patterns  "` (with trailing spaces), which fails exact-match comparison against the expected `"Migration Patterns"`.

### Convention-aware task enrichment

**File**: `plugins/sdlc-workflow/skills/plan-feature/SKILL.md`

The task enrichment step matches conventions by section name:

```python
if convention_name in discovered_conventions:
    notes.append(f"Per CONVENTIONS.md §{convention_name}: {action}")
```

This match fails when `convention_name` has trailing whitespace from the extraction step. The dark mode preference key lookup follows a similar pattern -- the settings section name is extracted without stripping, causing exact-match lookups against known preference keys (such as "Dark Mode") to fail, and the preference is never persisted.

### Test coverage gap

**Existing test**: `evals/plan-feature/files/conventions-mock.md`

The existing eval fixture for plan-feature conventions does NOT include trailing whitespace on headings -- so this edge case is not covered by current evals.

### CONVENTIONS.md

The repository does not have a `CONVENTIONS.md` at its root.

## Persistence-Impact Analysis

The buggy heading extraction function's output is used for in-memory key matching during settings persistence. The preference value itself would be persisted correctly if the key match succeeded. Since the key match fails due to trailing whitespace, the preference is never written to persistence in the first place -- no stale data exists in the database.

**Result**: No persistence boundary is reached for incorrect data. The code fix alone (stripping trailing whitespace) will correct future behavior. No data migration is needed.
