# Codebase Investigation — Steps 2-3

## Step 2 — Reproduce/Trace

### Code-path tracing

This bug cannot be directly reproduced via runnable commands (it involves a skill invocation). Tracing through the relevant code paths instead.

**Entry point**: The `/plan-feature` skill invocation, specifically the convention conformance analysis phase that reads `CONVENTIONS.md` headings.

**Trace findings**:

1. The plan-feature skill reads `CONVENTIONS.md` and iterates over lines to extract section headings.
2. The heading extraction logic is:
   ```python
   for line in conventions_content.split('\n'):
       if line.startswith('## '):
           section_name = line[3:]  # Extracts heading text after "## "
           conventions[section_name] = current_section_content
   ```
3. The extraction `line[3:]` takes the substring starting at index 3 to the end of the line. This does **not** strip trailing whitespace.
4. When the heading line is `## Migration Patterns  \n` (with trailing spaces), the extracted `section_name` becomes `"Migration Patterns  "` (with two trailing spaces).
5. Later, the convention-aware task enrichment step matches conventions by name:
   ```python
   if convention_name in discovered_conventions:
       notes.append(f"Per CONVENTIONS.md {convention_name}: {action}")
   ```
6. This match fails because `"Migration Patterns"` (the expected name, without trailing spaces) does not match `"Migration Patterns  "` (the extracted name, with trailing spaces).
7. The convention is silently skipped — no warning or error is logged.

**Reproduction outcome**: Confirmed via code-path trace. The behavior described in the bug report is consistent with the code.

## Step 3 — Codebase Investigation

### Target Repository

- **Repository**: acme-backend (identified from Component: sdlc-workflow and code paths)
- **Serena Instance**: serena_backend (from Repository Registry, but Code Intelligence section notes no Serena MCP servers are configured)
- **Path**: /home/dev/repos/acme-backend

Since no Serena instance is available, investigation uses Read/Grep/Glob fallback.

### Affected Files and Symbols

| File | Symbol / Location | Role |
|------|-------------------|------|
| `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` | Convention conformance analysis — heading extraction (`line[3:]`) | **Root cause**: extracts heading text without stripping trailing whitespace |
| `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` | Convention-aware task enrichment — name matching (`convention_name in discovered_conventions`) | **Failure point**: exact-match comparison fails due to trailing whitespace in extracted name |

### Root Cause Location

The defect is in the plan-feature skill's convention lookup logic, specifically the heading extraction at `line[3:]`. This line slices the heading text from position 3 onward but does not call `.strip()` or `.rstrip()` to remove trailing whitespace.

### Existing Test Coverage

- **Existing eval fixture**: `evals/plan-feature/files/conventions-mock.md` — this fixture does NOT include trailing whitespace on headings, so the edge case is not covered.
- **No test exists** for the trailing-whitespace scenario.

### CONVENTIONS.md Lookup

The repository does not have a `CONVENTIONS.md` at its root. No conventions to reference in the generated task's Implementation Notes from this repository.

### Investigation Summary

- **What is broken**: Heading extraction in the plan-feature convention lookup uses `line[3:]` which does not strip trailing whitespace from headings.
- **Where it is broken**: `plugins/sdlc-workflow/skills/plan-feature/SKILL.md`, convention conformance analysis section.
- **Why it is broken**: The `line[3:]` slice includes all characters after `## `, including any trailing spaces or tabs. The subsequent exact-match comparison against expected convention names fails when whitespace is present.
- **Impact**: Any `CONVENTIONS.md` heading with trailing whitespace causes that convention to be silently dropped from generated task descriptions. No warning is emitted.
