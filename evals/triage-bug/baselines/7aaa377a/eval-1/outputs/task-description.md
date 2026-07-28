# Step 5 – Generated Task Description for ACME-500

## Jira API Metadata

The following parameters would be passed to `jira.create_issue`:

```
project key:  ACME
issue type:   Task
summary:      Fix plan-feature convention heading extraction to strip trailing whitespace
labels:       ["ai-generated-jira", "reported-by-user"]
```

(Labels include `ai-generated-jira` as required, plus `reported-by-user` propagated from
the originating Bug ACME-500.)

After creation, the Task would be linked to ACME-500 using:
```
jira.create_issue_link(
  link_type="Blocks",
  inward_issue_key=<created-task-key>,
  outward_issue_key="ACME-500"
)
```

---

## Task Description

## Repository
acme-backend

## Target Branch
main

## Description

The `plan-feature` skill silently drops convention references from generated task
Implementation Notes when `CONVENTIONS.md` has trailing whitespace on heading lines.
This causes engineers to miss required conventions (e.g., "add `Index::create()` for all
FK columns") with no warning that anything was omitted.

The root cause is a one-character fix: the heading extraction `line[3:]` does not strip
trailing whitespace, so the stored section key never matches the expected lookup key in
the convention-aware task enrichment step.

This task fixes the extraction logic in `plugins/sdlc-workflow/skills/plan-feature/SKILL.md`
and adds eval coverage for the trailing-whitespace edge case.

Fixes ACME-500.

## Files to Modify
- `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` — Update the convention heading extraction instruction to strip trailing whitespace from the section name after removing the `## ` prefix
- `evals/plan-feature/files/conventions-mock.md` — Augment the existing fixture to include at least one heading with trailing whitespace, or create a separate fixture file

## Implementation Notes

The defect lives entirely within `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` in
two adjacent sections:

**Convention lookup section** — the heading extraction step:

```python
# Current (buggy):
section_name = line[3:]

# Fixed:
section_name = line[3:].strip()
```

This ensures a heading `## Migration Patterns  \n` produces the canonical key
`"Migration Patterns"` rather than `"Migration Patterns  "`.

**Convention-aware task enrichment section** — the downstream match:

```python
if convention_name in discovered_conventions:
    notes.append(f"Per CONVENTIONS.md §{convention_name}: {action}")
```

No change needed here — once the extraction is fixed, the exact-match lookup will
succeed for trimmed keys.

**Eval coverage** — the existing fixture `evals/plan-feature/files/conventions-mock.md`
does not include any trailing-whitespace headings. Add a heading of the form
`## <SectionName>  ` (with two trailing spaces) to the fixture and add an eval case
that asserts the generated task includes the corresponding `Per CONVENTIONS.md §...`
reference. This is the reproducer test.

No CONVENTIONS.md exists at the repository root, so no conventions apply to this fix
task itself.

Reference: Fixes ACME-500 (https://mock-jira.example.com/browse/ACME-500).

## Acceptance Criteria
- [ ] **Reproducer test**: a plan-feature eval using a `CONVENTIONS.md` fixture with trailing-whitespace headings fails before the fix and passes after (confirms the bug is fixed and cannot regress)
- [ ] When `CONVENTIONS.md` contains `## Migration Patterns  ` (with trailing spaces), running `/plan-feature` on a matching feature produces a task whose Implementation Notes include `Per CONVENTIONS.md §Migration Patterns: add Index::create() for all FK columns.`
- [ ] Convention references are never silently dropped due to trailing whitespace on any heading line — the fix is general, not scoped to a single section name
- [ ] All existing plan-feature evals continue to pass (no regression)

## Test Requirements
- [ ] **Reproducer test** (first): add a trailing-whitespace fixture to `evals/plan-feature/files/conventions-mock.md` (or a new file `evals/plan-feature/files/conventions-trailing-ws-mock.md`) containing `## Migration Patterns  ` with two trailing spaces followed by `Add Index::create() for all FK columns.`; assert that the generated task description contains the exact string `Per CONVENTIONS.md §Migration Patterns: add \`Index::create()\` for all FK columns.` — this test must fail against the pre-fix code and pass after the fix
- [ ] Add an eval case in the plan-feature eval suite that exercises the trailing-whitespace fixture end-to-end through the convention-aware task enrichment path
- [ ] Verify that convention sections whose headings have NO trailing whitespace continue to be picked up correctly (regression guard for the existing behavior)

## Bug Context

- **Bug**: [ACME-500](https://mock-jira.example.com/browse/ACME-500)
- **Steps to Reproduce**: (1) Create `CONVENTIONS.md` with `## Migration Patterns  ` (trailing spaces) containing `Add Index::create() for all FK columns.`; (2) run `/plan-feature ACME-100` on a feature requiring a DB migration with FKs; (3) inspect the generated task's Implementation Notes.
- **Expected Result**: Generated task's Implementation Notes include `Per CONVENTIONS.md §Migration Patterns: add Index::create() for all FK columns.`
- **Actual Result**: Implementation Notes do NOT reference the Migration Patterns convention; no warning is shown.
- **Root Cause**: The convention heading extraction `line[3:]` does not strip trailing whitespace, producing a key `"Migration Patterns  "` that never matches the exact-match lookup `convention_name in discovered_conventions` → convention is silently dropped.
