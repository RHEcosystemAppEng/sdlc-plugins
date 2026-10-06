# Step 3 -- Codebase Investigation

## Target Repository

- **Repository**: acme-backend
- **Role**: Rust backend service
- **Serena Instance**: serena_backend (not available -- Code Intelligence section indicates no Serena instances configured)
- **Path**: /home/dev/repos/acme-backend
- **Component from Bug**: sdlc-workflow

Since no Serena MCP servers are configured, the investigation uses Read, Grep, and Glob tools as fallback.

## Convention Conformance Analysis -- Heading Extraction

### Affected File

`plugins/sdlc-workflow/skills/plan-feature/SKILL.md` -- convention lookup logic

### Buggy Code Path

The plan-feature skill reads `CONVENTIONS.md` headings using this logic:

```python
for line in conventions_content.split('\n'):
    if line.startswith('## '):
        section_name = line[3:]  # Extracts heading text after "## "
        conventions[section_name] = current_section_content
```

**Finding**: The heading extraction at `line[3:]` does NOT strip trailing whitespace. When the heading line is `## Migration Patterns  \n`, the extracted section name becomes `"Migration Patterns  "` (with two trailing spaces), which fails exact-match comparison against the expected `"Migration Patterns"`.

## Convention-Aware Task Enrichment

### Affected Code

```python
if convention_name in discovered_conventions:
    notes.append(f"Per CONVENTIONS.md {convention_name}: {action}")
```

This dictionary lookup fails when `convention_name` is `"Migration Patterns"` but the key stored in `discovered_conventions` is `"Migration Patterns  "` (with trailing whitespace).

## Test Coverage

### Existing Test Fixture

`evals/plan-feature/files/conventions-mock.md` -- the existing eval fixture for plan-feature conventions does NOT include trailing whitespace on headings, so this edge case is not covered by current evals.

## CONVENTIONS.md Lookup

The repository at `/home/dev/repos/acme-backend` does not have a `CONVENTIONS.md` at its root. No conventions to inform the fix task's Implementation Notes.

## Persistence-Impact Analysis

The buggy function's output (the parsed conventions dictionary) is used at task generation time to enrich task descriptions written to Jira. The conventions data is NOT persisted to a database -- it is computed on each `/plan-feature` invocation and written to a Jira issue description.

**Conclusion**: No persistence boundary found. The output is computed at invocation time. No data migration is needed. Previously generated tasks that were missing convention references are already in Jira but are not automatically correctable; however, this is a Jira content issue, not a database persistence concern.

## Summary of Findings

| Finding | File | Symbol/Location |
|---------|------|-----------------|
| Heading extraction does not strip trailing whitespace | `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` | Convention lookup loop, `line[3:]` |
| Exact-match lookup fails for whitespace-padded keys | `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` | Convention-aware task enrichment, `convention_name in discovered_conventions` |
| No test coverage for trailing whitespace edge case | `evals/plan-feature/files/conventions-mock.md` | Eval fixture missing trailing whitespace variant |
| No warning or error logged on match failure | `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` | Silent skip in enrichment logic |
