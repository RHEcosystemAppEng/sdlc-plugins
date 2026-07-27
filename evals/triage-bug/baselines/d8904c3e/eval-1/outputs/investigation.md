# Steps 2-3 -- Codebase Investigation: ACME-500

## Step 2 -- Reproduce/Trace

### Code-path tracing

This bug involves the plan-feature skill's convention conformance analysis, which is a skill-level behavior rather than a directly runnable command. Using code-path tracing instead of direct reproduction.

**Entry point**: `/plan-feature ACME-100` invocation triggers convention conformance analysis in the plan-feature skill.

**Trace path**:

1. The plan-feature skill reads `CONVENTIONS.md` and parses headings to build a conventions dictionary.
2. The heading extraction logic in `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` uses:
   ```python
   for line in conventions_content.split('\n'):
       if line.startswith('## '):
           section_name = line[3:]  # Extracts heading text after "## "
           conventions[section_name] = current_section_content
   ```
3. When the heading line is `## Migration Patterns  \n`, `line[3:]` produces `"Migration Patterns  "` (with trailing spaces).
4. The task enrichment step performs an exact-match lookup:
   ```python
   if convention_name in discovered_conventions:
       notes.append(f"Per CONVENTIONS.md ...{convention_name}: {action}")
   ```
5. The lookup for `"Migration Patterns"` fails because the dictionary key is `"Migration Patterns  "` (with trailing whitespace). The convention is silently skipped -- no warning or error is logged.

**Reproduction outcome**: Confirmed via code-path trace. The defect is deterministic: any trailing whitespace on a `## ` heading in `CONVENTIONS.md` will cause that convention to be silently dropped from the generated task description.

## Step 3 -- Codebase Investigation

### Target repository

- **Component**: sdlc-workflow
- **Repository**: acme-backend (from Repository Registry)
- **Path**: /home/dev/repos/acme-backend
- **Serena Instance**: serena_backend (however, Code Intelligence section notes no Serena servers are configured, so falling back to Read/Grep/Glob)

### Affected files and symbols

1. **`plugins/sdlc-workflow/skills/plan-feature/SKILL.md`** -- Convention conformance analysis section
   - **Defect location**: `line[3:]` heading extraction does not call `.strip()` on the extracted section name
   - **Impact**: All convention headings with trailing whitespace are silently dropped from the conventions dictionary

2. **`plugins/sdlc-workflow/skills/plan-feature/SKILL.md`** -- Convention-aware task enrichment section
   - **Match logic**: `if convention_name in discovered_conventions:` performs exact string match
   - **Impact**: Lookup fails when dictionary keys contain trailing whitespace that the lookup key does not have

### Existing test coverage

- **`evals/plan-feature/files/conventions-mock.md`** -- Existing eval fixture for plan-feature conventions does NOT include trailing whitespace on headings. This edge case is not covered by current evals.

### CONVENTIONS.md lookup

The repository does not have a `CONVENTIONS.md` at its root. No additional conventions to include in the task's Implementation Notes from the target repository itself.

### Persistence-impact analysis

The buggy function's output (the conventions dictionary) is used transiently during task generation -- it is consumed in-memory to produce the task description text, which is then submitted to Jira via API. The conventions dictionary itself is not persisted to a database. The incorrect output (missing convention reference in the task description) is persisted as part of the Jira task description, but this is a Jira content issue, not a database record requiring a data migration.

**No persistence boundary found.** The output is computed at task-generation time and the fix will correct all future task descriptions. No data migration is needed.

### Patterns for reproducer test

The reproducer test should:
- Create a `CONVENTIONS.md` fixture with trailing whitespace on a heading (e.g., `## Migration Patterns  `)
- Invoke the convention parsing logic
- Assert that the convention is correctly extracted despite trailing whitespace
- Verify the convention appears in the generated task's Implementation Notes

The existing eval fixture at `evals/plan-feature/files/conventions-mock.md` provides a pattern for how convention mock files are structured.

### Decomposition Guard (Step 6)

This bug has a **single root cause**: the `line[3:]` heading extraction does not strip trailing whitespace. The silent drop is a direct consequence of this same defect (exact match against an un-stripped key). A single Task is appropriate -- no decomposition needed.
