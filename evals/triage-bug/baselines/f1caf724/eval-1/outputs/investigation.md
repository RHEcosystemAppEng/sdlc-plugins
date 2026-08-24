# Codebase Investigation -- Steps 2-3

## Step 2 -- Reproduce/Trace

### Reproduction method

This bug cannot be directly reproduced via runnable commands because it involves
a skill invocation (`/plan-feature`) that requires the full Claude Code runtime.
Code-path tracing is used instead.

### Code-path trace

**Entry point**: `/plan-feature ACME-100` skill invocation

**Trace through convention conformance analysis**:

1. The plan-feature skill reads `CONVENTIONS.md` and splits it by newline.

2. For each line, it checks if the line starts with `## ` to identify section headings:
   ```python
   for line in conventions_content.split('\n'):
       if line.startswith('## '):
           section_name = line[3:]  # Extracts heading text after "## "
           conventions[section_name] = current_section_content
   ```

3. **Defect location**: The extraction `line[3:]` captures everything after `## `,
   including any trailing whitespace. When the heading line in the file is
   `## Migration Patterns  \n`, the extracted `section_name` becomes
   `"Migration Patterns  "` (with two trailing spaces).

4. Later, the convention-aware task enrichment step performs an exact-match lookup:
   ```python
   if convention_name in discovered_conventions:
       notes.append(f"Per CONVENTIONS.md  {convention_name}: {action}")
   ```

5. The lookup key `convention_name` is `"Migration Patterns"` (no trailing spaces),
   which does NOT match the stored key `"Migration Patterns  "` (with trailing spaces).
   The match fails silently -- no KeyError, no warning, no fallback.

**Divergence point**: The behavior diverges from expected at the heading extraction
step (point 3 above). The extracted name should be stripped of trailing whitespace
to match the canonical convention name used in downstream lookups.

## Step 3 -- Codebase Investigation

### Target repository

Based on the Component field (`sdlc-workflow`) and the code paths referenced in
Steps to Reproduce, the bug affects the **sdlc-plugins** repository (self).

From the Repository Registry (mock CLAUDE.md):
- Repository: acme-backend
- Serena Instance: serena_backend
- Path: /home/dev/repos/acme-backend

Note: No Serena MCP servers are actually configured (Code Intelligence section
states: "No Serena MCP servers are configured. Code intelligence is not available.").
Fallback to Read/Grep/Glob tools was used.

### Affected files and symbols

| File | Symbol/Location | Role |
|------|----------------|------|
| `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` | Convention conformance analysis -- heading extraction loop | Extracts `section_name = line[3:]` without stripping whitespace |
| `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` | Convention-aware task enrichment | Performs exact-match lookup `convention_name in discovered_conventions` |

### Specific defect

- **File**: `plugins/sdlc-workflow/skills/plan-feature/SKILL.md`
- **Symbol**: Convention conformance analysis, heading extraction logic
- **Line**: `section_name = line[3:]`
- **Issue**: Missing `.strip()` (or `.rstrip()`) call on the extracted heading text

### Existing test coverage

- **Existing fixture**: `evals/plan-feature/files/conventions-mock.md` -- does NOT include
  trailing whitespace on headings, so this edge case is not covered by current evals.
- **No reproducer test exists** for the trailing-whitespace scenario.

### CONVENTIONS.md lookup

The repository does not have a `CONVENTIONS.md` at its root. No additional conventions
to inform the task's Implementation Notes.

### Persistence-impact analysis

**No persistence boundary found.** The output of the convention conformance analysis
is used to generate task descriptions that are posted to Jira via API calls. The buggy
value (the missing convention reference) is not persisted to a database at ingestion
time -- it is computed at task-generation time and sent to Jira as part of the task
description content.

While the resulting Jira task descriptions created during the period this bug has been
active will be missing convention references, this is Jira content (not a database
record), and correcting it requires re-running the plan-feature skill rather than a
data migration.

**Conclusion**: No data migration is needed. Fixing the heading extraction logic will
correct all future task generations.
