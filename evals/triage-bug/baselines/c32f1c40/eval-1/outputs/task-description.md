<!-- Jira API Metadata Block
jira.create_issue parameters:
  project_key: ACME
  issue_type: Task
  labels:
    - ai-generated-jira
  summary: "Fix convention heading extraction to strip trailing whitespace in plan-feature"
-->

## Repository
acme-backend

## Target Branch
main

## Description
Fix the plan-feature skill's convention conformance analysis to strip trailing whitespace
from CONVENTIONS.md heading lines during extraction. Currently, `line[3:]` preserves
trailing whitespace, causing exact-match convention lookups to silently fail when headings
have trailing spaces. This results in conventions being dropped from generated task
descriptions with no warning. Fixes ACME-500.

## Files to Modify
- `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` -- Fix heading extraction to strip trailing whitespace (`line[3:]` -> `line[3:].strip()`) in the convention conformance analysis logic

## Files to Create
- `evals/plan-feature/files/conventions-trailing-whitespace-mock.md` -- Test fixture with trailing whitespace on convention headings for the reproducer test

## Implementation Notes
The bug is in the convention conformance analysis section of
`plugins/sdlc-workflow/skills/plan-feature/SKILL.md`. The heading extraction logic
currently reads:

```python
for line in conventions_content.split('\n'):
    if line.startswith('## '):
        section_name = line[3:]  # BUG: does not strip trailing whitespace
        conventions[section_name] = current_section_content
```

**Fix**: Change `line[3:]` to `line[3:].strip()` to normalize the section name.

The convention-aware task enrichment step does an exact-match lookup:

```python
if convention_name in discovered_conventions:
    notes.append(f"Per CONVENTIONS.md  {convention_name}: {action}")
```

For defense in depth, consider also stripping the lookup key, but the primary fix
is at the extraction point.

**Reproducer test guidance**: Create a test fixture `CONVENTIONS.md` with trailing
whitespace on headings:

```
## Migration Patterns  
Add Index::create() for all FK columns.
```

(Note the two trailing spaces after `Migration Patterns`.)

The reproducer should:
1. Parse this fixture using the convention conformance analysis logic.
2. Assert that the section name `"Migration Patterns"` (without trailing spaces)
   is present as a key in the parsed conventions dictionary.
3. Assert that the generated task's Implementation Notes include the convention
   reference: `Per CONVENTIONS.md Migration Patterns: add Index::create() for all FK columns.`

**Existing test pattern**: The existing eval fixture at
`evals/plan-feature/files/conventions-mock.md` does NOT include trailing whitespace
on headings -- use it as a reference for the fixture format, then add trailing
whitespace to create the new fixture.

## Acceptance Criteria
- [ ] Reproducer test: a test with a CONVENTIONS.md fixture containing trailing whitespace on headings demonstrates the bug (fails before fix, passes after fix)
- [ ] Convention headings with trailing whitespace are correctly matched during plan-feature convention conformance analysis
- [ ] Conventions with trailing whitespace headings appear in generated task Implementation Notes
- [ ] No regression in existing plan-feature eval tests (conventions without trailing whitespace continue to work)

## Test Requirements
- [ ] Reproducer test: create a test using a CONVENTIONS.md fixture with trailing whitespace on section headings (e.g., `## Migration Patterns  ` with trailing spaces). Assert that the convention IS matched and included in the generated task output. Before the fix, this test must fail (convention silently dropped). After the fix, it must pass (convention included in Implementation Notes as `Per CONVENTIONS.md Migration Patterns: add Index::create() for all FK columns.`).
- [ ] Regression test: verify that existing conventions-mock.md fixture (without trailing whitespace) continues to produce correct convention matches after the fix.

## Verification Commands
- Run plan-feature evals to confirm no regression: `cd evals/plan-feature && ./run-eval.sh`

## Bug Context

- **Bug**: [ACME-500](https://mock-jira.example.com/browse/ACME-500)
- **Steps to Reproduce**: Create a CONVENTIONS.md with trailing whitespace on a heading (e.g., `## Migration Patterns  `), run `/plan-feature ACME-100` on a feature requiring that convention, inspect the generated task's Implementation Notes.
- **Expected Result**: The generated task's Implementation Notes should include: `Per CONVENTIONS.md Migration Patterns: add Index::create() for all FK columns.`
- **Actual Result**: The generated task's Implementation Notes do NOT reference the Migration Patterns convention. No warning or error is shown -- the convention is silently dropped.
- **Root Cause**: The heading extraction logic uses `line[3:]` without stripping trailing whitespace, causing exact-match convention lookups to fail silently when CONVENTIONS.md headings have trailing spaces.
