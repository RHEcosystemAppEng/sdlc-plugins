## Repository
sdlc-plugins

## Target Branch
main

## Description
Improve the plan-feature skill to specify index requirements when planning tasks that add new columns used in query filters. The verification of TC-9103 revealed that the task's migration specification added a `deleted_at` column to the `sbom` table but did not include creating an index, despite the list endpoint filtering by `deleted_at IS NULL` on every default query. A reviewer flagged this as a performance gap.

The plan-feature skill should include a check: when generating migration specifications that add columns which will be used in WHERE clauses (especially columns referenced in the endpoint filter logic described in the same task), add explicit guidance to create an appropriate index.

## Files to Modify
- `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` -- add guidance in the task generation section to specify index creation when new columns are used in query filters

## Implementation Notes
- Add a check in the migration specification logic: when a new column is added and the same task's endpoint/service changes include filtering by that column, include index creation in the migration specification
- This is a method-level improvement (language-agnostic: "add indexes for columns used in query filters") that applies across all repositories
- The guidance should cross-reference the task's own implementation: if the task adds a column AND adds a filter using that column, flag the need for an index

## Acceptance Criteria
- [ ] The plan-feature skill cross-references new columns with query filter usage within the same task
- [ ] When a new column is used in query filters, the migration specification includes index creation guidance
- [ ] The guidance is method-level and does not prescribe database-specific index types (the specific index type, e.g., partial index, is left to the implementer based on project conventions)

## Test Requirements
- [ ] Verify that a task adding a filtered column includes index guidance in the migration specification
