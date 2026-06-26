# Steps 2-3 -- Codebase Investigation: ACME-500

## Step 2 -- Reproduce/Trace

### Reproduction approach

This bug involves the plan-feature skill's handling of CONVENTIONS.md headings. It cannot be directly reproduced via a CLI command in this context because it involves skill execution internals. Code-path tracing is the appropriate approach.

### Code-path trace

**Entry point**: The `/plan-feature ACME-100` invocation triggers the plan-feature skill, which reads CONVENTIONS.md headings during convention conformance analysis.

**Trace through the affected code path**:

1. The plan-feature skill reads the contents of `CONVENTIONS.md`.
2. It splits the content by newline and iterates over lines.
3. For each line starting with `## `, it extracts the section name using `line[3:]`.
4. The extracted section names are stored as keys in a `conventions` dictionary.
5. Later, during task enrichment, convention names are matched against the dictionary using exact comparison: `if convention_name in discovered_conventions`.

**Divergence point**: At step 3, `line[3:]` extracts everything after `## ` but does NOT strip trailing whitespace. When the heading line is `## Migration Patterns  \n`, the extracted key becomes `"Migration Patterns  "` (with two trailing spaces). The subsequent exact-match comparison in step 5 looks for `"Migration Patterns"` (without trailing spaces), which fails. The convention is silently skipped with no warning.

### Reproduction outcome

**Confirmed via trace**: The bug is reproducible whenever a CONVENTIONS.md heading line contains trailing whitespace. The heading extraction logic at `line[3:]` preserves trailing whitespace, causing all downstream exact-match comparisons to fail silently.

## Step 3 -- Codebase Investigation

### Target repository

- **Component**: sdlc-workflow
- **Repository**: acme-backend (from Repository Registry)
- **Serena Instance**: serena_backend
- **Path**: /home/dev/repos/acme-backend

Note: Per Code Intelligence section, no Serena MCP servers are configured. Investigation uses Read/Grep/Glob fallback (simulated via repo-context-mock.md).

### CONVENTIONS.md lookup

The repository does not have a CONVENTIONS.md file at its root. No conventions to incorporate into the fix task's Implementation Notes.

### Affected files and symbols

#### File: `plugins/sdlc-workflow/skills/plan-feature/SKILL.md`

**Convention heading extraction (convention conformance analysis)**:

```python
for line in conventions_content.split('\n'):
    if line.startswith('## '):
        section_name = line[3:]  # BUG: does not strip trailing whitespace
        conventions[section_name] = current_section_content
```

- `line[3:]` extracts the heading text after `## ` but retains any trailing whitespace (spaces, tabs).
- This is the root cause location.

**Convention-aware task enrichment**:

```python
if convention_name in discovered_conventions:
    notes.append(f"Per CONVENTIONS.md {convention_name}: {action}")
```

- This exact-match comparison fails when the dictionary key has trailing whitespace but the lookup key does not.
- This is where the bug manifests (silent skip).

### Existing test coverage

- **Existing test**: `evals/plan-feature/files/conventions-mock.md` -- the existing eval fixture does NOT include trailing whitespace on headings. This edge case is not covered by current evals.
- No existing tests exercise the trailing-whitespace scenario.

### Investigation summary

| Finding | Detail |
|---------|--------|
| Bug location | `plugins/sdlc-workflow/skills/plan-feature/SKILL.md`, convention heading extraction |
| Defective expression | `line[3:]` -- does not call `.strip()` on extracted heading text |
| Failure mode | Silent -- no warning or error when convention match fails |
| Affected downstream logic | Convention-aware task enrichment uses exact match against un-stripped keys |
| Test gap | No existing eval fixture includes trailing whitespace on headings |
