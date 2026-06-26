# Jira API Metadata

Parameters for `jira.create_issue`:

- **Project key**: ACME
- **Issue type**: Task
- **Labels**: ai-generated-jira, bug-fix
- **additional_fields**: `{ "labels": ["ai-generated-jira", "bug-fix"] }`

---

## Repository
acme-backend

## Target Branch
main

## Description
Fix the convention heading extraction in the plan-feature skill to strip trailing whitespace from CONVENTIONS.md headings. Currently, `line[3:]` preserves trailing spaces, causing exact-match convention lookups to silently fail when headings have trailing whitespace. Fixes ACME-500.

## Files to Modify
- `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` -- fix heading extraction to strip trailing whitespace from `line[3:]`

## Implementation Notes
The bug is in the convention conformance analysis section of the plan-feature skill. The heading extraction code:

```python
for line in conventions_content.split('\n'):
    if line.startswith('## '):
        section_name = line[3:]  # BUG: does not strip trailing whitespace
        conventions[section_name] = current_section_content
```

Change `line[3:]` to `line[3:].strip()` to normalize the extracted heading text before using it as a dictionary key.

The downstream convention-aware task enrichment performs an exact match:

```python
if convention_name in discovered_conventions:
    notes.append(f"Per CONVENTIONS.md {convention_name}: {action}")
```

This match fails when the key has trailing whitespace but the lookup value does not. After applying `.strip()` at extraction time, the keys will be normalized and matches will succeed.

**Reproducer test guidance**: The Steps to Reproduce specify creating a CONVENTIONS.md with trailing whitespace on a heading (`## Migration Patterns  `) and running plan-feature. The reproducer test should:
- Provide a CONVENTIONS.md fixture containing `## Migration Patterns  \n` (with trailing spaces on the heading).
- Run the heading extraction logic against this fixture.
- Assert the extracted key is `"Migration Patterns"` (no trailing whitespace).
- Verify that the convention-aware task enrichment includes the convention in the output (i.e., the Implementation Notes contain `Per CONVENTIONS.md Migration Patterns: ...`).

The existing eval fixture at `evals/plan-feature/files/conventions-mock.md` does NOT include trailing whitespace on headings, so this edge case is currently untested.

Consider also adding a warning log when a convention heading is extracted but fails to match during enrichment, to prevent future silent failures.

Fixes [ACME-500](https://mock-jira.example.com/browse/ACME-500).

## Acceptance Criteria
- [ ] Reproducer test: a test with a CONVENTIONS.md fixture containing trailing whitespace on headings (e.g., `## Migration Patterns  `) demonstrates the bug fails before the fix and passes after the fix
- [ ] `line[3:]` is replaced with `line[3:].strip()` in the convention heading extraction logic so trailing whitespace is removed
- [ ] Conventions with trailing whitespace on headings are correctly matched and included in generated task Implementation Notes
- [ ] No regression in existing plan-feature tests and evals

## Test Requirements
- [ ] Reproducer test: create a CONVENTIONS.md fixture with trailing whitespace on at least one heading line (`## Migration Patterns  `), run convention extraction, and assert the heading is matched correctly (key is `"Migration Patterns"`, not `"Migration Patterns  "`)
- [ ] Test that convention-aware task enrichment includes the convention from the whitespace-containing heading in the generated output
- [ ] Verify existing eval fixtures (without trailing whitespace) continue to pass unchanged

## Verification Commands
- `pytest evals/plan-feature/ -v` -- all plan-feature evals should pass, including the new reproducer test

## Bug Context

- **Bug**: [ACME-500](https://mock-jira.example.com/browse/ACME-500)
- **Steps to Reproduce**: Create a CONVENTIONS.md with trailing whitespace on a heading (e.g., `## Migration Patterns  `), run `/plan-feature ACME-100` on a feature requiring a database migration with foreign keys, inspect the generated task's Implementation Notes.
- **Expected Result**: The generated task's Implementation Notes should include: "Per CONVENTIONS.md Migration Patterns: add `Index::create()` for all FK columns."
- **Actual Result**: The generated task's Implementation Notes do NOT reference the Migration Patterns convention. No warning or error is shown -- the convention is silently dropped.
- **Root Cause**: The heading extraction `line[3:]` does not strip trailing whitespace, causing exact-match convention lookups to fail silently when CONVENTIONS.md headings have trailing spaces.
