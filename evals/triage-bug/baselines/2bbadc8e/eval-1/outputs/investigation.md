# Steps 2-3 -- Codebase Investigation: ACME-500

## Step 2 -- Reproduce/Trace

### Reproduction method: Code-path tracing

This bug involves a skill's internal logic for processing CONVENTIONS.md headings, which
cannot be directly reproduced via CLI commands. Code-path tracing is the appropriate
approach.

### Trace findings

**Entry point**: `/plan-feature ACME-100` invocation triggers the plan-feature skill.

**Trace path**:

1. The plan-feature skill reads the target repository's `CONVENTIONS.md` file.
2. Convention heading extraction iterates over lines, looking for `## ` prefixed lines:
   ```python
   for line in conventions_content.split('\n'):
       if line.startswith('## '):
           section_name = line[3:]  # Extracts heading text after "## "
           conventions[section_name] = current_section_content
   ```
3. When the heading line is `## Migration Patterns  \n` (with trailing whitespace),
   `line[3:]` extracts `"Migration Patterns  "` (preserving the trailing spaces).
4. The extracted section name is stored in the `conventions` dictionary with the
   trailing whitespace intact.

**Divergence point**: The convention-aware task enrichment step performs an exact match:
   ```python
   if convention_name in discovered_conventions:
       notes.append(f"Per CONVENTIONS.md  {convention_name}: {action}")
   ```
   The lookup key `"Migration Patterns"` (without trailing spaces) does not match the
   stored key `"Migration Patterns  "` (with trailing spaces). The match fails silently
   -- no warning or error is raised.

**Reproduction outcome**: Confirmed via code-path tracing. The bug is deterministic:
any CONVENTIONS.md heading with trailing whitespace will be silently dropped from
convention conformance analysis.

## Step 3 -- Codebase Investigation

### Target repository

- **Repository**: acme-backend (from Component: sdlc-workflow)
- **Serena Instance**: serena_backend
- **Path**: /home/dev/repos/acme-backend
- **Code Intelligence**: No Serena MCP servers configured; using Read/Grep/Glob fallback

### Affected files and symbols

| File | Symbol/Location | Role |
|---|---|---|
| `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` | Convention heading extraction (`line[3:]`) | Extracts section names from CONVENTIONS.md headings without stripping whitespace |
| `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` | Convention-aware task enrichment (`convention_name in discovered_conventions`) | Performs exact-match lookup against extracted section names; fails when name has trailing whitespace |

### Code path analysis

**Buggy function -- heading extraction**:
- Location: `plugins/sdlc-workflow/skills/plan-feature/SKILL.md`, convention lookup section
- The expression `line[3:]` slices from character index 3 to end of line
- This correctly removes the `## ` prefix but does NOT strip trailing whitespace
- Fix: change `line[3:]` to `line[3:].strip()` to normalize the extracted heading name

**Downstream consumer -- task enrichment**:
- Location: `plugins/sdlc-workflow/skills/plan-feature/SKILL.md`, convention-aware task enrichment section
- Uses exact string match (`convention_name in discovered_conventions`)
- No defensive stripping on either side of the comparison
- The enrichment logic itself is correct; the defect is upstream in the extraction

### Existing test coverage

- **Existing eval fixture**: `evals/plan-feature/files/conventions-mock.md`
- **Coverage gap**: The existing fixture does NOT include trailing whitespace on headings,
  so this edge case is not covered by current evals
- **No reproducer test exists** for trailing whitespace in convention headings

### CONVENTIONS.md lookup

The repository does not have a `CONVENTIONS.md` file at its root. No repository-level
conventions apply to the fix task.

### Persistence-impact analysis

**Trace from buggy function output to persistence boundary**:

1. The heading extraction output (`conventions` dictionary) is used solely within the
   plan-feature skill's in-memory processing during task generation.
2. The convention references are written into the generated Jira task description via
   the `notes.append()` call.
3. The output flows to the Jira API (task creation) but is NOT persisted to a local
   database -- it is computed fresh each time `/plan-feature` runs.

**Conclusion**: No persistence boundary found. The buggy output is computed at
task-generation time and flows directly to Jira. No data migration is needed.
Previously generated tasks that were missing convention references cannot be
retroactively fixed via migration -- they would need to be regenerated.
