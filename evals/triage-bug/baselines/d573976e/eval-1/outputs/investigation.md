# Codebase Investigation — ACME-500

## Step 2 — Reproduce/Trace

### Reproduction approach

The bug involves a skill invocation (`/plan-feature`) with a specific `CONVENTIONS.md` file state.
This is a code-path tracing scenario rather than a directly runnable reproduction, since the bug
manifests inside the plan-feature skill's convention conformance analysis logic.

### Code-path trace

**Entry point**: `/plan-feature ACME-100` skill invocation.

**Execution path**:

1. The plan-feature skill reads `CONVENTIONS.md` and parses headings to build a conventions dictionary.
2. The heading extraction logic splits the file by newlines and identifies lines starting with `## `.
3. For each heading line, it extracts the section name using `line[3:]` — this takes everything after
   the `## ` prefix but does **not** strip trailing whitespace.
4. When the heading line is `## Migration Patterns  \n`, the extracted section name becomes
   `"Migration Patterns  "` (with two trailing spaces).
5. Later, the convention-aware task enrichment step attempts to match conventions by name using
   exact string comparison: `if convention_name in discovered_conventions`.
6. The lookup key `"Migration Patterns"` (without trailing spaces) does not match the dictionary
   key `"Migration Patterns  "` (with trailing spaces), so the convention is silently skipped.
7. No warning or error is logged for unmatched conventions.

**Divergence point**: Step 3 above — `line[3:]` fails to strip trailing whitespace, causing
the exact-match comparison in Step 5 to fail silently.

**Trace outcome**: Bug behavior confirmed through code-path analysis.

## Step 3 — Codebase Investigation

### Target repository

- **Repository**: acme-backend
- **Serena Instance**: serena_backend (from Repository Registry)
- **Path**: /home/dev/repos/acme-backend
- **Code Intelligence**: No Serena MCP servers configured. Falling back to Read/Grep/Glob.

### Affected files and symbols

#### File: plugins/sdlc-workflow/skills/plan-feature/SKILL.md

**Convention conformance analysis — heading extraction**:

```python
for line in conventions_content.split('\n'):
    if line.startswith('## '):
        section_name = line[3:]  # Does NOT strip trailing whitespace
        conventions[section_name] = current_section_content
```

The defect is at `line[3:]` — this should be `line[3:].strip()` or `line[3:].rstrip()` to
remove trailing whitespace before storing the section name as a dictionary key.

**Convention-aware task enrichment — lookup**:

```python
if convention_name in discovered_conventions:
    notes.append(f"Per CONVENTIONS.md {convention_name}: {action}")
```

This lookup uses exact string comparison. When the key has trailing whitespace from the
extraction step, the match fails.

### Existing test coverage

**File**: `evals/plan-feature/files/conventions-mock.md`

The existing eval fixture for plan-feature conventions does **not** include trailing whitespace
on headings. This edge case is not covered by current evals, which is why the bug was not
caught before release.

### CONVENTIONS.md lookup

The repository does not have a `CONVENTIONS.md` at its root. No conventions to inform the
generated task's Implementation Notes from this source.

### Reuse candidates

- The heading extraction logic in `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` is
  the primary code to modify.
- The existing eval fixture `evals/plan-feature/files/conventions-mock.md` should be
  extended or a new fixture created to cover trailing whitespace edge cases.

### Summary of findings

| Item | Detail |
|------|--------|
| **Root cause location** | `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` — heading extraction logic |
| **Defect** | `line[3:]` does not strip trailing whitespace from convention headings |
| **Impact** | Silent convention drop — no warning, no error, conventions with trailing whitespace in headings are silently ignored |
| **Test gap** | Existing eval fixture lacks trailing whitespace test cases |
| **Single root cause** | Yes — one defect in one location, no decomposition needed |
