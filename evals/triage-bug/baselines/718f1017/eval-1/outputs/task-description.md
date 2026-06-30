<!-- Jira API metadata — parameters for jira.create_issue -->
```
Project Key: ACME
Issue Type: Task
Labels: ["ai-generated-jira"]
```

## Repository
acme-backend

## Target Branch
main

## Description
Fix ACME-500: plan-feature silently drops conventions when `CONVENTIONS.md` has trailing whitespace on heading lines. The heading extraction logic uses `line[3:]` which preserves trailing whitespace, causing exact-match convention lookups to fail silently. Apply `.strip()` to normalize heading keys.

## Files to Modify
- `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` — fix heading extraction to strip trailing whitespace from `line[3:]`

## Implementation Notes
The convention lookup in `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` extracts heading names with:

```python
section_name = line[3:]
```

When a `CONVENTIONS.md` heading line has trailing whitespace (e.g., `## Migration Patterns  `), `line[3:]` produces `"Migration Patterns  "` (with trailing spaces). The downstream match:

```python
if convention_name in discovered_conventions:
```

fails silently because the key includes trailing whitespace that the lookup value does not.

**Fix**: Change `line[3:]` to `line[3:].strip()` so trailing whitespace is removed before storing the section name in the conventions dictionary.

**Reproducer test**: Create a `CONVENTIONS.md` fixture with trailing whitespace on a heading line (e.g., `## Migration Patterns  ` with two trailing spaces after "Patterns"). Run the convention lookup against this fixture and assert that the convention reference string `Per CONVENTIONS.md §Migration Patterns:` appears in the generated task's Implementation Notes.

## Acceptance Criteria
- [ ] Reproducer test: a test using a `CONVENTIONS.md` fixture with trailing whitespace on headings confirms the convention is matched and included in the output (this test should fail before the fix and pass after)
- [ ] `line[3:]` is replaced with `line[3:].strip()` in the convention heading extraction logic
- [ ] Conventions with trailing whitespace on headings are correctly discovered and referenced in generated task descriptions
- [ ] Existing conventions without trailing whitespace continue to work as before (no regression)

## Test Requirements
- [ ] Reproducer test: create a `CONVENTIONS.md` fixture with trailing whitespace on a heading (e.g., `## Migration Patterns  ` with trailing spaces), run convention lookup, and assert that `"Migration Patterns"` is a key in the discovered conventions dictionary and that the generated Implementation Notes include `Per CONVENTIONS.md §Migration Patterns:`
- [ ] Regression test: verify that headings without trailing whitespace still match correctly
- [ ] Edge case test: verify headings with mixed whitespace (tabs, multiple spaces) are handled

## Verification Commands
- `grep -n 'line\[3:\]' plugins/sdlc-workflow/skills/plan-feature/SKILL.md` — should show `.strip()` applied to the extraction

## Bug Context
- **Bug**: [ACME-500](https://mock-jira.example.com/browse/ACME-500)
- **Steps to Reproduce**:
  1. Create a `CONVENTIONS.md` file with a convention section that has trailing whitespace on the heading (e.g., `## Migration Patterns  `)
  2. Run `/plan-feature ACME-100` on a feature that requires a database migration with foreign keys
  3. Inspect the generated task's Implementation Notes
- **Expected Result**: The generated task's Implementation Notes should include: `Per CONVENTIONS.md §Migration Patterns: add Index::create() for all FK columns.`
- **Actual Result**: The generated task's Implementation Notes do NOT reference the Migration Patterns convention. No warning or error is shown — the convention is silently dropped.
- **Root Cause**: Heading extraction uses `line[3:]` which preserves trailing whitespace, causing exact-match convention lookups to fail silently.
