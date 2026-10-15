# Steps 2-3 -- Codebase Investigation: ACME-500

## Step 2 -- Reproduce/Trace

### Reproduction approach: Code-path tracing

This bug cannot be directly reproduced via runnable commands because it involves the plan-feature skill's internal convention parsing logic. Code-path tracing is the appropriate method.

### Entry point

The entry point is the `/plan-feature` skill invocation (Step 2 of the reproduction steps). The skill reads `CONVENTIONS.md` and extracts headings to match conventions against task requirements.

### Trace findings

**Trace path**: `CONVENTIONS.md` file read --> heading extraction loop --> convention dictionary keying --> convention-aware task enrichment match

1. **Heading extraction** (`plugins/sdlc-workflow/skills/plan-feature/SKILL.md`, convention conformance analysis):
   ```python
   for line in conventions_content.split('\n'):
       if line.startswith('## '):
           section_name = line[3:]  # Extracts heading text after "## "
           conventions[section_name] = current_section_content
   ```
   When the input line is `## Migration Patterns  \n`, `line[3:]` produces `"Migration Patterns  "` (with two trailing spaces). The `split('\n')` strips the newline, but trailing spaces remain.

2. **Convention matching** (`plugins/sdlc-workflow/skills/plan-feature/SKILL.md`, convention-aware task enrichment):
   ```python
   if convention_name in discovered_conventions:
       notes.append(f"Per CONVENTIONS.md {convention_name}: {action}")
   ```
   The lookup key `convention_name` is `"Migration Patterns"` (without trailing whitespace), but the dictionary key stored in step 1 is `"Migration Patterns  "` (with trailing whitespace). The `in` check fails, and the convention is silently skipped.

3. **No warning/error path**: There is no fallback or logging when a convention is not found in the dictionary. The `if` block simply does not execute, resulting in silent omission.

### Divergence point

The actual behavior diverges from expected behavior at the heading extraction step. The extracted section name includes trailing whitespace from the source file, causing all downstream exact-match lookups to fail silently.

## Step 3 -- Codebase Investigation

### Target repository

- **Repository**: acme-backend (based on Component: sdlc-workflow and the code paths referenced)
- **Serena Instance**: serena_backend (from Repository Registry)
- **Path**: /home/dev/repos/acme-backend

Note: Code Intelligence section states "No Serena MCP servers are configured." Read/Grep/Glob fallback is used.

### Affected files and symbols

| File | Symbol/Section | Role |
|------|----------------|------|
| `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` | Convention conformance analysis (heading extraction loop) | **Defect location** -- `line[3:]` does not strip trailing whitespace |
| `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` | Convention-aware task enrichment (match block) | **Impact location** -- exact-match lookup fails due to whitespace mismatch |

### Existing test coverage

- **File**: `evals/plan-feature/files/conventions-mock.md`
- **Status**: The existing eval fixture does NOT include trailing whitespace on headings. This edge case is not covered by current evals.

### CONVENTIONS.md lookup

The repository does not have a `CONVENTIONS.md` at its root. No project-specific conventions apply to the fix task.

### Persistence-impact analysis

**No persistence boundary found.** The convention conformance analysis is computed at query time during each `/plan-feature` invocation. Convention section names are extracted from `CONVENTIONS.md`, held in an in-memory dictionary, and used to generate task description text. No values are written to a database, ORM model, or persistent store.

- The output of the heading extraction is a transient Python dictionary (`conventions[section_name]`)
- The downstream consumer writes to a Jira task description via the Jira API, but the section name itself is not persisted as structured data -- it is embedded in generated text
- No data migration is needed -- fixing the extraction logic will correct all future invocations
