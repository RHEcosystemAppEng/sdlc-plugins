# Steps 2–3 — Reproduce/Trace and Codebase Investigation: ACME-500

## Step 2 — Reproduce / Trace

### Runnable reproduction
The Steps to Reproduce call for a skill invocation (`/plan-feature ACME-100`) against a live Jira
feature. That is not a read-only command that can be run safely, and this eval has no external
access. **Reproduction outcome: not run directly. Code-path tracing was used instead.**

### Code-path trace
1. **Entry point:** `/plan-feature ACME-100` runs the plan-feature skill
   (`plugins/sdlc-workflow/skills/plan-feature/SKILL.md`).
2. **Convention lookup:** plan-feature reads the target repo's `CONVENTIONS.md` and builds a map
   of section name to content by scanning headings:
   ```python
   for line in conventions_content.split('\n'):
       if line.startswith('## '):
           section_name = line[3:]  # no strip()
           conventions[section_name] = current_section_content
   ```
   With the input `## Migration Patterns  `, the key becomes `"Migration Patterns  "`
   (two trailing spaces).
3. **Task enrichment:** the convention-aware task enrichment step looks up conventions by exact name:
   ```python
   if convention_name in discovered_conventions:
       notes.append(f"Per CONVENTIONS.md §{convention_name}: {action}")
   ```
   `"Migration Patterns" in {"Migration Patterns  ": ...}` is `False`, so no note is appended.
4. **Point of divergence:** the miss in step 3 has no `else` branch and no warning. The
   convention is dropped silently, which matches the Actual Result: no reference and no warning.

## Step 3 — Codebase Investigation

### Target repository
- Component `sdlc-workflow` and the code paths in the Steps to Reproduce point to the plan-feature
  skill in the sdlc-workflow plugin.
- Repository Registry entry: `acme-backend`. Serena instance `serena_backend`, path
  `/home/dev/repos/acme-backend`.
- Code Intelligence states that no Serena MCP servers are configured, so the Read/Grep/Glob
  fallback applies. In this eval the codebase is represented by `repo-context-mock.md`.

### Affected files and symbols

| File | Location / symbol | Role in bug |
|---|---|---|
| `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` | Convention conformance analysis (CONVENTIONS.md heading extraction: `section_name = line[3:]`) | **Defect origin.** The extracted heading text is not normalized, so trailing whitespace stays in the key |
| `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` | Convention-aware task enrichment (`if convention_name in discovered_conventions`) | **Defect manifestation.** The exact-match lookup fails, and the miss produces no diagnostic |

### Impact analysis
- The `conventions` / `discovered_conventions` map is used only by the task enrichment step. Any
  `CONVENTIONS.md` heading with trailing whitespace (spaces or tabs, and possibly `\r` from CRLF
  line endings, since the content is split on `'\n'` only) causes that convention to be dropped.
- All conventions are affected, not just Migration Patterns. Generated tasks lose
  repository-specific guidance without any notice.

### Existing tests and patterns
- `evals/plan-feature/files/conventions-mock.md` is the existing plan-feature conventions eval
  fixture. Its headings have **no** trailing whitespace, so this edge case is not covered.
- The reproducer should follow the existing eval-fixture pattern (`evals/<skill>/files/*.md` plus
  an eval entry in `evals/plan-feature/evals.json`).

### Reusable utilities / patterns
- No shared heading-parsing helper was found. The fix is local: normalize extracted heading
  text (`strip()` / `rstrip()`) at the extraction point, and normalize the lookup key the same way.

### CONVENTIONS.md lookup
- The target repository has **no** `CONVENTIONS.md` at its root, so there are no
  repository-specific conventions to apply to the Implementation Notes.

### Persistence-impact analysis
- The buggy output (section-name keys and the generated Implementation Notes text) is computed
  each time plan-feature runs. It is not written to a database. The only downstream effect is the
  Jira task descriptions generated during affected runs.
- **No persistence boundary found. No data migration is needed.** Tasks generated earlier that
  are missing conventions can be regenerated or edited by hand. This is outside the scope of the
  code fix.

### Decomposition Guard (Step 6) check
- There is one root cause (unnormalized heading extraction) that shows up at the lookup site.
  The missing warning is a related hardening of the same code path, not an independent defect.
  **No decomposition needed. A single Task is appropriate.**
