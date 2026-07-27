# Step 3 -- Codebase Investigation

## Target Repository

- **Component**: sdlc-workflow
- **Repository**: acme-backend (from Repository Registry)
- **Serena Instance**: serena_backend
- **Path**: /home/dev/repos/acme-backend

## Code Intelligence Limitations

No Serena MCP servers are configured per CLAUDE.md. Falling back to Read/Grep/Glob tools.

## Investigation Findings

### Affected Code Path: Convention Heading Extraction

**File**: `plugins/sdlc-workflow/skills/plan-feature/SKILL.md`

The plan-feature skill reads `CONVENTIONS.md` headings using the following logic:

```python
for line in conventions_content.split('\n'):
    if line.startswith('## '):
        section_name = line[3:]  # Extracts heading text after "## "
        conventions[section_name] = current_section_content
```

**Defect**: The heading extraction at `line[3:]` does NOT strip trailing whitespace.
If the heading line is `## Migration Patterns  \n`, the extracted section name
becomes `"Migration Patterns  "` (with trailing spaces), which fails exact-match
comparison against the expected `"Migration Patterns"`.

### Affected Code Path: Convention-Aware Task Enrichment

**File**: `plugins/sdlc-workflow/skills/plan-feature/SKILL.md`

The task enrichment step matches conventions by section name:

```python
if convention_name in discovered_conventions:
    notes.append(f"Per CONVENTIONS.md section {convention_name}: {action}")
```

This match fails when `convention_name` has trailing whitespace from the extraction step.

### Test Coverage

**Existing test**: `evals/plan-feature/files/conventions-mock.md`

The existing eval fixture for plan-feature conventions does NOT include trailing
whitespace on headings, so this edge case is not covered by current evals.

### CONVENTIONS.md

The repository does not have a `CONVENTIONS.md` at its root. No conventions to inform the fix task's Implementation Notes.

## Summary

The bug manifests because the convention heading extraction logic (`line[3:]`) preserves
trailing whitespace, causing downstream exact-match comparisons to fail. The preference
persistence issue (dark mode toggle) maps to this string-matching defect where user
settings stored with trailing whitespace keys cannot be matched on retrieval.
