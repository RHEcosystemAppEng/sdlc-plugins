# Jira API Metadata

The following parameters would be passed to `jira.create_issue`:

- **Project key**: ACME
- **Issue type**: Task
- **Labels**: ai-generated-jira
- **additional_fields**: `{ "labels": ["ai-generated-jira"] }`

After creation, a link would be created via `jira.create_issue_link`:
- **link_type**: Blocks
- **inward_issue_key**: <created-task-key> (the Task)
- **outward_issue_key**: ACME-500 (the Bug)

---

**Summary**: Strip trailing whitespace from CONVENTIONS.md heading extraction in plan-feature skill

## Repository
acme-backend

## Target Branch
main

## Description
The plan-feature skill's convention heading extraction uses `line[3:]` to parse
`## ` headings from `CONVENTIONS.md` files, but does not strip trailing whitespace.
When a heading line contains trailing spaces (e.g., `## Migration Patterns  `), the
extracted section name retains those spaces, causing exact-match lookups to fail
silently. The convention is dropped from the generated task with no warning.

This task fixes the heading extraction to strip trailing whitespace and adds a
reproducer test to prevent regression. Fixes ACME-500.

## Files to Modify
- `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` -- add `.strip()` to the heading extraction line (`section_name = line[3:]`) so trailing whitespace is normalized

## Files to Create
- `evals/plan-feature/files/conventions-trailing-whitespace-mock.md` -- conventions fixture with trailing whitespace on heading lines for the reproducer test

## Implementation Notes
The defect is in the convention heading extraction loop in
`plugins/sdlc-workflow/skills/plan-feature/SKILL.md`. The current code:

```python
section_name = line[3:]  # Extracts heading text after "## "
```

should be changed to:

```python
section_name = line[3:].strip()  # Normalize trailing whitespace
```

This ensures that `## Migration Patterns  ` extracts as `"Migration Patterns"`
rather than `"Migration Patterns  "`, allowing the downstream exact-match lookup
(`convention_name in discovered_conventions`) to succeed.

The convention-aware task enrichment at the match site does not need modification --
the fix at the extraction point is sufficient since the lookup key will now be
normalized.

**Reproducer test guidance:**
- Use the existing eval pattern in `evals/plan-feature/` as a reference.
- The existing fixture at `evals/plan-feature/files/conventions-mock.md` does NOT
  include trailing whitespace -- create a new fixture file that duplicates it with
  trailing spaces on heading lines.
- The reproducer should confirm that conventions with trailing whitespace on headings
  are matched and included in the generated task's Implementation Notes.

**Warning logging (optional improvement):**
Consider adding a warning log when a convention heading contains leading or trailing
whitespace after stripping, to help users identify formatting issues in their
`CONVENTIONS.md` files.

## Reuse Candidates
- `evals/plan-feature/files/conventions-mock.md` -- existing conventions fixture; duplicate and extend with trailing whitespace for the reproducer test

## Acceptance Criteria
- [ ] A reproducer test demonstrates the bug: a CONVENTIONS.md fixture with trailing whitespace on a heading line causes the convention to be silently dropped (fails before fix, passes after fix)
- [ ] The heading extraction in plan-feature strips trailing whitespace from `## ` headings so that conventions are matched regardless of trailing spaces
- [ ] No regression in existing plan-feature evals and tests

## Test Requirements
- [ ] Reproducer test: create a CONVENTIONS.md fixture with `## Migration Patterns  ` (trailing spaces) and verify that plan-feature includes the convention reference `Per CONVENTIONS.md Migration Patterns: ...` in the generated task's Implementation Notes. Before the fix, this test should fail (convention missing). After the fix, it should pass.
- [ ] Verify that the existing conventions-mock.md (without trailing whitespace) continues to work correctly -- no regression in the standard case
- [ ] Edge case: heading with only whitespace after `## ` (e.g., `##    `) should be handled gracefully (either skipped or treated as empty)

## Bug Context

- **Bug**: [ACME-500](https://mock-jira.example.com/browse/ACME-500)
- **Steps to Reproduce**: Create a `CONVENTIONS.md` with trailing whitespace on a heading line (e.g., `## Migration Patterns  `), run `/plan-feature ACME-100` on a feature requiring that convention, and inspect the generated task's Implementation Notes.
- **Expected Result**: The generated task's Implementation Notes should include: `Per CONVENTIONS.md Migration Patterns: add Index::create() for all FK columns.`
- **Actual Result**: The generated task's Implementation Notes do NOT reference the Migration Patterns convention. No warning or error is shown -- the convention is silently dropped.
- **Root Cause**: The heading extraction `line[3:]` does not strip trailing whitespace, producing a key like `"Migration Patterns  "` that fails exact-match lookup against `"Migration Patterns"`.
