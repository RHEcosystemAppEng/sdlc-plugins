# Task 2 — Collect ownerGroup during service onboarding

**Summary:** TC-9007: Collect and persist ownerGroup during initial service registration
**Labels:** ai-generated-jira
**Priority:** Major (inherited from TC-9007)
**Fix Versions:** (none; the Feature has no fixVersions)
**Epic group (by-sub-feature, pending approval):** Owner group capture

## Repository
catalog-service

## Target Branch
main

## Description
Extend the initial registration (onboarding) workflow so it accepts an `ownerGroup` value and persists it on the new Service Catalog record through the shared store helpers from Task 1. This covers the Feature requirement "A registered service record includes its `ownerGroup`".

Scope note: only the onboarding writer is in scope. Whether other catalog writers must also populate `ownerGroup` is an open scope conflict recorded in the TC-9007 impact map.

## Files to Modify
- `src/workflows/registration.py` — accept `ownerGroup` as onboarding input and pass it to the store when creating the catalog record

## Implementation Notes
- `src/workflows/registration.py` adds a service to the catalog during initial registration. Pass `ownerGroup` into the existing store create helper in `src/catalog/store.py` (extended in Task 1). Do not write directly to persistence or duplicate schema logic.
- Decide with the reviewer whether `ownerGroup` is required at onboarding. The Feature AC says every record has an `ownerGroup` after creation, so validate that a non-empty value is supplied and reject registration with a clear validation error otherwise, rather than silently persisting an empty owner group.
- Keep existing registration behavior (ID assignment, other fields) unchanged.
- Constraints (docs/constraints.md): §2 commit rules (TC task ID footer, Conventional Commits, `Assisted-by:`); §3 PR to `main` with `--base main`; §5.1 file scope; §5.4 reuse store helpers; §5.6 trace onboarding input → store → persisted record.

## Reuse Candidates
- `src/catalog/store.py` — shared record create helper with `ownerGroup` support (from Task 1)

## Acceptance Criteria
- [ ] Registering a service with an `ownerGroup` creates a catalog record containing that `ownerGroup`
- [ ] Registration without a non-empty `ownerGroup` fails with a validation error and creates no record
- [ ] Existing registration behavior, including record ID assignment, is unchanged

## Test Requirements
- [ ] `tests/workflows/test_registration.py`: registration with `ownerGroup` persists the value on the created record
- [ ] `tests/workflows/test_registration.py`: registration with missing/empty `ownerGroup` is rejected and no record is written
- [ ] `tests/workflows/test_registration.py`: regression check that existing registration fields and the record ID are unchanged

## Dependencies
- Depends on: Task 1 — Add ownerGroup to the shared Service Catalog record schema
