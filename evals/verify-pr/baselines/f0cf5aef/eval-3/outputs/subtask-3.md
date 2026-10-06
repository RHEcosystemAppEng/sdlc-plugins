## Repository
sdlc-plugins

## Target Branch
main

## Description
Improve the plan-feature skill to specify transaction requirements when planning tasks that involve multi-table cascade operations. The verification of TC-9103 revealed that the task's Implementation Notes described cascade update logic across three tables (sbom, sbom_package, sbom_advisory) but did not specify wrapping these operations in a database transaction. This led to an implementation without atomicity guarantees, which a reviewer correctly flagged as a data integrity risk.

The plan-feature skill should include a check: when generating Implementation Notes that describe operations spanning multiple database tables, add explicit guidance to use a transaction wrapper. This is a universal principle (not repo-specific) -- any multi-table mutation requires atomicity to prevent inconsistent state on partial failure.

## Files to Modify
- `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` -- add guidance in the task generation section to specify transaction requirements for multi-table operations

## Implementation Notes
- Add a check in the Implementation Notes generation logic: when the planned implementation involves UPDATE/INSERT/DELETE operations on multiple tables as part of a single logical operation, include a note to wrap them in a transaction
- This is a method-level improvement (language-agnostic: "wrap multi-table mutations in a transaction") that applies across all repositories, not a repo-specific convention
- The guidance should be conditional -- only triggered when the implementation involves coordinated mutations across multiple tables

## Acceptance Criteria
- [ ] The plan-feature skill checks for multi-table mutation patterns when generating Implementation Notes
- [ ] When multi-table mutations are detected, the generated Implementation Notes include explicit transaction requirements
- [ ] The guidance is method-level (e.g., "wrap these operations in a database transaction for atomicity") and does not prescribe language-specific APIs

## Test Requirements
- [ ] Verify that a task planning cascade operations across tables includes transaction guidance in Implementation Notes
