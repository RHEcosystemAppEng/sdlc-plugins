# Investigation — ACME-500

## Step 2 — Reproduce/Trace

### Code-path tracing

The bug involves the plan-feature skill's convention conformance analysis. This is a skill/documentation-level bug — direct reproduction requires running the skill against a Jira issue — so we trace through the relevant code paths instead.

**Entry point**: `/plan-feature ACME-100` invocation

**Trace through convention lookup**:

1. The plan-feature skill reads `CONVENTIONS.md` and parses headings to extract convention sections.
2. The heading extraction logic is:
   ```python
   for line in conventions_content.split('\n'):
       if line.startswith('## '):
           section_name = line[3:]  # Extracts heading text after "## "
           conventions[section_name] = current_section_content
   ```
3. When the heading line is `## Migration Patterns  \n`, `line[3:]` extracts `"Migration Patterns  "` (with trailing spaces).
4. The `line[3:]` slice does **NOT** strip trailing whitespace — it preserves whatever characters follow `## `.

**Trace through convention matching**:

5. The task enrichment step later matches conventions by name:
   ```python
   if convention_name in discovered_conventions:
       notes.append(f"Per CONVENTIONS.md §{convention_name}: {action}")
   ```
6. The lookup uses `convention_name = "Migration Patterns"` (clean, without trailing whitespace).
7. The dictionary key is `"Migration Patterns  "` (with trailing spaces from extraction).
8. The exact-match comparison `"Migration Patterns" in discovered_conventions` **fails silently** — no KeyError, no warning, just a missed match.

**Divergence point**: The actual behavior diverges from expected at the heading extraction step (step 3 above). The extracted section name includes trailing whitespace, causing all subsequent exact-match lookups to fail.

**Reproduction outcome**: Confirmed via code-path tracing. The bug is deterministic — any `CONVENTIONS.md` heading with trailing whitespace will be silently dropped.

## Step 3 — Codebase Investigation

### Target repository

- **Repository**: acme-backend (from Repository Registry)
- **Component**: sdlc-workflow (from Bug issue)
- **Serena Instance**: serena_backend
- **Path**: /home/dev/repos/acme-backend

### Affected files and symbols

| File | Symbol/Location | Role |
|------|----------------|------|
| `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` | Convention conformance analysis — heading extraction (`line[3:]`) | **Root cause**: extracts heading text without stripping whitespace |
| `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` | Convention-aware task enrichment — name matching (`convention_name in discovered_conventions`) | **Failure point**: exact-match lookup fails due to trailing whitespace in key |

### Existing test coverage

- **Existing fixture**: `evals/plan-feature/files/conventions-mock.md` — this fixture does **not** include trailing whitespace on headings, so the edge case is not covered by current evals.
- **Coverage gap**: No test exercises the trailing-whitespace-on-heading scenario.

### CONVENTIONS.md lookup

The repository does not have a `CONVENTIONS.md` file at its root. No repository-level conventions apply to the fix task.

### Key findings

1. The root cause is isolated to a single code path: heading extraction in plan-feature's convention lookup.
2. The fix is straightforward: apply `.strip()` to the extracted heading text.
3. The silent failure (no warning logged) makes this bug difficult to detect in practice.
4. Existing test fixtures need to be augmented with trailing-whitespace variants.
