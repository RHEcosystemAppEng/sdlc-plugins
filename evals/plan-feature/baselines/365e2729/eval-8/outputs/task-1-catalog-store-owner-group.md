# Task 1 — Add ownerGroup to the shared Service Catalog record schema and persistence

**Summary:** TC-9007: Add ownerGroup to Service Catalog record schema and store helpers
**Labels:** ai-generated-jira
**Priority:** Major (inherited from TC-9007)
**Epic group (by-sub-feature):** Owner group data model and onboarding

## Repository
catalog-service

## Target Branch
main

## Description
Add an `ownerGroup` field to the shared Service Catalog record so each service record can carry its owning group. The persistence helpers must keep an existing `ownerGroup` when an update omits the field, and must apply a new value when one is supplied. Stable record IDs and existing population behavior must not change. This is the foundation for the registration (Task 2) and display (Task 3) changes in TC-9007.

Scope note: the Feature's universal criterion ("every record has `ownerGroup` after creation or update") is **unresolved** pending stakeholder scope clarification (see the impact map). This task provides store-level semantics only. It does not change or test any writer other than registration (Task 2).

## Files to Modify
- `src/catalog/store.py` — add `ownerGroup` to the record schema; update create/update persistence helpers with preserve-on-omit and replace-on-supply semantics
- `tests/catalog/test_store.py` — add persistence tests for `ownerGroup`

## Implementation Notes
- `src/catalog/store.py` is the single shared schema and persistence module for Service Catalog records. Add `ownerGroup` there rather than in individual workflows, so every caller of the store helpers sees the same contract.
- Update semantics: when an update payload does not contain `ownerGroup` (key absent), keep the stored value. When it contains a value, replace it. Decide explicitly how an explicit `None`/empty value is handled, and document that choice in a docstring. Do not treat "absent" and "explicit replacement" as the same thing.
- Make the field optional at the schema level (nullable, with a default) so existing records and existing callers keep loading and saving without changes. "Existing catalog population behavior remains unchanged" is an acceptance criterion.
- Do not change how record IDs are generated or matched. Updates must still resolve to the same stable ID.
- Follow the existing schema and helper patterns already in `src/catalog/store.py` (field declaration style, serialization, and update/merge helper). Extend the existing update helper rather than adding a parallel one.
- Constraints (docs/constraints.md): §2 commit rules (Conventional Commits, Jira ID footer `Implements <task-key>`, `Assisted-by:` trailer); §3 PR rules (`--base main`, link the PR on the Jira task); §5 code change rules (change only the listed files, inspect before modifying, reuse existing helpers, check parity with sibling fields); §1.4/§1.5 implement-task scope rules.

## Reuse Candidates
- `src/catalog/store.py` — existing record schema and update/persistence helpers; extend these instead of writing new persistence code

## Acceptance Criteria
- [ ] The Service Catalog record schema includes an optional `ownerGroup` field
- [ ] Creating a record with `ownerGroup` persists it, and reading the record back returns it
- [ ] Updating a record without `ownerGroup` keeps the previously stored `ownerGroup`
- [ ] Updating a record with a new `ownerGroup` replaces the stored value
- [ ] Record IDs stay stable across create and update. No ID is regenerated or changed by this work
- [ ] Records saved before this change, without `ownerGroup`, still load and save without errors

## Test Requirements
- [ ] `tests/catalog/test_store.py`: create a record with `ownerGroup` and assert it is persisted and returned
- [ ] `tests/catalog/test_store.py`: update a record with the `ownerGroup` key omitted and assert the existing value is kept
- [ ] `tests/catalog/test_store.py`: update a record with a new `ownerGroup` and assert the value is replaced
- [ ] `tests/catalog/test_store.py`: assert the record ID is unchanged after create followed by update
- [ ] `tests/catalog/test_store.py`: load and save a legacy record that has no `ownerGroup` and assert existing behavior is unchanged

## Dependencies
- None
