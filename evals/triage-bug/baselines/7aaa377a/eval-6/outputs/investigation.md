# Step 2–3 – Codebase Investigation: ACME-500

## Step 2 – Reproduce / Trace

The bug does not involve runnable CLI commands against a live service — it is a
skill-logic bug where a text-parsing step in the `plan-feature` skill silently
discards convention sections from `CONVENTIONS.md` when their headings carry trailing
whitespace.

### Code-path tracing

**Entry point**: invocation of `/plan-feature ACME-100` (as described in Steps to Reproduce).

The plan-feature skill reads `CONVENTIONS.md` and extracts section headings.
The trace follows the heading extraction through to the task enrichment step:

1. The skill iterates over lines in `CONVENTIONS.md`.
2. For each line starting with `## `, it extracts the section name via `line[3:]`.
3. The extracted name is used as a key in a `conventions` dictionary.
4. In the task enrichment step, a lookup `if convention_name in discovered_conventions:` is
   performed to decide whether to include the convention in Implementation Notes.

**Divergence point**: when the heading line is `## Migration Patterns  \n` (with trailing spaces
followed by a newline), `line[3:]` yields `"Migration Patterns  "` (retaining the trailing
spaces). The enrichment step then compares this against the expected key `"Migration Patterns"`
— an exact-match failure. The convention is not appended to the notes, and no error is raised.

**Reproduction confirmed by trace**: the bug is deterministic and reproducible whenever a
CONVENTIONS.md heading has trailing whitespace.

---

## Step 3 – Codebase Investigation

### Target repository identification

- **Component**: sdlc-workflow
- **Repository Registry entry**: `acme-backend` → Path: `/home/dev/repos/acme-backend`
- **Code Intelligence**: No Serena MCP servers configured → using Read/Grep/Glob fallback

### No Serena — direct file inspection

**File investigated**: `plugins/sdlc-workflow/skills/plan-feature/SKILL.md`

#### Convention conformance analysis — heading extraction (Section A)

```python
for line in conventions_content.split('\n'):
    if line.startswith('## '):
        section_name = line[3:]  # Extracts heading text after "## "
        conventions[section_name] = current_section_content
```

**Finding**: `line[3:]` slices the heading text without any whitespace normalization.
When the source line contains trailing spaces before the newline (e.g., `## Migration Patterns  `),
the resulting `section_name` is `"Migration Patterns  "` — with two trailing spaces preserved.
This corrupted key is stored in the `conventions` dictionary.

#### Convention-aware task enrichment — section match (Section B)

```python
if convention_name in discovered_conventions:
    notes.append(f"Per CONVENTIONS.md §{convention_name}: {action}")
```

**Finding**: This exact-string lookup fails because the stored key is `"Migration Patterns  "`
while the expected lookup key is `"Migration Patterns"`. The condition evaluates to `False`,
so the convention line is never appended to `notes`. No exception is raised; the silent skip
is the bug.

### Existing test coverage

**File**: `evals/plan-feature/files/conventions-mock.md`

The existing eval fixture for plan-feature convention analysis does NOT include heading lines
with trailing whitespace. The trailing-whitespace edge case is therefore **uncovered** by the
current test suite.

### CONVENTIONS.md lookup

The repository has **no `CONVENTIONS.md`** at its root. No additional conventions apply to
the fix.

### Persistence-impact analysis

The bug is confined to skill/text-processing logic within a Markdown-based skill definition.
The convention lookup result is used only at skill invocation time to compose a task
description string — it is **not written to a database, file, or any persistent store**.
Each invocation recomputes the lookup fresh from the current `CONVENTIONS.md` content.

**Persistence boundary**: not found.
**Data migration**: not required. Fixing the extraction logic will correct all future
plan-feature invocations immediately, with no residual stale data.

---

## Investigation Summary

| Area                | Finding                                                                                |
|---------------------|----------------------------------------------------------------------------------------|
| Affected file       | `plugins/sdlc-workflow/skills/plan-feature/SKILL.md`                                  |
| Root location       | Heading extraction loop (Section A) — `line[3:]` without `.rstrip()`                  |
| Secondary location  | Task enrichment match (Section B) — fails because key has trailing spaces              |
| Test coverage gap   | `evals/plan-feature/files/conventions-mock.md` — no trailing-whitespace fixture        |
| Persistence impact  | None — computed at invocation time only                                                |
| Decomposition       | Single root cause (missing rstrip) with two manifestation points — no decomposition needed |
