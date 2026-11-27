# Repository Impact Map — TC-9007: Add an owner group to Service Catalog records

> Status: **PENDING SCOPE CLARIFICATION.** The planned onboarding-and-display changes are listed below. Two Feature acceptance criteria apply to the shared Service Catalog record across *all* population paths. The stakeholder has excluded those paths, so the criteria are recorded as **unresolved**. They are not claimed as covered.

## Analysis context

- Repository analysed: `catalog-service`. It is the only repository in the Feature's Repository Structure. No Serena instance is configured, so the analysis used the repository structure in the Feature description.
- Shared artifact: the **Service Catalog record**. Its schema and persistence helpers are in `src/catalog/store.py`.
- CONVENTIONS.md: none found for `catalog-service`. No convention enrichment applies.
- Testing readiness template (`docs/testing-readiness.md`): none found. No testing tasks are generated.
- Eval infrastructure: not applicable, because no skill `SKILL.md` is modified.

## Shared-artifact producer / consumer trace (Service Catalog record)

| Role | Path | Test path | Planning status |
|---|---|---|---|
| Schema / persistence (shared) | `src/catalog/store.py` | `tests/catalog/test_store.py` | **In scope** (Task 1) |
| Writer: initial registration (primary) | `src/workflows/registration.py` | `tests/workflows/test_registration.py` | **In scope** (Task 2) |
| Writer: scheduled synchronization | `src/workflows/scheduled_sync.py` | `tests/workflows/test_scheduled_sync.py` | **UNRESOLVED: excluded by stakeholder** |
| Writer: fallback import (recovery) | `src/workflows/fallback_import.py` | `tests/workflows/test_fallback_import.py` | **UNRESOLVED: excluded by stakeholder** |
| Writer: on-demand refresh (`POST /api/catalog/refresh`) | `src/api/on_demand_refresh.py` | `tests/api/test_on_demand_refresh.py` | **UNRESOLVED: excluded by stakeholder** |
| Consumer: summary API | `src/api/catalog_summary.py` | `tests/api/test_catalog_summary.py` | **In scope** (Task 3) |
| Consumer: downloadable report | `src/reports/catalog_export.py` | `tests/reports/test_catalog_export.py` | **In scope** (Task 4) |

## catalog-service

  changes:
    - Add an `ownerGroup` field to the shared Service Catalog record schema and persistence helpers. When an update omits `ownerGroup`, keep the stored value. When an update supplies a new value, replace the stored value. Stable record IDs and existing population behavior must not change.
    - Collect `ownerGroup` during initial service registration and persist it on the newly created catalog record.
    - Expose `ownerGroup` for each record in the catalog summary API response.
    - Include `ownerGroup` for each record in the downloadable catalog report.
    - Update documentation for the `ownerGroup` field in the Service Catalog record contract (documentation task).

## Scope conflict — unresolved acceptance criteria

The stakeholder instruction says this is "strictly an onboarding-and-display change" and asks that files and tests for scheduled synchronization, fallback import and on-demand refresh be left out. The Feature's acceptance criteria apply to the shared record, so that instruction conflicts with them:

| Feature acceptance criterion | Status under current scope | Gap |
|---|---|---|
| "Every Service Catalog record has an `ownerGroup` value after creation or update." | **UNRESOLVED / NOT COVERED** | Records created or updated by scheduled sync, fallback import or on-demand refresh are not validated. If those writers rebuild or replace records instead of calling the shared update helper, they could drop or omit `ownerGroup`. Registration and the store-level preservation logic alone cannot show the criterion holds for every update path. |
| "The summary API and downloadable report display `ownerGroup` for a record regardless of how that record was populated." | **PARTIALLY COVERED, UNRESOLVED** | Tasks 3 and 4 verify the consumers using records created by registration and directly through the store. They do not verify records produced by the three excluded writers. |
| "Existing catalog population behavior and stable IDs remain unchanged." | **PARTIALLY COVERED, UNRESOLVED** | Task 1 covers stable IDs and update semantics at the store level, and Task 2 covers registration. The three excluded writers have no regression tests in this plan. |
| Requirement: "Updates to a service record preserve the current owner group unless a new value is supplied (record may be refreshed after onboarding)" | **PARTIALLY COVERED, UNRESOLVED** | Store-level preservation is covered in Task 1. The refresh and update callers are the three excluded writers, and they are not validated. |

### Excluded paths (unresolved; not included in any task)

- `src/workflows/scheduled_sync.py` with `tests/workflows/test_scheduled_sync.py`. Path-specific gap: no test shows a scheduled sync update keeps the existing `ownerGroup` when the provider payload omits it, or applies a supplied replacement.
- `src/workflows/fallback_import.py` with `tests/workflows/test_fallback_import.py`. Path-specific gap: no test shows that imported records from previously exported data, which may come from before `ownerGroup` existed, end up with an `ownerGroup` value, or that an existing value is kept.
- `src/api/on_demand_refresh.py` with `tests/api/test_on_demand_refresh.py`. Path-specific gap: no test shows that `POST /api/catalog/refresh` keeps `ownerGroup` when it is omitted and applies a supplied replacement.
- Consumer coverage gap: `tests/api/test_catalog_summary.py` and `tests/reports/test_catalog_export.py` do not exercise records produced by the three excluded writers.

### Clarification requested

Please choose one option before the universal acceptance criteria can be treated as satisfied:

1. **Expand scope.** Add tasks, or extend the existing ones, for the three excluded writers and their tests, and extend the consumer tests to records from every writer.
2. **Amend the Feature.** Narrow the acceptance criteria to records created through registration, and revise the Documentation Considerations to match. The excluded paths could then be tracked in a separate follow-up Feature.
3. **Accept the risk explicitly.** Record that the criteria stay unmet for non-registration paths.

Until a decision is made, the generated tasks cover only the in-scope paths above. None of them claims to satisfy the universal criteria.

## Excluded requirements

- **Documentation Considerations: "document that catalog records may be populated through registration, scheduled synchronization, fallback import, or on-demand refresh".** This is only partially plannable under the current scope. The documentation task covers the `ownerGroup` field contract and the registration path. Stating that all four paths honor the `ownerGroup` contract depends on resolving the scope conflict above. Missing input: a stakeholder decision on the excluded writer paths.

## Workflow mode

`direct-to-main`. See `workflow-mode-comment.md`.

---
This comment was AI-generated by [sdlc-workflow/plan-feature](https://github.com/RHEcosystemAppEng/sdlc-plugins) v0.14.0.
