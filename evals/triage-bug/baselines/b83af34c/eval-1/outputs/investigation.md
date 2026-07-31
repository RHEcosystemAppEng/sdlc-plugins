# Step 2 -- Reproduce/Trace

## Code-path tracing

This bug involves the plan-feature skill's convention parsing logic, which is a
skill/documentation bug that cannot be directly reproduced via CLI commands in the
current environment. Code-path tracing was used instead.

### Entry point

The entry point is the `/plan-feature ACME-100` skill invocation. When plan-feature
runs, it reads CONVENTIONS.md from the target repository and performs convention
conformance analysis to enrich generated task descriptions with relevant convention
references.

### Trace through affected code paths

1. **Convention file reading**: The plan-feature skill reads the CONVENTIONS.md file
   and splits its content by newlines.

2. **Heading extraction** (the defect site): For each line, the code checks if it
   starts with `## ` and extracts the heading text using `line[3:]`. This slice
   operation captures everything after the `## ` prefix, including any trailing
   whitespace characters.

   ```python
   for line in conventions_content.split('\n'):
       if line.startswith('## '):
           section_name = line[3:]  # Does NOT strip trailing whitespace
           conventions[section_name] = current_section_content
   ```

   When the heading line is `## Migration Patterns  \n`, the extracted section name
   becomes `"Migration Patterns  "` (with two trailing spaces).

3. **Convention matching** (where behavior diverges): The task enrichment step
   performs an exact string match to find the convention:

   ```python
   if convention_name in discovered_conventions:
       notes.append(f"Per CONVENTIONS.md section {convention_name}: {action}")
   ```

   The lookup key `"Migration Patterns"` (clean) does not match the stored key
   `"Migration Patterns  "` (with trailing spaces), so the convention is silently
   skipped. No warning or error is emitted.

### Divergence from expected behavior

The divergence occurs between steps 2 and 3: the heading extraction preserves
trailing whitespace, but the convention matching expects clean heading names.
The result is a silent failure -- the convention exists in the dictionary but
under a whitespace-padded key that never matches.

# Step 3 -- Codebase Investigation

## Target repository

Based on the Component field (sdlc-workflow) and the code paths referenced in the
bug description, the target repository is **acme-backend** (from the Repository
Registry in CLAUDE.md).

- Serena Instance: serena_backend
- Path: /home/dev/repos/acme-backend

## Affected files and symbols

### Primary defect location

- **File**: `plugins/sdlc-workflow/skills/plan-feature/SKILL.md`
- **Symbol/section**: Convention conformance analysis -- heading extraction logic
- **Defect**: `line[3:]` does not call `.strip()` on the extracted heading text,
  leaving trailing whitespace in the dictionary key

### Secondary affected location

- **File**: `plugins/sdlc-workflow/skills/plan-feature/SKILL.md`
- **Symbol/section**: Convention-aware task enrichment -- convention name matching
- **Impact**: Exact-match lookup against convention names fails when keys have
  trailing whitespace

## Existing test coverage

- **File**: `evals/plan-feature/files/conventions-mock.md`
- **Status**: The existing eval fixture does NOT include trailing whitespace on
  headings, so this edge case is not covered by current evals.

## CONVENTIONS.md lookup

The repository does not have a CONVENTIONS.md at its root. No additional conventions
apply to the fix task.

## Persistence-impact analysis

The buggy function's output (the convention dictionary) is used to enrich task
descriptions that are posted to Jira via the API. The convention text is included
in the generated task's Implementation Notes field.

**Persistence boundary**: The generated task description is persisted to Jira
(external system) when `jira.create_issue` is called. However, this is not a
database persistence concern in the traditional sense -- each task is generated
fresh from source data (CONVENTIONS.md) at plan-feature invocation time. Previously
generated tasks with missing conventions are already persisted in Jira but represent
completed work artifacts, not ongoing data that can be retroactively corrected via
migration.

**Conclusion**: No data migration is needed. The fix corrects future behavior.
Previously generated tasks that silently omitted conventions are historical artifacts.

## Summary of findings

| Aspect | Finding |
|--------|---------|
| Root cause location | `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` -- heading extraction |
| Defect type | Missing string normalization (trailing whitespace not stripped) |
| Silent failure | No warning logged when convention match fails |
| Test gap | `evals/plan-feature/files/conventions-mock.md` lacks trailing-whitespace case |
| Persistence impact | None -- output is per-invocation, not persisted to local database |
| CONVENTIONS.md | Not present in repository root |
