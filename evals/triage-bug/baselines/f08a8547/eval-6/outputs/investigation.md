# Step 3 -- Codebase Investigation

## Target Repository

Based on the **Component** field (`sdlc-workflow`) and the code paths referenced in the
Steps to Reproduce (`/plan-feature`, `CONVENTIONS.md` processing), the bug affects the
**acme-backend** repository.

**Repository Registry entry:**

| Repository   | Role                 | Serena Instance  | Path                              |
|-------------|----------------------|------------------|-----------------------------------|
| acme-backend | Rust backend service | serena_backend   | /home/dev/repos/acme-backend      |

## Code Intelligence Note

The project CLAUDE.md states: "No Serena MCP servers are configured. Code intelligence
is not available." Falling back to Read/Grep/Glob tools for investigation.

## Affected Files and Symbols

### 1. Convention Heading Extraction -- `plugins/sdlc-workflow/skills/plan-feature/SKILL.md`

The plan-feature skill parses CONVENTIONS.md headings using the following logic:

```python
for line in conventions_content.split('\n'):
    if line.startswith('## '):
        section_name = line[3:]  # Extracts heading text after "## "
        conventions[section_name] = current_section_content
```

**Defect:** The extraction `line[3:]` captures the raw text after `## ` without stripping
trailing whitespace. When a heading line is `## Migration Patterns  \n`, the extracted
section name becomes `"Migration Patterns  "` (with two trailing spaces).

### 2. Convention-Aware Task Enrichment -- `plugins/sdlc-workflow/skills/plan-feature/SKILL.md`

The task enrichment step matches conventions by exact section name comparison:

```python
if convention_name in discovered_conventions:
    notes.append(f"Per CONVENTIONS.md {convention_name}: {action}")
```

**Defect:** This match uses exact string comparison. The key `"Migration Patterns  "` (with
trailing spaces) does not match the lookup key `"Migration Patterns"` (without trailing
spaces), so the convention is silently skipped.

### 3. No Warning or Error Path

There is no fallback logic, fuzzy matching, or warning when a convention is expected but
not found in the discovered conventions dictionary. The mismatch is completely silent.

## Existing Test Coverage

### `evals/plan-feature/files/conventions-mock.md`

The existing eval fixture for plan-feature conventions does NOT include trailing whitespace
on headings. The edge case of trailing whitespace in convention headings is not covered
by current evals.

## CONVENTIONS.md Lookup

The repository does not have a `CONVENTIONS.md` file at its root. No conventions to
inform the generated task's Implementation Notes.

## Persistence-Impact Analysis

The buggy function extracts convention headings from CONVENTIONS.md and uses them for
in-memory dictionary lookups during task generation. The convention matching result is
used to compose task description text.

**Trace:** `conventions_content.split('\n')` -> heading extraction -> `conventions[section_name]`
dictionary -> `convention_name in discovered_conventions` lookup -> task description text output

No persistence boundary was found. The convention matching is computed at task-generation
time and the output is written to Jira issue descriptions via the API, not persisted to a
local database. No data migration is needed.

## Decomposition Guard (Step 6)

This bug has a **single root cause**: the heading extraction does not strip trailing
whitespace, which causes the downstream exact-match comparison to fail. Although the defect
manifests at two points in the code (extraction and matching), both are part of the same
logical flow and share one underlying cause. A single Task is appropriate.

## Summary of Findings

| Aspect                    | Finding                                                            |
|---------------------------|--------------------------------------------------------------------|
| Affected file             | `plugins/sdlc-workflow/skills/plan-feature/SKILL.md`               |
| Buggy operation           | Heading extraction via `line[3:]` without `.strip()`               |
| Silent failure            | No warning when convention match fails                             |
| Test gap                  | No eval fixture tests trailing whitespace on CONVENTIONS.md headings|
| Persistence impact        | None -- computed at task-generation time                           |
| Decomposition             | Single root cause -- no split needed                              |
