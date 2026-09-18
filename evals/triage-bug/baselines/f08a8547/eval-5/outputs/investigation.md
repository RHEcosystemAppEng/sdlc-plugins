# Step 3 -- Codebase Investigation: ACME-511

## Target Repository

- **Component**: sdlc-workflow
- **Repository**: acme-backend (from Repository Registry)
- **Serena Instance**: serena_backend
- **Path**: /home/dev/repos/acme-backend

## Code Intelligence Limitations

Per CLAUDE.md Code Intelligence section: "No Serena MCP servers are configured. Code intelligence is not available." Falling back to Read/Grep/Glob for investigation.

## Investigation Findings

### Affected Code Path: Convention Heading Extraction

File: `plugins/sdlc-workflow/skills/plan-feature/SKILL.md`

The plan-feature skill reads `CONVENTIONS.md` headings using this logic:

```python
for line in conventions_content.split('\n'):
    if line.startswith('## '):
        section_name = line[3:]  # Extracts heading text after "## "
        conventions[section_name] = current_section_content
```

**Defect:** The heading extraction at `line[3:]` does NOT strip trailing whitespace.
If the heading line is `## Migration Patterns  \n`, the extracted section name
becomes `"Migration Patterns  "` (with trailing spaces), which fails exact-match
comparison against the expected `"Migration Patterns"`.

### Affected Code Path: Convention-Aware Task Enrichment

File: `plugins/sdlc-workflow/skills/plan-feature/SKILL.md`

The task enrichment step matches conventions by section name:

```python
if convention_name in discovered_conventions:
    notes.append(f"Per CONVENTIONS.md section {convention_name}: {action}")
```

This match fails when `convention_name` has trailing whitespace from the extraction step.

### Existing Test Coverage

File: `evals/plan-feature/files/conventions-mock.md`

The existing eval fixture for plan-feature conventions does NOT include trailing
whitespace on headings, so this edge case is not covered by current evals.

### CONVENTIONS.md Lookup

The repository does not have a CONVENTIONS.md at its root. No additional conventions
to inform implementation notes.

## Persistence-Impact Analysis

The buggy function's output (convention section names) is used for in-memory matching
during task enrichment. The section names are not persisted to a database -- they are
extracted and compared at query/processing time within the plan-feature skill execution.

**No persistence boundary found.** The output is computed at processing time. No data
migration is needed.

## Summary of Affected Files and Symbols

| File | Symbol/Location | Issue |
|------|----------------|-------|
| `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` | Convention heading extraction (`line[3:]`) | Missing `.strip()` on extracted section name |
| `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` | Convention-aware task enrichment (`convention_name in discovered_conventions`) | Exact-match fails due to trailing whitespace |
| `evals/plan-feature/files/conventions-mock.md` | Test fixture | Does not cover trailing whitespace edge case |
