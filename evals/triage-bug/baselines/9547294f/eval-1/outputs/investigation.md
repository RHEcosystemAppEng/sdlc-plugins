# Step 2 -- Reproduce/Trace

## Code-path Tracing

This bug involves a skill behavior (plan-feature convention conformance analysis), so direct reproduction via CLI is not applicable. Instead, tracing through the relevant code paths.

### Entry point

The entry point is the `/plan-feature ACME-100` invocation, which triggers the plan-feature skill's convention conformance analysis.

### Trace findings

1. **Convention heading extraction**: The plan-feature skill reads `CONVENTIONS.md` and extracts section headings using `line[3:]` (stripping only the `## ` prefix). This does NOT strip trailing whitespace from the heading line.

2. **Key defect**: When a heading line contains trailing whitespace (e.g., `## Migration Patterns  \n`), the extracted section name becomes `"Migration Patterns  "` (with trailing spaces) instead of `"Migration Patterns"`.

3. **Failed match**: The convention-aware task enrichment step performs exact string comparison (`if convention_name in discovered_conventions`). The stored key `"Migration Patterns  "` does not match the expected lookup key `"Migration Patterns"`, so the convention is silently skipped.

4. **No error handling**: There is no warning or fallback when a convention section is discovered but not matched. The failure is completely silent.

### Reproduction outcome

**Confirmed via code-path trace.** The bug is deterministic: any `CONVENTIONS.md` heading with trailing whitespace will cause that convention to be silently dropped from generated task descriptions.

---

# Step 3 -- Codebase Investigation

## Target Repository

- **Repository**: acme-backend
- **Serena Instance**: serena_backend (however, Code Intelligence section notes no Serena MCP servers are configured)
- **Path**: /home/dev/repos/acme-backend

Since no Serena instances are available, investigation uses Read/Grep/Glob fallback.

## Affected Files and Symbols

### 1. Convention heading extraction -- `plugins/sdlc-workflow/skills/plan-feature/SKILL.md`

The convention lookup logic:

```python
for line in conventions_content.split('\n'):
    if line.startswith('## '):
        section_name = line[3:]  # BUG: does not strip trailing whitespace
        conventions[section_name] = current_section_content
```

The `line[3:]` extraction preserves any trailing whitespace from the heading line. This is the root of the defect.

### 2. Convention-aware task enrichment -- `plugins/sdlc-workflow/skills/plan-feature/SKILL.md`

The task enrichment performs exact-match comparison:

```python
if convention_name in discovered_conventions:
    notes.append(f"Per CONVENTIONS.md  {convention_name}: {action}")
```

This match fails when the stored key has trailing whitespace but the lookup key does not.

### 3. Existing test coverage -- `evals/plan-feature/files/conventions-mock.md`

The existing eval fixture for plan-feature conventions does NOT include trailing whitespace on headings. This edge case is not covered by current evals.

## CONVENTIONS.md Lookup

The target repository (acme-backend) does not have a `CONVENTIONS.md` at its root. No conventions to incorporate into implementation notes from the target repo.

## Existing Test Patterns

The existing eval fixture at `evals/plan-feature/files/conventions-mock.md` provides the pattern for convention mock files. A reproducer test should create a similar fixture with trailing whitespace on headings to trigger the bug.

## Reuse Candidates

No existing utility functions for whitespace-safe heading extraction were found in the codebase. The fix will need to modify the extraction logic directly.
