# Codebase Investigation — ACME-500

## Target Repository

Based on the Component field (`sdlc-workflow`) and the code paths referenced in Steps to Reproduce (plan-feature skill, CONVENTIONS.md lookup), the target repository is:

- **Repository**: acme-backend
- **Serena Instance**: serena_backend
- **Path**: /home/dev/repos/acme-backend

## CONVENTIONS.md Lookup

The repository does not have a `CONVENTIONS.md` at its root. No additional conventions to inform Implementation Notes.

## Code Path Tracing

### Entry Point

The bug is triggered by running `/plan-feature ACME-100`, which invokes the plan-feature skill. During plan-feature's convention conformance analysis step, it reads the project's `CONVENTIONS.md` file and extracts section headings.

### Code Path 1: Heading Extraction (Root Cause Location)

**File**: `plugins/sdlc-workflow/skills/plan-feature/SKILL.md`
**Section**: Convention conformance analysis

```python
for line in conventions_content.split('\n'):
    if line.startswith('## '):
        section_name = line[3:]  # Extracts heading text after "## "
        conventions[section_name] = current_section_content
```

**Finding**: The heading extraction uses `line[3:]` to get the text after `## `. This slicing operation preserves any trailing whitespace present on the line. When a `CONVENTIONS.md` heading has trailing spaces (e.g., `## Migration Patterns  `), the extracted `section_name` becomes `"Migration Patterns  "` (with two trailing spaces) instead of `"Migration Patterns"`.

This is the **root cause** of the bug. The `line[3:]` expression does not call `.strip()` or `.rstrip()` to remove trailing whitespace.

### Code Path 2: Convention-Aware Task Enrichment (Failure Manifestation)

**File**: `plugins/sdlc-workflow/skills/plan-feature/SKILL.md`
**Section**: Convention-aware task enrichment

```python
if convention_name in discovered_conventions:
    notes.append(f"Per CONVENTIONS.md §{convention_name}: {action}")
```

**Finding**: The task enrichment step performs an exact-match lookup of `convention_name` against the `discovered_conventions` dictionary. When the key was stored with trailing whitespace (`"Migration Patterns  "`), the lookup for `"Migration Patterns"` (without trailing whitespace) fails silently. No warning or error is raised — the convention is simply not found, so the task's Implementation Notes omit it entirely.

### Silent Failure Analysis

The bug is particularly impactful because:
1. No exception is raised — the dictionary lookup simply returns no match.
2. No warning is logged — the code does not check for near-misses or report unmatched conventions.
3. The user sees no indication that a convention was skipped — the generated task appears complete but is missing convention guidance.

## Test Coverage Gap

### Existing test: `evals/plan-feature/files/conventions-mock.md`

The existing eval fixture for plan-feature conventions does **not** include trailing whitespace on headings. This means the trailing-whitespace edge case is entirely uncovered by current evals. A reproducer test must create a conventions fixture with trailing whitespace on at least one heading to expose the bug.

## Summary of Findings

| Aspect | Detail |
|--------|--------|
| **Root cause file** | `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` |
| **Root cause code** | `section_name = line[3:]` — missing `.strip()` |
| **Failure point** | Convention name exact-match lookup in task enrichment |
| **Symptom** | Convention silently dropped from generated task Implementation Notes |
| **Existing test gap** | `evals/plan-feature/files/conventions-mock.md` has no trailing-whitespace headings |
