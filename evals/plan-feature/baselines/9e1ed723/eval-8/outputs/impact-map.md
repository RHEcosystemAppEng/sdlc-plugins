# Repository Impact Map — TC-9007: Add an owner group to Service Catalog records

## Shared-artifact lifecycle trace (Step 3)

**Shared artifact:** the Service Catalog record (schema and persistence in `src/catalog/store.py`).

The Feature acceptance criteria depend on the contents of this shared record ("Every Service Catalog record has an `ownerGroup` value after creation or update", "display `ownerGroup` ... regardless of how that record was populated"). I traced the record through every path the repository structure shows.

| Role | Path | Test coverage | In stakeholder scope? |
|---|---|---|---|
| Schema / persistence (shared) | `src/catalog/store.py` | `tests/catalog/test_store.py` | Yes |
| Producer: initial registration (primary) | `src/workflows/registration.py` | `tests/workflows/test_registration.py` | Yes |
| Producer: scheduled synchronization (background) | `src/workflows/scheduled_sync.py` | `tests/workflows/test_scheduled_sync.py` | **No (excluded by stakeholder)** |
| Producer: fallback import (recovery) | `src/workflows/fallback_import.py` | `tests/workflows/test_fallback_import.py` | **No (excluded by stakeholder)** |
| Producer: on-demand refresh (`POST /api/catalog/refresh`) | `src/api/on_demand_refresh.py` | `tests/api/test_on_demand_refresh.py` | **No (excluded by stakeholder)** |
| Consumer: summary API | `src/api/catalog_summary.py` | `tests/api/test_catalog_summary.py` | Yes |
| Consumer: downloadable report | `src/reports/catalog_export.py` | `tests/reports/test_catalog_export.py` | Yes |

Note: the target repository (`catalog-service`) is described only in the Feature's repository structure table. It is not in the CLAUDE.md Repository Registry and has no Serena instance, so I could not check for CONVENTIONS.md, `docs/testing-readiness.md`, or existing symbols. I used the file paths given in the Feature as the repository evidence.

## Impact map

```
catalog-service:
  changes:
    - Add an ownerGroup field to the shared Service Catalog record schema and persistence helpers, keeping the current owner group on update when no new value is supplied (src/catalog/store.py)
    - Collect ownerGroup during initial onboarding and persist it on the new catalog record (src/workflows/registration.py)
    - Expose ownerGroup in the catalog summary API response (src/api/catalog_summary.py)
    - Include ownerGroup in the downloadable catalog report (src/reports/catalog_export.py)
    - Add focused tests for the store, registration, summary API, and report (tests/catalog/test_store.py, tests/workflows/test_registration.py, tests/api/test_catalog_summary.py, tests/reports/test_catalog_export.py)
    - Update documentation for the ownerGroup field (documentation task; the multi-path statement depends on how the scope conflict below is resolved)
```

## UNRESOLVED: scope conflict (clarification required)

The stakeholder asked for an onboarding-and-display-only change and explicitly excluded scheduled synchronization, fallback import, and on-demand refresh. The repository evidence shows that all three paths also write to the same shared Service Catalog record. Because of that, the planned tasks **do not fully satisfy** these Feature acceptance criteria:

| Acceptance criterion | Status with current scope | Uncovered paths / coverage gap |
|---|---|---|
| Every Service Catalog record has an `ownerGroup` value after creation or **update** | **Unresolved / partially covered**: only records created through registration are covered. The store-level preserve-on-update helper is planned, but nothing verifies that the excluded writers call it or send `ownerGroup`. | `src/workflows/scheduled_sync.py` + `tests/workflows/test_scheduled_sync.py`; `src/workflows/fallback_import.py` + `tests/workflows/test_fallback_import.py`; `src/api/on_demand_refresh.py` + `tests/api/test_on_demand_refresh.py`. Records created or replaced by these paths may lack `ownerGroup`, or may lose an existing value if a writer replaces the whole record instead of merging. |
| Summary API and downloadable report display `ownerGroup` for a record **regardless of how that record was populated** | **Unresolved / partially covered**: the consumers will read and render the field, but `ownerGroup` will only be populated reliably on registration-created records. No test covers records written by sync, fallback import, or refresh. | Same three producer paths and their tests as above. |
| Updates preserve the current owner group unless a new value is supplied (Requirement 3) | **Unresolved / partially covered**: the preserve semantics are implemented and tested in the shared store, but the Feature itself says "the record may be refreshed after onboarding", and the refresh/sync/import paths that actually do those updates are out of scope. | `src/api/on_demand_refresh.py`, `src/workflows/scheduled_sync.py`, `src/workflows/fallback_import.py` and their tests. |
| Existing catalog population behavior and stable IDs remain unchanged | Covered for registration and store (regression tests in Tasks 1 and 2). Not verified for the three excluded producers. | Same three producer paths: there are no regression tests for stable IDs on those paths. |

**Question for the stakeholder / engineer:**

> The `ownerGroup` acceptance criteria apply to every Service Catalog record, but three other workflows (scheduled sync, fallback import, on-demand refresh) also create or update those records. Please choose one:
> 1. **Expand scope**: add tasks (source and tests) for `src/workflows/scheduled_sync.py`, `src/workflows/fallback_import.py`, and `src/api/on_demand_refresh.py` so the criteria are fully met.
> 2. **Narrow the acceptance criteria**: reword them to cover only records created through onboarding, and treat records populated by other paths as a known gap or follow-up Feature.
> 3. **Hybrid**: keep this Feature as onboarding-and-display and create a linked follow-up Feature for the other population paths.

Until the scope is expanded with approval, the excluded paths do **not** appear in any task's Files to Modify, Files to Create, or Test Requirements. They are listed only here as unresolved impact-map paths.

## Excluded requirements

- None was dropped silently. Requirement 3 (preserve owner group on update) and the "regardless of how populated" criterion are only partly planned. See the unresolved scope conflict above.

## Workflow mode decision (Step 4.5)

**Mode: `direct-to-main`**

Rationale: I checked the four atomicity indicators.
- Coordinated schema migrations: no. The `ownerGroup` field is additive and optional/defaulted at the store layer (Task 1), so it can merge on its own without breaking existing readers or writers.
- Breaking API changes: no. The summary API and report gain a field; no existing field or path changes.
- Cross-cutting refactors: no.
- Tightly coupled components: no. Each task leaves `main` working. Consumers render an empty/absent owner group until producers populate it.

Tasks are sequenced with Dependencies (Task 1 before Tasks 2–4) but do not need a feature branch.
