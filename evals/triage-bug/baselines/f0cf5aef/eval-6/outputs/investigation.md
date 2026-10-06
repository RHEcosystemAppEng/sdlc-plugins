# Steps 2-3 -- Codebase Investigation: ACME-500

## Target Repository

- **Repository**: acme-backend
- **Role**: Rust backend service
- **Serena Instance**: serena_backend
- **Path**: /home/dev/repos/acme-backend

Identified from: Component field ("sdlc-workflow") and Repository Registry in CLAUDE.md.

## Step 2 -- Reproduce/Trace

### Reproduction approach

The Steps to Reproduce describe creating a `CONVENTIONS.md` file with trailing whitespace on a heading and running `/plan-feature ACME-100`. This is a skill invocation, not a directly runnable command, so code-path tracing is the appropriate approach.

### Code-path tracing

**Entry point**: The `/plan-feature` skill's convention conformance analysis, which reads `CONVENTIONS.md` and matches section headings to convention names.

**Trace findings**:

1. The plan-feature skill reads `CONVENTIONS.md` and parses it line by line to extract convention sections.

2. The heading extraction logic (from `plugins/sdlc-workflow/skills/plan-feature/SKILL.md`):
   ```python
   for line in conventions_content.split('\n'):
       if line.startswith('## '):
           section_name = line[3:]  # Extracts heading text after "## "
           conventions[section_name] = current_section_content
   ```
   The key defect is at `line[3:]` -- this extracts everything after `## ` but does **not** call `.strip()` on the result. If the heading line has trailing whitespace (e.g., `## Migration Patterns  \n`), the extracted section name becomes `"Migration Patterns  "` (with trailing spaces).

3. The convention-aware task enrichment step performs an exact-match lookup:
   ```python
   if convention_name in discovered_conventions:
       notes.append(f"Per CONVENTIONS.md §{convention_name}: {action}")
   ```
   This lookup uses the canonical name `"Migration Patterns"` (without trailing whitespace) as the key. Since the dictionary was populated with `"Migration Patterns  "` (with trailing spaces), the exact-match comparison fails silently.

4. No warning or error is emitted when a convention name does not match -- the convention is simply skipped, and the generated task omits it entirely.

**Divergence point**: The heading extraction at `line[3:]` does not strip trailing whitespace, causing exact-match lookups to fail when `CONVENTIONS.md` headings contain trailing spaces.

## Step 3 -- Codebase Investigation

### Code Intelligence

Per CLAUDE.md Code Intelligence section: "No Serena MCP servers are configured. Code intelligence is not available."

Fallback: Using Read, Grep, and Glob tools for investigation.

### Investigation findings

**Affected files and symbols** (from repo-context-mock.md):

1. **Convention heading extraction** (`plugins/sdlc-workflow/skills/plan-feature/SKILL.md`):
   - The `line[3:]` expression extracts the heading text without stripping trailing whitespace.
   - This populates the `conventions` dictionary with keys that may contain trailing spaces.

2. **Convention-aware task enrichment** (`plugins/sdlc-workflow/skills/plan-feature/SKILL.md`):
   - The `if convention_name in discovered_conventions` lookup performs an exact string match.
   - When the key has trailing whitespace, the match fails silently.

3. **Eval fixture** (`evals/plan-feature/files/conventions-mock.md`):
   - The existing eval fixture for plan-feature conventions does NOT include trailing whitespace on headings.
   - This edge case is not covered by current evals.

### CONVENTIONS.md lookup

Checked for `CONVENTIONS.md` at the repository root (`/home/dev/repos/acme-backend/CONVENTIONS.md`). The repository does not have a CONVENTIONS.md file at its root.

### Persistence-impact analysis

**Trace output to persistence boundary**: The bug affects the plan-feature skill's output -- specifically, the generated task description's Implementation Notes content. Task descriptions are created in Jira via `jira.create_issue`, which persists the description to Jira's database.

However, this is not a data-at-rest corruption issue in the traditional sense. The stale data is a missing convention reference in a Jira task description. Each invocation of `/plan-feature` produces a new task -- existing tasks with missing conventions are not automatically correctable via migration, but they are also not reused as source-of-truth data.

**Conclusion**: No data migration is needed. Fixing the heading extraction logic will ensure future invocations of `/plan-feature` correctly include conventions from headings with trailing whitespace. Previously generated tasks with missing conventions are historical artifacts, not actively incorrect persisted data.

### Existing test patterns

Relevant test patterns found:

- `evals/plan-feature/files/conventions-mock.md` -- existing eval fixture for convention parsing, but does NOT cover trailing whitespace edge case.
- Plan-feature evals test convention conformance analysis but only with clean headings (no trailing whitespace).
- No existing test specifically asserts behavior when `CONVENTIONS.md` headings contain trailing whitespace.

The reproducer test should add a conventions mock file with trailing whitespace on headings and verify that the convention is still correctly matched and included in the generated task.
