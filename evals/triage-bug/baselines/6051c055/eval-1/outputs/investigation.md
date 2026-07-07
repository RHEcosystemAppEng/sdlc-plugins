# Codebase Investigation — ACME-500

## Step 2 — Reproduce/Trace

### Code-path tracing

This bug cannot be directly reproduced (it involves a skill invocation and convention lookup logic). Tracing through the relevant code paths:

1. **Entry point**: The user invokes `/plan-feature ACME-100` on a feature that requires a database migration.
2. **Convention loading**: The plan-feature skill reads `CONVENTIONS.md` and extracts section headings using line-by-line parsing.
3. **Heading extraction** (in `plugins/sdlc-workflow/skills/plan-feature/SKILL.md`):
   ```python
   for line in conventions_content.split('\n'):
       if line.startswith('## '):
           section_name = line[3:]  # Extracts heading text after "## "
           conventions[section_name] = current_section_content
   ```
   The extraction `line[3:]` takes everything after `## ` but does NOT strip trailing whitespace. When the heading line is `## Migration Patterns  \n` (with trailing spaces), the extracted section name becomes `"Migration Patterns  "` (with two trailing spaces).

4. **Convention-aware task enrichment**: The task enrichment step matches conventions by section name:
   ```python
   if convention_name in discovered_conventions:
       notes.append(f"Per CONVENTIONS.md {convention_name}: {action}")
   ```
   This lookup uses the clean name `"Migration Patterns"` as the key, which does NOT match `"Migration Patterns  "` (with trailing spaces) in the `discovered_conventions` dict. The match fails silently -- no warning is logged.

5. **Divergence point**: The behavior diverges at the heading extraction step (`line[3:]`). The expected behavior is that trailing whitespace on heading lines is ignored. The actual behavior is that trailing whitespace is preserved in the dictionary key, causing downstream exact-match comparisons to fail.

### Trace outcome

Bug confirmed via code-path tracing. The root cause is the missing `.strip()` call on the heading extraction line.

## Step 3 — Codebase Investigation

### Target repository

The bug affects the **sdlc-plugins** repository (component: sdlc-workflow). From the Repository Registry:

| Repository | Role | Serena Instance | Path |
|---|---|---|---|
| acme-backend | Rust backend service | serena_backend | /home/dev/repos/acme-backend |

### Affected files and symbols

1. **`plugins/sdlc-workflow/skills/plan-feature/SKILL.md`** — Convention conformance analysis section
   - **Heading extraction**: `section_name = line[3:]` does not strip trailing whitespace
   - **Convention-aware task enrichment**: `if convention_name in discovered_conventions` uses exact-match comparison that fails when keys have trailing whitespace

### Existing test coverage

- **`evals/plan-feature/files/conventions-mock.md`** — Existing eval fixture for plan-feature conventions does NOT include trailing whitespace on headings. This edge case is not covered by current evals.

### CONVENTIONS.md lookup

The repository does not have a CONVENTIONS.md at its root. No conventions to incorporate into the task's Implementation Notes.

### Investigation summary

- **Root cause location**: `plugins/sdlc-workflow/skills/plan-feature/SKILL.md`, convention conformance analysis section, heading extraction logic
- **Defect**: `line[3:]` does not call `.strip()` to remove trailing whitespace
- **Impact**: Any `CONVENTIONS.md` heading with trailing whitespace will be silently dropped from generated task descriptions
- **Existing tests**: No coverage for trailing-whitespace edge case in convention headings
- **Reusable patterns**: The existing eval fixture `evals/plan-feature/files/conventions-mock.md` can be extended with a trailing-whitespace variant for the reproducer test
