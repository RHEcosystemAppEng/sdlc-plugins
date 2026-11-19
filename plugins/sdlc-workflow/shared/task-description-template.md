# Task Description Template

All Jira tasks created by SDLC workflow skills must follow this template.
Skills that create tasks (plan-feature, verify-pr) produce this format;
skills that consume tasks (implement-task) parse it.

## Template

```
## Repository
<repository-name>

## Target Branch
<branch-name (e.g., main or TC-4418)>

## Description
<What this task achieves and why>

## Files to Modify
- `path/to/file.ext` — <brief reason>

## Files to Create
- `path/to/new_file.ext` — <purpose>

## API Changes
- `GET /v2/endpoint` — NEW: <description>
- `PUT /v2/endpoint/{id}` — MODIFY: <what changes in request/response>

## Implementation Notes
<Specific guidance: patterns to follow, existing code to reuse,
key functions/structs/components to interact with.
Reference actual file paths and symbol names found during repository analysis.>

## Reuse Candidates
- `path/to/file.ext::symbol_name` — <what it does and how it relates to this task>

## Acceptance Criteria
- [ ] Criterion 1
- [ ] Criterion 2

## Test Requirements
- [ ] Test description 1
- [ ] Test description 2

## Verification Commands
- `<command>` — <expected outcome>

## Documentation Updates
- `path/to/doc.md` — <what content to add or revise>

## Dependencies
- Depends on: Task N — <task title> (if any)
```

## Rules

- Omit sections that don't apply (e.g. no API Changes for a pure UI task, no Files
  to Create if only modifying, no Documentation Updates if no docs are impacted)
- Target Branch is always required — use `main` for standard direct-to-main workflow,
  or the feature issue ID for feature-branch workflow
- Repository must be a single repository per task
- When the root cause is owned by a different repository or the data layer, the
  task MUST include a **Root Cause Layer** section following the rule below
- File paths must be real paths discovered during repository or code analysis
- Implementation Notes must reference existing patterns, not abstract guidance —
  when reusable utilities, helpers, or shared modules exist, list them with file
  paths and symbol names so the implementer can reuse them instead of writing new code
- Reuse Candidates is optional — include it when existing code (domain logic,
  components, utilities, or patterns) overlaps with the planned changes, so the
  implementer has an explicit checklist of code to consider reusing
- Each task must be small enough for a single engineer to implement
- Verification Commands are optional — include them when acceptance criteria can be
  verified by running a command against the built or running service
- Documentation Updates is optional — include it when the task changes public APIs,
  configuration, setup steps, or architectural patterns, listing which docs need
  updating and what content to add or revise (not the actual doc content)

## Extension sections

Individual skills may add context-specific sections beyond the base template.
These extensions are documented in the skill that produces them:

- **Target PR** — used by verify-pr (Step 4e) for review feedback fixes, so
  implement-task adds commits to an existing PR branch
- **Review Context** — used by verify-pr (Step 4e) to capture the original review
  comment text and PR file/line reference
- **Bookend Type** — used by plan-feature for feature-branch bookend tasks,
  values: `create-branch` or `merge-branch`. implement-task uses this to skip
  normal implementation steps and handle branch/PR operations instead
- **Bug Context** — used by triage-bug to capture the originating Bug's key,
  Steps to Reproduce, Expected/Actual Result, and Root Cause summary.
  implement-task uses this to understand the bug being fixed and to write
  the reproducer test.
- **Root Cause Layer** — used by triage-bug, plan-feature, and verify-pr when the
  root cause is owned by a different repository or the data layer than the task's
  repository. implement-task uses it to recognize a deliberate symptom-level fix
  and to find the owning-repository Task or approved waiver.

## Root Cause Layer rule

When a task's fix location is the symptom layer, include the extension section:

```
## Root Cause Layer

- Root cause owned by: <repository> / <layer>
- Fix location: <root-cause | symptom>
- Deferred root-cause task: <owning-repository Task or Bug key>
```

A task whose `Fix location` is `symptom` MUST either name the owning-repository
Task (or Bug) that fixes the root cause in `Deferred root-cause task`, or record
an explicit user-approved waiver as `Deferred root-cause task: none — waiver
approved by <user>`. A symptom-level task MUST NOT be created while the root
cause is known to live in another repository or the data layer unless one of
these two conditions is met.

This rule routes work to the layer that owns the defect. It does not relax the
single-repository-per-task rule: each task, including the owning-repository task,
targets exactly one repository.
