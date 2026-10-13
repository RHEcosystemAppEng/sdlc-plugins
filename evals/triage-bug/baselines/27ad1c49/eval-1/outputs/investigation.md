# Steps 2-3 -- Codebase Investigation: ACME-500

## Step 2 -- Reproduce/Trace

### Reproduction approach

This bug involves the plan-feature skill's behavior when processing `CONVENTIONS.md` files.
It is not directly reproducible via a single CLI command; instead, code-path tracing is used
to understand the defect.

### Code-path tracing

**Entry point**: `/plan-feature ACME-100` invocation (plan-feature skill entry).

**Trace path 1 -- Convention heading extraction**:

Location: `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` (convention conformance analysis)

```python
for line in conventions_content.split('\n'):
    if line.startswith('## '):
        section_name = line[3:]  # Extracts heading text after "## "
        conventions[section_name] = current_section_content
```

When `CONVENTIONS.md` contains the line `## Migration Patterns  \n` (with trailing whitespace),
`line[3:]` extracts `"Migration Patterns  "` (with two trailing spaces). The key stored in the
`conventions` dictionary includes the trailing whitespace.

**Trace path 2 -- Convention-aware task enrichment**:

Location: `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` (convention-aware task enrichment)

```python
if convention_name in discovered_conventions:
    notes.append(f"Per CONVENTIONS.md {convention_name}: {action}")
```

The `convention_name` used in the lookup is the clean, expected name (e.g., `"Migration Patterns"`
without trailing whitespace). The `in` operator performs an exact-match key lookup in the
`discovered_conventions` dictionary. Since the stored key is `"Migration Patterns  "` (with
trailing spaces) and the lookup key is `"Migration Patterns"` (without), the match fails.

**Divergence point**: The actual behavior diverges from expected behavior at the heading
extraction step. The extraction preserves trailing whitespace, which causes downstream
exact-match lookups to fail silently -- no warning or error is raised.

### Reproduction outcome

**Confirmed via trace**: The root cause is identifiable from the code. A heading line with
trailing whitespace in CONVENTIONS.md will produce a dictionary key with trailing whitespace,
which will never match a clean lookup key. The convention is silently dropped.

## Step 3 -- Codebase Investigation

### Target repository

Based on the Component field (`sdlc-workflow`) and the code paths referenced in the bug
description, the target repository is:

| Repository | Role | Serena Instance | Path |
|---|---|---|---|
| acme-backend | Rust backend service | serena_backend | /home/dev/repos/acme-backend |

The bug affects the `plan-feature` skill within the sdlc-workflow plugin.

### Serena availability

Per CLAUDE.md Code Intelligence section: "No Serena MCP servers are configured. Code
intelligence is not available." Fallback to Read/Grep/Glob for investigation.

### Affected files and symbols

| File | Symbol/Location | Role in Bug |
|------|----------------|-------------|
| `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` | Convention conformance analysis -- heading extraction (`line[3:]`) | **Primary defect**: extracts heading text without stripping trailing whitespace |
| `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` | Convention-aware task enrichment (`convention_name in discovered_conventions`) | **Secondary impact**: exact-match lookup fails due to whitespace mismatch |

### Existing test coverage

| Test File | Coverage |
|-----------|----------|
| `evals/plan-feature/files/conventions-mock.md` | Existing fixture does NOT include trailing whitespace on headings -- edge case is not covered |

No existing test or eval covers the trailing-whitespace edge case on CONVENTIONS.md headings.

### CONVENTIONS.md lookup

The repository does not have a `CONVENTIONS.md` file at its root. No conventions to apply
to the generated task.

### Persistence-impact analysis

The buggy function's output (convention section names and their content) is used at
task-generation time to enrich Jira task descriptions. The output flows through:

1. `section_name = line[3:]` (heading extraction)
2. `conventions[section_name] = current_section_content` (stored in in-memory dictionary)
3. `if convention_name in discovered_conventions` (lookup for task enrichment)
4. Task description text generated and posted to Jira via `jira.create_issue`

The convention data is **computed at generation time** and written to a Jira task description.
While the Jira task description is persisted, the incorrect behavior (omitting a convention)
results in **missing content** rather than **incorrect stored data**. There is no database
table or column containing stale values that need correction. Fixing the heading extraction
logic corrects future task generation.

**Conclusion**: No persistence boundary is involved. No data migration is needed.

### Summary of findings

The bug has a **single root cause**: the convention heading extraction in plan-feature does
not strip trailing whitespace from `CONVENTIONS.md` heading lines. This causes a silent
failure in convention matching during task enrichment. No decomposition is needed (Step 6
not triggered).
