# Task 2 — Collect and persist ownerGroup during initial registration

**Summary:** TC-9007: Collect ownerGroup in the registration workflow
**Labels:** ai-generated-jira
**Priority:** Major (inherited from TC-9007)
**Epic group (by-sub-feature):** Owner group data model and onboarding

## Repository
catalog-service

## Target Branch
main

## Description
Extend the initial registration (onboarding) workflow so that a new service record collects an `ownerGroup` and stores it in the shared Service Catalog record. This covers the Feature requirement "A registered service record includes its `ownerGroup`".

Scope note: registration is the only writer planned in this Feature, as the stakeholder instructed. This task alone does not satisfy the universal criterion that every Service Catalog record has an `ownerGroup` regardless of population path. That criterion is unresolved pending scope clarification (see the impact map).

## Files to Modify
- `src/workflows/registration.py` — accept `ownerGroup` as registration input and pass it to the store create helper
- `tests/workflows/test_registration.py` — add registration tests for `ownerGroup`

## Implementation Notes
- `src/workflows/registration.py` adds a service to the catalog during initial registration. Pass `ownerGroup` through the existing store create helper in `src/catalog/store.py` (extended in Task 1). Do not write to persistence directly.
- Validate `ownerGroup` at the registration boundary using the same input validation pattern that `src/workflows/registration.py` already uses for its other required fields. Registration should reject a missing or empty `ownerGroup` so that newly onboarded records always have a value.
- Do not change how registration derives or assigns the record ID.
- Constraints (docs/constraints.md): §2 commit rules; §3 PR rules (`--base main`); §5 code change rules (change only the listed files, reuse the Task 1 store helpers, check parity with how the other registration fields are validated).

## Reuse Candidates
- `src/catalog/store.py` — record create helper with `ownerGroup` support (from Task 1)
- `src/workflows/registration.py` — existing input validation for registration fields

## Acceptance Criteria
- [ ] Registering a service with an `ownerGroup` creates a catalog record with that `ownerGroup` stored
- [ ] Registering a service without an `ownerGroup` is rejected with a validation error, and no record is created
- [ ] Registration still assigns stable record IDs exactly as before

## Test Requirements
- [ ] `tests/workflows/test_registration.py`: register a service with `ownerGroup` and assert the stored record contains the supplied value
- [ ] `tests/workflows/test_registration.py`: register without `ownerGroup` and assert a validation error is raised and no record is persisted
- [ ] `tests/workflows/test_registration.py`: assert the record ID produced by registration is unchanged compared with the existing behavior

## Dependencies
- Depends on: Task 1 — Add ownerGroup to the shared Service Catalog record schema and persistence
