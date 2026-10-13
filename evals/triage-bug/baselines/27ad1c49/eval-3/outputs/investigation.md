# Investigation: ACME-502

## Bug Summary

**Key**: ACME-502
**Summary**: Skill output is malformed and task creation uses wrong issue type
**Component**: sdlc-workflow

Two distinct problems occur when running `/plan-feature`:
1. Generated task descriptions have malformed convention references in Implementation Notes (kebab-case instead of title case).
2. Tasks are created with issue type "Feature" (ID 10142) instead of "Task" (ID 10050).

## Investigation Findings

### Root Cause 1: Convention reference formatter uses wrong case transform

**What is broken**: When `/plan-feature` generates Implementation Notes that reference sections from a project's `CONVENTIONS.md`, the convention reference formatter produces kebab-case slugs (e.g., `migration-patterns`) instead of preserving the original heading text in title case (e.g., `Migration Patterns`).

**Why it is broken**: The convention reference formatter in `shared/convention-utils.md` applies a slug/kebab-case transformation to CONVENTIONS.md section headings when building `section-ref` references. It lowercases the heading text and replaces spaces with hyphens, producing references like `migration-patterns`. The correct behavior is to preserve the original heading text as-is, producing references like `Migration Patterns` prefixed with the `section` marker.

**Where it is broken**: `shared/convention-utils.md` -- the utility module responsible for parsing CONVENTIONS.md headings and formatting section references for inclusion in generated task descriptions.

**How to verify the fix**: A reproducer test should:
1. Provide a CONVENTIONS.md with a heading `## Migration Patterns`.
2. Invoke the convention reference formatter on that heading.
3. Assert the output is `Migration Patterns` (title case, matching the original heading), not `migration-patterns` (kebab-case slug).

### Root Cause 2: Task creation uses Feature issue type ID instead of Task

**What is broken**: When `/plan-feature` creates a Jira issue for the generated task, it uses the Feature issue type ID (10142) from Jira Configuration instead of the Task issue type ID. This causes the created issue to be typed as "Feature" rather than "Task".

**Why it is broken**: The task creation logic in `plan-feature/SKILL.md` Step 6a reads the `Feature issue type ID` field from the project's Jira Configuration section. This is the correct field for creating Feature issues, but when the step creates a *Task* (a sub-work-item of a feature), it should instead use the Task issue type ID. The code path does not distinguish between creating a Feature and creating a Task -- it unconditionally uses the Feature issue type ID for all issue creation.

**Where it is broken**: `plan-feature/SKILL.md` Step 6a -- the task creation step that calls `jira.create_issue` with the issue type parameter sourced from the wrong configuration field.

**How to verify the fix**: A reproducer test should:
1. Configure a project with a custom issue type scheme where Task has ID 10050 and Feature has ID 10142.
2. Run `/plan-feature` to generate and create a task.
3. Assert the created issue's `issuetype.id` is `10050` (Task), not `10142` (Feature).

## Independence Assessment

These two root causes are **independent**:

- **Different modules**: Root cause 1 is in `shared/convention-utils.md` (a shared utility), while root cause 2 is in `plan-feature/SKILL.md` Step 6a (skill-specific task creation logic).
- **Different code paths**: Root cause 1 affects the content generation pipeline (formatting convention references for description text), while root cause 2 affects the Jira API call (selecting the issue type ID parameter).
- **Different failure modes**: Root cause 1 produces cosmetically incorrect description content; root cause 2 creates the wrong type of Jira issue entirely.
- **Independently fixable**: Fixing the convention formatter does not affect issue type selection, and vice versa. Each fix can be developed, tested, and deployed independently.

This independence triggers the Decomposition Guard (Step 6).
