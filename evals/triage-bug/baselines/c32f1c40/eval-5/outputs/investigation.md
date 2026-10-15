# Step 3 -- Codebase Investigation: ACME-511

## Target Repository

- **Repository**: acme-backend
- **Role**: Rust backend service
- **Serena Instance**: serena_backend
- **Path**: /home/dev/repos/acme-backend

Identified from the Repository Registry in CLAUDE.md. The Component field (`sdlc-workflow`)
and the nature of the bug (dark mode preference persistence) point to this repository.

## Code Intelligence Limitations

Per CLAUDE.md Code Intelligence section: "No Serena MCP servers are configured.
Code intelligence is not available." Falling back to Read/Grep/Glob tools.

## Investigation Findings

### Relevant Code Paths

#### Convention Heading Extraction (plan-feature skill)

File: `plugins/sdlc-workflow/skills/plan-feature/SKILL.md`

The plan-feature skill reads `CONVENTIONS.md` headings using this logic:

```python
for line in conventions_content.split('\n'):
    if line.startswith('## '):
        section_name = line[3:]  # Extracts heading text after "## "
        conventions[section_name] = current_section_content
```

**Issue identified**: The heading extraction at `line[3:]` does NOT strip trailing
whitespace. If the heading line is `## Migration Patterns  \n`, the extracted section
name becomes `"Migration Patterns  "` (with trailing spaces), which fails exact-match
comparison against the expected `"Migration Patterns"`.

#### Convention-Aware Task Enrichment

File: `plugins/sdlc-workflow/skills/plan-feature/SKILL.md`

The task enrichment step matches conventions by section name:

```python
if convention_name in discovered_conventions:
    notes.append(f"Per CONVENTIONS.md §{convention_name}: {action}")
```

This match fails when `convention_name` has trailing whitespace from the extraction step.

### Test Coverage Gap

File: `evals/plan-feature/files/conventions-mock.md`

The existing eval fixture for plan-feature conventions does NOT include trailing
whitespace on headings, so this edge case is not covered by current evals.

### CONVENTIONS.md

The repository does not have a CONVENTIONS.md at its root.

## Persistence-Impact Analysis

The bug concerns dark mode preference not persisting across browser sessions. The
preference toggle state is a UI setting. Tracing the preference storage:

- The dark mode setting is toggled in Settings > Appearance
- The setting value is not written to a backend database -- it is a client-side
  preference that should be stored in browser localStorage or a similar client-side
  persistence mechanism
- No persistence boundary to a backend database was found

**Result**: No data migration is needed. The bug is about client-side preference
persistence, not backend data storage. Fixing the preference storage mechanism will
correct the issue for all future sessions.

## Decomposition Guard (Step 6)

The bug has a single root cause: the dark mode preference is not being persisted to
client-side storage when the user toggles it. This is a single defect, not multiple
independent issues. No decomposition is needed.
