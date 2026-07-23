## Repository
sdlc-plugins

## Target Branch
main

## Description
Add explicit guidance to the plan-feature skill's task generation logic to include transaction wrapping requirements in Implementation Notes when a task involves multiple related database write operations that must be atomic. The root cause of the reviewer-flagged defect in TC-9103 was that the plan-feature phase generated Implementation Notes describing cascade update logic (updating sbom, sbom_package, and sbom_advisory) without specifying that these operations must be wrapped in a database transaction. The implementer followed the notes literally and produced non-transactional code, which a reviewer caught as a consistency risk.

## Files to Modify
- `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` -- add a guidance rule in the task description generation section instructing the skill to check whether planned database operations involve multiple related writes (cascades, multi-table updates, parent-child modifications) and, when they do, include a transaction wrapping requirement in Implementation Notes

## Implementation Notes
- The gap is in the plan-feature skill's task generation phase: when it produces Implementation Notes for database operations, it should detect multi-table write patterns and add transactional atomicity guidance
- This is a method-based improvement (applies to any repository with database operations, not specific to Rust or SeaORM)
- The guidance should be expressed as a general rule: "When Implementation Notes describe operations that modify multiple related database tables, include a note requiring transactional wrapping to ensure atomicity"
- Do not embed language-specific API references (e.g., SeaORM transaction syntax) in the skill -- those belong in per-project CONVENTIONS.md

## Acceptance Criteria
- [ ] plan-feature skill includes transaction wrapping guidance in Implementation Notes when a task involves multiple related database write operations
- [ ] The guidance is method-based and language-agnostic (does not reference specific ORM APIs)

## Test Requirements
- [ ] Verify that a task description generated for a multi-table cascade operation includes transactional atomicity guidance in Implementation Notes
