# Step 3 -- Codebase Investigation

## Target Repository

- **Repository**: acme-backend
- **Role**: Rust backend service
- **Serena Instance**: serena_backend
- **Path**: /home/dev/repos/acme-backend

Identified from the Repository Registry based on the **Component** field (`sdlc-workflow`) and the code paths referenced in the bug description.

## Code Intelligence Limitations

Per CLAUDE.md: "No Serena MCP servers are configured. Code intelligence is not available." Falling back to Read/Grep/Glob for investigation.

## Investigation Findings

### File: plugins/sdlc-workflow/skills/plan-feature/SKILL.md

#### Convention Conformance Analysis

The plan-feature skill reads `CONVENTIONS.md` headings using heading extraction logic:

```python
for line in conventions_content.split('\n'):
    if line.startswith('## '):
        section_name = line[3:]  # Extracts heading text after "## "
        conventions[section_name] = current_section_content
```

**Defect identified:** The heading extraction at `line[3:]` does NOT strip trailing whitespace. If the heading line is `## Migration Patterns  \n`, the extracted section name becomes `"Migration Patterns  "` (with trailing spaces), which fails exact-match comparison against the expected `"Migration Patterns"`.

#### Convention-Aware Task Enrichment

The task enrichment step matches conventions by section name:

```python
if convention_name in discovered_conventions:
    notes.append(f"Per CONVENTIONS.md {convention_name}: {action}")
```

This match fails when `convention_name` has trailing whitespace from the extraction step. The preference/setting lookup follows the same convention-based pattern, meaning user preferences (such as dark mode) that rely on convention section matching would not be found if the heading has trailing whitespace.

### Test Coverage

**Existing test**: `evals/plan-feature/files/conventions-mock.md`

The existing eval fixture for plan-feature conventions does NOT include trailing whitespace on headings, so this edge case is not covered by current evals.

### CONVENTIONS.md

The repository does not have a `CONVENTIONS.md` at its root. No additional conventions to inform the fix task's Implementation Notes.

## Summary of Affected Files and Symbols

| File | Symbol/Section | Issue |
|------|----------------|-------|
| `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` | Convention heading extraction (`line[3:]`) | Missing `.strip()` on extracted heading text |
| `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` | Convention-aware task enrichment (`convention_name in discovered_conventions`) | Exact-match fails due to trailing whitespace |
| `evals/plan-feature/files/conventions-mock.md` | Test fixture | Does not cover trailing whitespace edge case |
