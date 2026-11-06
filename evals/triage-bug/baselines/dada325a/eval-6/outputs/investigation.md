# Steps 2–3 – Reproduce/Trace and Codebase Investigation: ACME-500

## Step 2 – Reproduce/Trace

### Runnable reproduction
Not attempted. The Steps to Reproduce invoke a Claude Code skill (`/plan-feature ACME-100`), which needs Jira and an LLM session, and the eval rules forbid external tool calls. Outcome: **environment-dependent**, so code-path tracing was used instead.

### Code-path trace
1. **Entry point**: `/plan-feature ACME-100` → `plugins/sdlc-workflow/skills/plan-feature/SKILL.md`.
2. **Convention lookup** (convention conformance analysis): the skill reads the target repository's `CONVENTIONS.md` and builds a map from section heading to section content:
   ```python
   for line in conventions_content.split('\n'):
       if line.startswith('## '):
           section_name = line[3:]  # Extracts heading text after "## "
           conventions[section_name] = current_section_content
   ```
   With the input `## Migration Patterns  `, `section_name` becomes `"Migration Patterns  "`, which keeps the two trailing spaces.
3. **Task enrichment** (convention-aware task enrichment): conventions are looked up by exact name:
   ```python
   if convention_name in discovered_conventions:
       notes.append(f"Per CONVENTIONS.md §{convention_name}: {action}")
   ```
   The lookup key `"Migration Patterns"` is not equal to the stored key `"Migration Patterns  "`, so the membership test is False and no note is added.
4. **Divergence point**: heading extraction at `line[3:]` in the convention lookup. It does not normalize whitespace. Because there is no `else`/warning branch, the miss produces no output, which matches the Actual Result ("silently dropped, no warning").

## Step 3 – Codebase Investigation

### Target repository
- Component `sdlc-workflow` and the file paths in the repo context point to the plan-feature skill.
- Registry entry: **acme-backend** (Serena instance `serena_backend`, path `/home/dev/repos/acme-backend`).
- Code Intelligence: no Serena instances are configured, so the fallback is Read/Grep/Glob (simulated here from repo-context-mock.md).

### Affected files and symbols

| File | Location / symbol | Role in bug |
|---|---|---|
| `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` | Convention conformance analysis: heading parsing loop (`section_name = line[3:]`) | **Defect.** Stores heading keys without stripping trailing whitespace. |
| `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` | Convention-aware task enrichment (`if convention_name in discovered_conventions`) | Consumer. Exact-match lookup fails on the polluted key and gives no warning on a miss. |

### Impact analysis
- Every consumer of the `conventions` / `discovered_conventions` map is affected. Any heading with trailing spaces or tabs (and possibly `\r` from CRLF line endings, because the split is only on `\n`) will never match.
- The defect is limited to the plan-feature convention lookup. No other module is involved, so this is a **single root cause** and the Decomposition Guard (Step 6) is not triggered.

### Existing tests / fixtures
- `evals/plan-feature/files/conventions-mock.md` is the existing plan-feature conventions eval fixture. Its headings have **no** trailing whitespace, so current evals do not cover this edge case.
- The reproducer should be a new or extended plan-feature eval fixture whose CONVENTIONS.md heading has trailing whitespace (`## Migration Patterns  `), plus an eval assertion.

### Reusable patterns
- The existing eval layout (`evals/plan-feature/evals.json` plus fixtures under `evals/plan-feature/files/`) is the pattern to follow when adding the reproducer case.
- The usual normalization idiom (`.strip()` / `.rstrip()` on the heading text) is enough. No new helper is needed.

### CONVENTIONS.md lookup
- The target repository has **no** `CONVENTIONS.md` at its root, so no repo-specific conventions apply to the Implementation Notes.

### Persistence-impact analysis
- The buggy output (a convention-name map) lives only in memory while plan-feature runs and goes into generated task text. Nothing writes it to a database.
- **No persistence boundary found.** No data migration is needed. Jira tasks generated earlier may lack the convention, but they are not database records this fix should correct. At most, a note can suggest re-checking recently planned tasks.

## Step 6 – Decomposition Guard check
One defect (missing whitespace normalization in heading extraction) causes the whole bug. Not triggered.
