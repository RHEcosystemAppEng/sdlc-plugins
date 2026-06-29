# Codebase Investigation — ACME-500

## Target Repository

- **Repository**: acme-backend
- **Role**: Rust backend service
- **Serena Instance**: serena_backend
- **Path**: /home/dev/repos/acme-backend

The **Component** field (`sdlc-workflow`) and the Steps to Reproduce (referencing `/plan-feature`) point to the `plugins/sdlc-workflow/skills/plan-feature/` code path.

## Code Intelligence Limitations

Per CLAUDE.md Code Intelligence section: "No Serena MCP servers are configured. Code intelligence is not available." Falling back to Read/Grep/Glob for investigation.

## Step 2 — Reproduce/Trace

This bug cannot be directly reproduced via CLI because it involves a skill invocation (`/plan-feature`) with a specific CONVENTIONS.md configuration. Code-path tracing was performed instead.

### Trace Findings

**Entry point**: The `/plan-feature` skill reads `CONVENTIONS.md` to discover project conventions for task enrichment.

**Convention extraction logic** (in `plugins/sdlc-workflow/skills/plan-feature/SKILL.md`):

```python
for line in conventions_content.split('\n'):
    if line.startswith('## '):
        section_name = line[3:]  # Extracts heading text after "## "
        conventions[section_name] = current_section_content
```

The `line[3:]` slice extracts everything after `## ` but does NOT call `.strip()` on the result. When a heading line contains trailing whitespace (e.g., `## Migration Patterns  \n`), the extracted section name becomes `"Migration Patterns  "` (with trailing spaces).

**Convention matching logic** (in the task enrichment step):

```python
if convention_name in discovered_conventions:
    notes.append(f"Per CONVENTIONS.md §{convention_name}: {action}")
```

This performs an exact dictionary lookup. When the key is `"Migration Patterns  "` (with trailing spaces) but the lookup uses `"Migration Patterns"` (clean), the match fails silently.

**Reproduction outcome**: Confirmed via code-path trace. The bug is deterministic when CONVENTIONS.md headings contain trailing whitespace.

## Step 3 — Codebase Investigation

### Affected Files and Symbols

| File | Symbol/Location | Issue |
|------|----------------|-------|
| `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` | Convention heading extraction (`line[3:]`) | Missing `.strip()` on extracted heading text |
| `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` | Convention-aware task enrichment (dictionary lookup) | Exact-match fails on whitespace-padded keys |

### Existing Tests

- `evals/plan-feature/files/conventions-mock.md` — The existing eval fixture does NOT include trailing whitespace on headings, so this edge case is not covered by current evals.

### CONVENTIONS.md Lookup

The repository does not have a `CONVENTIONS.md` at its root. No conventions apply to the fix task.

### Reuse Candidates

No existing utility functions for heading extraction or whitespace normalization were found in the codebase. The fix is localized to the heading extraction line.

### Investigation Summary

The bug has a single root cause: the heading extraction code at `line[3:]` does not strip trailing whitespace. This causes the convention dictionary to store keys with trailing spaces, which then fail exact-match lookups during task enrichment. The failure is silent — no warning or error is logged when a convention is not matched.
