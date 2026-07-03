# Codebase Investigation: ACME-500

## Step 2 -- Reproduce/Trace

### Reproduction approach

This bug involves the plan-feature skill's internal convention parsing logic, which is not directly runnable as a CLI command. Code-path tracing is the appropriate method.

### Code-path trace

**Entry point**: `/plan-feature ACME-100` invocation triggers the plan-feature skill, which reads `CONVENTIONS.md` and performs convention conformance analysis.

**Trace through convention heading extraction**:

The plan-feature skill reads `CONVENTIONS.md` headings using this logic:

```python
for line in conventions_content.split('\n'):
    if line.startswith('## '):
        section_name = line[3:]  # Extracts heading text after "## "
        conventions[section_name] = current_section_content
```

When the heading line is `## Migration Patterns  \n` (with trailing whitespace), `line[3:]` extracts `"Migration Patterns  "` (with two trailing spaces). The extraction does NOT call `.strip()` on the result.

**Trace through convention matching**:

The task enrichment step matches conventions by exact section name:

```python
if convention_name in discovered_conventions:
    notes.append(f"Per CONVENTIONS.md §{convention_name}: {action}")
```

The lookup uses the clean name `"Migration Patterns"` but the dictionary key is `"Migration Patterns  "` (with trailing spaces). The exact match fails, and the convention is silently skipped -- no warning or error is emitted.

**Divergence point**: The behavior diverges at the heading extraction step, where trailing whitespace is preserved in the dictionary key, causing all subsequent lookups to fail for any heading with trailing whitespace.

## Step 3 -- Codebase Investigation

### Target repository

- **Component**: sdlc-workflow
- **Repository**: acme-backend (from Repository Registry)
- **Path**: /home/dev/repos/acme-backend

### Serena availability

No Serena MCP servers are configured per the Code Intelligence section. Using Read/Grep/Glob fallback.

### Affected files and symbols

| File | Symbol/Section | Role |
|---|---|---|
| `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` | Convention heading extraction (`line[3:]`) | Extracts convention section names without stripping whitespace |
| `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` | Convention-aware task enrichment (`convention_name in discovered_conventions`) | Exact-match lookup fails when key has trailing whitespace |

### Existing test coverage

- **File**: `evals/plan-feature/files/conventions-mock.md`
- **Finding**: The existing eval fixture for plan-feature conventions does NOT include trailing whitespace on headings. This edge case is not covered by current evals.

### CONVENTIONS.md lookup

The repository does not have a `CONVENTIONS.md` at its root. No conventions to reference in the fix task's Implementation Notes.

### Investigation summary

1. **Single root cause**: The heading extraction at `line[3:]` does not strip trailing whitespace, causing downstream exact-match lookups to fail silently.
2. **No existing test coverage**: The plan-feature eval fixtures do not include headings with trailing whitespace.
3. **Silent failure**: No warning or diagnostic is emitted when a convention is skipped due to a match failure, making the bug hard to detect.
