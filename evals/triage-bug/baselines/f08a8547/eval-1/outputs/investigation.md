# Steps 2-3 -- Codebase Investigation: ACME-500

## Step 2 -- Reproduce/Trace

### Reproduction method: Code-path tracing

The Steps to Reproduce reference a skill invocation (`/plan-feature ACME-100`), which cannot be directly executed as a runnable command. Code-path tracing is used instead.

### Trace findings

**Entry point:** `/plan-feature` skill invocation with a feature issue that requires database migration conventions.

**Trace path:**

1. The plan-feature skill reads `CONVENTIONS.md` and parses convention section headings using a line-by-line loop:

   ```python
   for line in conventions_content.split('\n'):
       if line.startswith('## '):
           section_name = line[3:]  # Extracts heading text after "## "
           conventions[section_name] = current_section_content
   ```

2. The heading extraction at `line[3:]` does NOT call `.strip()` on the result. When the source line is `## Migration Patterns  \n`, the extracted `section_name` becomes `"Migration Patterns  "` (with two trailing spaces).

3. The convention-aware task enrichment step later matches conventions by exact string comparison:

   ```python
   if convention_name in discovered_conventions:
       notes.append(f"Per CONVENTIONS.md {convention_name}: {action}")
   ```

4. The expected key `"Migration Patterns"` does not match the stored key `"Migration Patterns  "` due to trailing whitespace. The lookup silently returns no match.

5. No warning or error is emitted when a convention is expected but not found. The convention is silently omitted from the generated task.

**Trace conclusion:** The bug is confirmed through code-path analysis. The root cause is the missing `.strip()` call on the extracted heading text.

## Step 3 -- Codebase Investigation

### Target repository

Based on the Component field (sdlc-workflow) and the code paths referenced in the bug, the target repository is **acme-backend** from the Repository Registry.

- **Serena Instance:** serena_backend
- **Path:** /home/dev/repos/acme-backend

Note: Code Intelligence section states "No Serena MCP servers are configured." Fallback to Read/Grep/Glob is used.

### Affected files and symbols

| File | Symbol/Section | Role |
|------|---------------|------|
| `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` | Convention conformance analysis (heading extraction) | Contains the `line[3:]` extraction without `.strip()` |
| `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` | Convention-aware task enrichment | Contains the `if convention_name in discovered_conventions` exact match |

### Code path analysis

1. **Heading extraction** (`plugins/sdlc-workflow/skills/plan-feature/SKILL.md`):
   - The loop `for line in conventions_content.split('\n')` iterates over CONVENTIONS.md content
   - `line.startswith('## ')` correctly identifies heading lines
   - `section_name = line[3:]` extracts the heading text but preserves trailing whitespace
   - The extracted name is used as a dictionary key in `conventions[section_name]`

2. **Convention matching** (`plugins/sdlc-workflow/skills/plan-feature/SKILL.md`):
   - The enrichment step uses `if convention_name in discovered_conventions` for lookup
   - This is an exact string match against dictionary keys
   - Trailing whitespace in the key causes the match to fail silently

### Existing test coverage

- **`evals/plan-feature/files/conventions-mock.md`**: The existing eval fixture for plan-feature conventions does NOT include trailing whitespace on headings. This edge case is not covered by current evals.

### CONVENTIONS.md lookup

The repository does not have a `CONVENTIONS.md` file at its root. No project-level conventions apply to the fix task.

### Persistence-impact analysis

The buggy function's output (convention section names stored as dictionary keys) is used to generate Jira task descriptions at task-creation time. Tracing the output:

1. `section_name` is stored as a key in the `conventions` dictionary (in-memory)
2. The dictionary is queried during task enrichment to build Implementation Notes text
3. The enriched text is passed to `jira.create_issue` as part of the task description

**No persistence boundary found.** The convention data is computed at task-generation time and used to compose Jira issue content via the API. It is not written to a local database. Incorrect convention lookups produce incomplete task descriptions in Jira, but no database migration is needed -- fixing the code corrects all future task generations. Previously generated tasks with missing conventions are already persisted in Jira and would need manual review if correction is desired, but this falls outside the scope of a code fix.
