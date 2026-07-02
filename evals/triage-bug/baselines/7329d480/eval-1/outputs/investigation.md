# Codebase Investigation — ACME-500

## Step 2 — Reproduce/Trace

### Reproduction approach

This bug involves the plan-feature skill's behavior when processing CONVENTIONS.md files. It cannot be directly reproduced via runnable commands (it is a skill/convention-parsing bug), so code-path tracing is used.

### Code-path trace

**Entry point**: `/plan-feature ACME-100` invocation triggers the plan-feature skill, which reads CONVENTIONS.md to discover project conventions for inclusion in generated task descriptions.

**Trace findings**:

1. The plan-feature skill reads `CONVENTIONS.md` and splits it into lines.
2. For each line starting with `## `, it extracts the heading text using `line[3:]`.
3. If the heading line contains trailing whitespace (e.g., `## Migration Patterns  \n`), the extracted section name becomes `"Migration Patterns  "` (with trailing spaces).
4. During task enrichment, the skill attempts an exact match: `if convention_name in discovered_conventions`.
5. The lookup key `"Migration Patterns"` (without trailing spaces) does not match the stored key `"Migration Patterns  "` (with trailing spaces).
6. The match fails silently — no warning is emitted, and the convention is simply omitted from the generated task.

**Reproduction outcome**: Confirmed via trace. The behavior described in the bug report matches the code path analysis.

## Step 3 — Codebase Investigation

### Target repository

- **Repository**: acme-backend
- **Serena Instance**: serena_backend
- **Path**: /home/dev/repos/acme-backend

The bug affects the `sdlc-workflow` component, specifically the plan-feature skill's convention conformance analysis.

### Affected files and symbols

#### File: `plugins/sdlc-workflow/skills/plan-feature/SKILL.md`

**Convention heading extraction** (convention lookup section):

```python
for line in conventions_content.split('\n'):
    if line.startswith('## '):
        section_name = line[3:]  # BUG: Does NOT strip trailing whitespace
        conventions[section_name] = current_section_content
```

The defect is at `line[3:]` — this slices the heading text after `## ` but does not call `.strip()` or `.rstrip()` to remove trailing whitespace. When the heading line is `## Migration Patterns  \n`, the extracted name is `"Migration Patterns  "`.

**Convention-aware task enrichment** (task enrichment section):

```python
if convention_name in discovered_conventions:
    notes.append(f"Per CONVENTIONS.md §{convention_name}: {action}")
```

This performs an exact match against the keys in `discovered_conventions`. The lookup fails because `"Migration Patterns"` != `"Migration Patterns  "`.

### Existing test coverage

**File**: `evals/plan-feature/files/conventions-mock.md`

The existing eval fixture for plan-feature conventions does NOT include trailing whitespace on headings. This edge case is not covered by current evals.

### CONVENTIONS.md lookup

The repository (acme-backend) does not have a `CONVENTIONS.md` at its root. No project conventions apply to the fix task.

### Reuse candidates

No existing utility functions for whitespace-safe heading extraction were found. The fix will need to modify the extraction logic directly.

### Investigation summary

| Item | Detail |
|---|---|
| Defect location | `plugins/sdlc-workflow/skills/plan-feature/SKILL.md`, convention lookup section |
| Defect type | Missing whitespace normalization in heading extraction |
| Root symbol | `line[3:]` — heading text extraction without `.strip()` |
| Silent failure | No warning logged when convention match fails |
| Test gap | Existing eval fixtures lack trailing whitespace on headings |
