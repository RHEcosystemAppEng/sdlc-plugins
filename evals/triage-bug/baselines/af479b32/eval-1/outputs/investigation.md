# Steps 2-3 -- Codebase Investigation: ACME-500

## Step 2 -- Reproduce/Trace

### Reproduction approach

The bug involves the plan-feature skill's convention conformance analysis, which is a skill behavior rather than a directly runnable command. Code-path tracing was used instead of direct reproduction.

### Code-path trace

**Entry point**: `/plan-feature ACME-100` invocation triggers the plan-feature skill, which reads `CONVENTIONS.md` from the target repository root.

**Trace through convention loading**:

1. The skill reads the raw content of `CONVENTIONS.md` and splits it by newline.
2. For each line, it checks if the line starts with `## ` to identify section headings.
3. The heading text is extracted using `line[3:]`, which captures everything after `## ` -- including any trailing whitespace characters.

**Divergence point identified**: When a heading line contains trailing whitespace (e.g., `## Migration Patterns  \n`), the extracted section name becomes `"Migration Patterns  "` (with two trailing spaces) instead of `"Migration Patterns"`.

**Downstream failure**: The convention-aware task enrichment step performs an exact-match lookup:
```python
if convention_name in discovered_conventions:
    notes.append(f"Per CONVENTIONS.md ...{convention_name}: {action}")
```

The lookup key `"Migration Patterns"` does not match the stored key `"Migration Patterns  "`, so the convention is silently skipped. No warning or error is emitted.

### Trace findings

- The bug is **confirmed by code-path analysis**: trailing whitespace on CONVENTIONS.md headings causes exact-match failure in convention lookup.
- The failure is **silent** -- no diagnostic output indicates the convention was skipped.

## Step 3 -- Codebase Investigation

### Target repository

The bug affects the **sdlc-workflow** component, which maps to the plugin code within the repository. Based on the Repository Registry, the relevant repository is **acme-backend** at `/home/dev/repos/acme-backend`.

Since no Serena instance is available (Code Intelligence section states "No Serena MCP servers are configured"), investigation uses Read/Grep/Glob fallback.

### Affected files and symbols

| File | Symbol/Section | Issue |
|------|----------------|-------|
| `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` | Convention conformance analysis -- heading extraction | `line[3:]` does not strip trailing whitespace |
| `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` | Convention-aware task enrichment -- name matching | Exact-match comparison fails for keys with trailing whitespace |

### Affected code paths

**1. Heading extraction (convention loading)**:
```python
for line in conventions_content.split('\n'):
    if line.startswith('## '):
        section_name = line[3:]  # Does NOT strip trailing whitespace
        conventions[section_name] = current_section_content
```

**2. Convention matching (task enrichment)**:
```python
if convention_name in discovered_conventions:
    notes.append(f"Per CONVENTIONS.md ...{convention_name}: {action}")
```

### Existing test coverage

- `evals/plan-feature/files/conventions-mock.md` -- existing eval fixture for plan-feature conventions does NOT include trailing whitespace on headings.
- This edge case is **not covered** by current evals.

### CONVENTIONS.md lookup

The repository does not have a `CONVENTIONS.md` at its root. No additional conventions to inform the fix task.

### Patterns for reproducer test

- The existing eval pattern uses mock fixture files under `evals/plan-feature/files/`.
- A reproducer test should create a `CONVENTIONS.md` fixture with trailing whitespace on a heading line and verify that the convention is still matched and included in the generated task output.

### Reusable utilities

- Existing conventions-mock fixture (`evals/plan-feature/files/conventions-mock.md`) can serve as a base for creating the trailing-whitespace variant.
