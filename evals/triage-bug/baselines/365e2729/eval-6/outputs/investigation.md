# Steps 2–3 – Reproduce/Trace and Codebase Investigation: ACME-500

## Step 2 – Reproduce/Trace

### Runnable reproduction

The Steps to Reproduce depend on a skill invocation (`/plan-feature ACME-100`) that needs
live Jira and LLM execution. They are not a deterministic CLI or test command, so a
read-only runnable reproduction is not possible. Outcome: **not directly reproducible —
code-path tracing used instead.**

### Code-path trace

1. **Entry point:** `/plan-feature ACME-100` → `plugins/sdlc-workflow/skills/plan-feature/SKILL.md`.
2. **Convention lookup:** the skill reads the target repo's `CONVENTIONS.md` and splits it by
   line. Any line starting with `## ` becomes a section key:
   ```python
   for line in conventions_content.split('\n'):
       if line.startswith('## '):
           section_name = line[3:]  # no .strip()/.rstrip()
           conventions[section_name] = current_section_content
   ```
   With input `## Migration Patterns  `, the key becomes `"Migration Patterns  "` (two trailing spaces).
3. **Convention-aware task enrichment:** the enrichment step looks up conventions by exact name:
   ```python
   if convention_name in discovered_conventions:
       notes.append(f"Per CONVENTIONS.md §{convention_name}: {action}")
   ```
   `"Migration Patterns" in {"Migration Patterns  ": ...}` → `False`.
4. **Point of divergence:** the lookup misses, and there is no `else` branch or warning, so
   the convention is skipped without any message. The Implementation Notes leave out the
   `Index::create()` guidance (the Actual Result). The expected behaviour needs the key to be
   `"Migration Patterns"`.

## Step 3 – Codebase Investigation

### Target repository

- Component `sdlc-workflow` and the trace both point to the plan-feature skill.
- Repository Registry entry: **acme-backend**, Serena instance `serena_backend`, path
  `/home/dev/repos/acme-backend`.
- The Code Intelligence section says "No Serena MCP servers are configured", so the fallback
  applies (Read/Grep/Glob at the registry path). For this eval, findings come from the
  mock repository context (`repo-context-mock.md`). No live Serena or Grep calls were made.

### Affected files and symbols

| File | Location / Symbol | Role in bug |
|---|---|---|
| `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` | Convention conformance analysis (heading extraction `section_name = line[3:]`) | **Defect.** The heading text is not stripped of trailing whitespace before it is used as a dictionary key. |
| `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` | Convention-aware task enrichment (`if convention_name in discovered_conventions`) | Consumer. The exact-match lookup fails on the whitespace-polluted keys, and the miss produces no warning. |

### Impact analysis (referencing consumers)

- The extracted `conventions` map feeds only the task-enrichment step in the same skill.
  That step is the only consumer found in the provided context.
- Any convention heading with trailing whitespace (spaces or tabs, and `\r` from CRLF files,
  which `split('\n')` leaves at the end of the line) is affected. So the defect is wider than
  `Migration Patterns`: every section in a CRLF-encoded `CONVENTIONS.md` would be dropped.

### Existing tests / fixtures

- `evals/plan-feature/files/conventions-mock.md`: the existing plan-feature conventions eval
  fixture. Its headings have **no** trailing whitespace, so this edge case is not covered
  today. It is the natural pattern to copy for a reproducer fixture.
- Eval assertions for plan-feature live in `evals/plan-feature/evals.json` (the same structure
  as the other skill eval suites in the repo). A new eval case can be added there.

### Reusable utilities / patterns

- Normalise the heading with standard string trimming (`.strip()` / `.rstrip()`) at
  extraction time. No new helper is needed.
- The existing eval fixture format (`evals/plan-feature/files/*.md` + `evals.json`
  assertions) is the pattern for the reproducer.

### CONVENTIONS.md lookup

The target repository has **no** `CONVENTIONS.md` at its root, so no repo-specific
conventions apply to the Implementation Notes.

### Persistence-impact analysis

- The buggy output is an in-memory conventions dictionary used during plan-feature execution
  to write task description text. It is never written to a database table. The generated
  Jira task is the only artifact.
- **No persistence boundary found.** No data migration is needed. Tasks generated earlier
  with missing conventions are not self-correcting, but fixing them means re-running
  plan-feature (or editing those tasks by hand). A schema or data migration would not help,
  and that work is out of scope for this fix.

### Decomposition Guard (Step 6) check

There is a single root cause: unstripped heading extraction. The silent-miss behaviour in
the enrichment step is part of the same defect and lives in the same file. **No
decomposition needed.** One Task is appropriate.
