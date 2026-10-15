<!-- Jira API Metadata -->
<!-- jira.create_issue parameters: -->
<!-- project: ACME -->
<!-- issuetype: Task -->
<!-- labels: ["ai-generated-jira"] -->
<!-- summary: Fix plan-feature convention heading extraction to strip trailing whitespace -->

## Repository
acme-backend

## Target Branch
main

## Description
Fix the plan-feature skill's convention conformance analysis to strip trailing whitespace from `CONVENTIONS.md` headings during extraction. Currently, `line[3:]` captures trailing spaces, causing exact-match lookups to fail silently when headings have trailing whitespace. This results in conventions being silently omitted from generated task descriptions. Fixes ACME-500.

## Files to Modify
- `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` -- Add `.strip()` to the heading extraction logic (`section_name = line[3:]` becomes `section_name = line[3:].strip()`)

## Implementation Notes
The defect is in the convention conformance analysis section of `plugins/sdlc-workflow/skills/plan-feature/SKILL.md`. The heading extraction loop splits `CONVENTIONS.md` content by newline and checks for lines starting with `## `. The extracted section name uses `line[3:]` which does not strip trailing whitespace.

**Current code path:**
```python
for line in conventions_content.split('\n'):
    if line.startswith('## '):
        section_name = line[3:]  # BUG: trailing whitespace preserved
        conventions[section_name] = current_section_content
```

**Fix:**
```python
section_name = line[3:].strip()
```

The downstream match in the convention-aware task enrichment step uses exact string comparison:
```python
if convention_name in discovered_conventions:
    notes.append(f"Per CONVENTIONS.md {convention_name}: {action}")
```

This match will succeed once the extraction step produces clean keys.

**Reproducer test guidance:**
- Create a test fixture `CONVENTIONS.md` with trailing whitespace on a heading line: `## Migration Patterns  ` (two trailing spaces after "Patterns")
- Include a convention body: `Add Index::create() for all FK columns.`
- Run the convention extraction logic against this fixture
- Assert that the extracted section name equals `"Migration Patterns"` (without trailing whitespace)
- Assert that the convention is matched and appears in the generated task's Implementation Notes as `Per CONVENTIONS.md Migration Patterns: add Index::create() for all FK columns.`

**Existing test reference:** `evals/plan-feature/files/conventions-mock.md` -- the existing eval fixture does not include trailing whitespace on headings, so a new fixture or modification is needed for the reproducer.

## Acceptance Criteria
- [ ] A reproducer test exists that creates a `CONVENTIONS.md` with trailing whitespace on a heading, runs the convention extraction, and asserts the convention is correctly matched and included in the output. The test fails before the fix and passes after.
- [ ] The heading extraction in plan-feature's convention conformance analysis strips trailing whitespace from section names (e.g., `line[3:].strip()`)
- [ ] Conventions with trailing whitespace on headings in `CONVENTIONS.md` are correctly matched and included in generated task descriptions
- [ ] No regression in existing plan-feature eval tests

## Test Requirements
- [ ] Reproducer test: create a `CONVENTIONS.md` fixture with trailing whitespace on a `## ` heading (e.g., `## Migration Patterns  `), run the convention extraction and matching logic, and assert that (a) the section name is extracted without trailing whitespace, (b) the convention appears in the generated Implementation Notes. This test must fail before the fix and pass after.
- [ ] Verify that headings WITHOUT trailing whitespace continue to work correctly (no regression)
- [ ] Verify that headings with mixed whitespace (tabs, multiple spaces) are also handled by the `.strip()` fix

## Verification Commands
- Run plan-feature evals to confirm no regression: `claude /eval plan-feature`

## Bug Context

- **Bug**: [ACME-500](https://mock-jira.example.com/browse/ACME-500)
- **Steps to Reproduce**: Create a `CONVENTIONS.md` with trailing whitespace on a heading (e.g., `## Migration Patterns  `), run `/plan-feature` on a feature requiring that convention, and inspect the generated task's Implementation Notes.
- **Expected Result**: The generated task's Implementation Notes should include: `Per CONVENTIONS.md Migration Patterns: add Index::create() for all FK columns.`
- **Actual Result**: The generated task's Implementation Notes do NOT reference the Migration Patterns convention. No warning or error is shown -- the convention is silently dropped.
- **Root Cause**: The heading extraction uses `line[3:]` without `.strip()`, preserving trailing whitespace in the dictionary key. The downstream exact-match lookup then fails because the lookup key has no trailing whitespace, causing the convention to be silently omitted.
