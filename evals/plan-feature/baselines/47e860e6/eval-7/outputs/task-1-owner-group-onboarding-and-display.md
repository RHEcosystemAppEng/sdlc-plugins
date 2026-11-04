# Task 1 — Add `ownerGroup` to Service Catalog records for onboarding and display

**Summary:** TC-9007: Add ownerGroup to catalog schema, registration, summary API, and report
**Labels:** ai-generated-jira
**Priority:** Major (inherited from TC-9007)
**Fix Versions:** omitted (TC-9007 has none)

> **Draft, pending scope clarification.** This task covers the onboarding flow, the shared schema, and the consumers. The Feature's AC1, AC2, and Requirement 3 also depend on the scheduled sync, fallback import, and on-demand refresh writers. Those paths are listed as unresolved in the impact map and are **not** in scope here unless the stakeholder approves expanding scope. This task alone does **not** satisfy the Feature's "every record / regardless of how populated" criteria.

## Repository
catalog-service

## Target Branch
main

## Description
Add an `ownerGroup` field to the shared Service Catalog record so users can see who owns each service. Collect it during initial registration (onboarding), and show it in the catalog summary API and the downloadable report. The shared persistence helpers must keep an existing `ownerGroup` when a record is updated without a new value, so the field is not lost on later writes through the shared helper. Implements part of TC-9007.

## Files to Modify
- `src/catalog/store.py` — add `ownerGroup` to the shared catalog record schema; make the persistence/update helpers keep the stored `ownerGroup` when an update supplies none, and replace it when a new value is supplied
- `src/workflows/registration.py` — accept `ownerGroup` during initial registration and persist it on the new catalog record
- `src/api/catalog_summary.py` — include `ownerGroup` in each record of the summary API response
- `src/reports/catalog_export.py` — add an `ownerGroup` column/field to the downloadable report
- `tests/catalog/test_store.py` — schema and preserve-on-update persistence tests
- `tests/workflows/test_registration.py` — onboarding tests for `ownerGroup`
- `tests/api/test_catalog_summary.py` — summary API display tests
- `tests/reports/test_catalog_export.py` — report display tests

## API Changes
- Catalog summary API (`src/api/catalog_summary.py`) — MODIFY: each record in the response gains an `ownerGroup` field. This is an additive change; existing fields and IDs are unchanged.

## Implementation Notes
- **Shared artifact:** `src/catalog/store.py` is the single source of the record contract. Define `ownerGroup` there once. The registration writer and both readers must use that schema, not define their own field handling.
- **Preserve-on-update:** put the merge rule in the store's persistence/update helper: keep the stored `ownerGroup` unless the incoming update has a non-empty value. Do not change how records are keyed or how IDs are produced (AC3: stable IDs).
- **Registration:** in `src/workflows/registration.py`, take `ownerGroup` from the onboarding input and pass it through the existing store helper used to add the service. Keep the existing registration behavior otherwise unchanged.
- **Consumers:** `src/api/catalog_summary.py` and `src/reports/catalog_export.py` already read records from the shared store. Read `ownerGroup` from the record, and do not derive or default it in the consumer.
- **Out of scope pending clarification:** `src/workflows/scheduled_sync.py`, `src/workflows/fallback_import.py`, and `src/api/on_demand_refresh.py` also write catalog records. Do not modify them in this task unless the task description is updated after the stakeholder approves expanding scope (see the TC-9007 impact map comment).
- Constraints (docs/constraints.md):
  - §2 Commits: Conventional Commits format; footer references the Jira task ID; include `--trailer="Assisted-by: Claude Code"`.
  - §3 PRs: branch named after the task ID; `gh pr create --base main`; post the PR link on the Jira task.
  - §5 Code changes: change only the files listed above; inspect the code before modifying it; reuse the existing store helpers rather than duplicating persistence logic; trace `ownerGroup` end to end (registration input → store → summary API/report) before committing.

## Reuse Candidates
- `src/catalog/store.py` — existing record schema and persistence helpers. Extend them rather than adding a parallel write path for `ownerGroup`.
- `tests/catalog/test_store.py`, `tests/workflows/test_registration.py`, `tests/api/test_catalog_summary.py`, `tests/reports/test_catalog_export.py` — existing test modules and fixtures to extend for the new field.

## Acceptance Criteria
- [ ] The shared Service Catalog record schema in `src/catalog/store.py` includes `ownerGroup`
- [ ] A service registered through `src/workflows/registration.py` is persisted with the supplied `ownerGroup`
- [ ] Updating a record through the store's persistence helper without an `ownerGroup` keeps the existing value; updating with a new value replaces it
- [ ] The catalog summary API (`src/api/catalog_summary.py`) returns `ownerGroup` for each record
- [ ] The downloadable report (`src/reports/catalog_export.py`) includes `ownerGroup` for each record
- [ ] Stable record IDs and existing registration behavior are unchanged

## Test Requirements
- [ ] `tests/catalog/test_store.py`: a record saved with `ownerGroup` reads back with the same value
- [ ] `tests/catalog/test_store.py`: an update that omits `ownerGroup` keeps the stored value; an update with a new value replaces it
- [ ] `tests/catalog/test_store.py`: record IDs are unchanged by adding the field and by preserve-on-update writes
- [ ] `tests/workflows/test_registration.py`: registration with `ownerGroup` persists it on the created record; existing registration assertions (including the generated ID) still pass
- [ ] `tests/api/test_catalog_summary.py`: the summary response includes the record's `ownerGroup`
- [ ] `tests/reports/test_catalog_export.py`: the exported report includes the record's `ownerGroup`

## Documentation Updates
- Summary API reference (if the repo has one) — add the `ownerGroup` field to the summary record shape

## Dependencies
- None
