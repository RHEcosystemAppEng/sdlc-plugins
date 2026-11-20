# Repository Impact Map — TC-9007: Add an owner group to Service Catalog records

## Planning context and assumptions

- **Feature**: TC-9007 (Priority: Major, Fix Versions: none)
- **Target repository**: `catalog-service` (single repository). No Serena instance is registered for it, so the analysis used the repository structure listed in the Feature description as the repository evidence (Glob/Read fallback). No `CONVENTIONS.md` or `docs/testing-readiness.md` was found in that structure, so no convention enrichment or testing tasks apply.
- **Figma**: no Figma link in the Feature; Step 2 skipped.
- **Parent link (Step 1.5)**: no parent supplied (non-interactive run); skipped.
- **Issue types (Step 2.5)**: assumed the TC project has a level-1 "Epic" type (Jira not queried in this eval). CLAUDE.md Hierarchy Configuration sets the grouping strategy to `by-sub-feature`.
- **Stakeholder scope instruction**: "Strictly an onboarding-and-display change. Do not include files or tests for scheduled synchronization, fallback import, or on-demand refresh."

## Shared-artifact producer and consumer analysis (Step 3)

**Shared artifact:** the Service Catalog record (schema and persistence in `src/catalog/store.py`). The acceptance criteria are about this record ("every record", "regardless of how populated"), so every path that writes it or reads it is in the criteria's reach.

| Role | Path | Source file | Test file | Covered by the planned tasks? |
|---|---|---|---|---|
| Schema / persistence | Shared record schema and helpers | `src/catalog/store.py` | `tests/catalog/test_store.py` | Yes (Task 1) |
| Producer: primary | Initial registration / onboarding | `src/workflows/registration.py` | `tests/workflows/test_registration.py` | Yes (Task 2) |
| Producer: scheduled/background | Scheduled provider synchronization | `src/workflows/scheduled_sync.py` | `tests/workflows/test_scheduled_sync.py` | **No (out of scope per stakeholder, UNRESOLVED)** |
| Producer: fallback/recovery | Fallback import of previously exported data | `src/workflows/fallback_import.py` | `tests/workflows/test_fallback_import.py` | **No (out of scope per stakeholder, UNRESOLVED)** |
| Producer: on-demand/API | `POST /api/catalog/refresh` operator refresh | `src/api/on_demand_refresh.py` | `tests/api/test_on_demand_refresh.py` | **No (out of scope per stakeholder, UNRESOLVED)** |
| Consumer | Catalog summary API | `src/api/catalog_summary.py` | `tests/api/test_catalog_summary.py` | Yes (Task 3) |
| Consumer | Downloadable catalog report | `src/reports/catalog_export.py` | `tests/reports/test_catalog_export.py` | Yes (Task 4) |

## Impact map

```
catalog-service:
  changes:
    - Add an ownerGroup field to the shared Service Catalog record schema and persistence helpers, with update semantics that keep the stored ownerGroup unless a new value is supplied and leave record IDs unchanged (src/catalog/store.py, tests/catalog/test_store.py)
    - Collect ownerGroup during initial registration and persist it on the new catalog record (src/workflows/registration.py, tests/workflows/test_registration.py)
    - Expose ownerGroup in the catalog summary API response (src/api/catalog_summary.py, tests/api/test_catalog_summary.py)
    - Include ownerGroup in the downloadable catalog report (src/reports/catalog_export.py, tests/reports/test_catalog_export.py)
    - Update operator/API documentation about the ownerGroup catalog contract (documentation task)
```

## UNRESOLVED: scope conflict with the shared-record acceptance criteria

The stakeholder's exclusion conflicts with three Feature acceptance criteria and one MVP requirement. Registration and display changes alone **do not** satisfy them. I have **not** marked these criteria as covered by the planned tasks.

| Feature criterion / requirement | Why onboarding + display alone does not satisfy it | Excluded paths needed to close the gap |
|---|---|---|
| AC1: "Every Service Catalog record has an `ownerGroup` value after creation or update." | Records can also be created or updated by scheduled sync, fallback import, and on-demand refresh. Nothing in scope makes sure those writers set or keep `ownerGroup`. | `src/workflows/scheduled_sync.py` + `tests/workflows/test_scheduled_sync.py`; `src/workflows/fallback_import.py` + `tests/workflows/test_fallback_import.py`; `src/api/on_demand_refresh.py` + `tests/api/test_on_demand_refresh.py` |
| AC2: "The summary API and downloadable report display `ownerGroup` for a record regardless of how that record was populated." | The consumers will render the field. But records written by the excluded paths may have no value, or may have had it overwritten, so there would be nothing correct to display. | Same three writer/test pairs as above |
| AC3: "Existing catalog population behavior and stable IDs remain unchanged." | Task 1 changes the shared store. Without regression tests on the three other writers, nobody verifies that their population behavior and IDs stay the same after the schema change. | `tests/workflows/test_scheduled_sync.py`, `tests/workflows/test_fallback_import.py`, `tests/api/test_on_demand_refresh.py` (and the matching source files if a fix turns out to be needed) |
| Requirement 3: "Updates to a service record preserve the current owner group unless a new value is supplied." | The update/refresh writers after onboarding are exactly the excluded paths (scheduled sync, fallback import, on-demand refresh). Task 1 adds a preserving merge helper in the store. Whether those writers use it, or overwrite whole records, cannot be verified or tested inside the current scope. | `src/workflows/scheduled_sync.py`, `src/workflows/fallback_import.py`, `src/api/on_demand_refresh.py` and their tests |

### Clarification requested from the stakeholder / engineer

Please choose one before these criteria are treated as covered:

1. **Expand scope**: add tasks (or extend Tasks 1–2) to update and test `scheduled_sync.py`, `fallback_import.py`, and `on_demand_refresh.py` so they set or keep `ownerGroup` and keep stable IDs. This is the only option that satisfies AC1–AC3 as written.
2. **Narrow the acceptance criteria**: reword AC1/AC2/Requirement 3 to apply only to records created through registration, and record the other writers as a known follow-up gap (new Feature or Task).
3. **Partial coverage with a tracked follow-up**: keep this plan as is and open a follow-up issue for the three writer paths. TC-9007 stays not done until the follow-up closes.

Until one of these is approved, the excluded paths appear **only** in this impact map. They are deliberately not in any task's Files to Modify, Files to Create, or Test Requirements.

## Excluded requirements

- None excluded for missing inputs. The writer paths above are excluded by **stakeholder scope instruction**, not by missing inputs, and are tracked as unresolved (see above).

## Workflow mode (Step 4.5)

- **Mode: `direct-to-main`**
- Rationale: no atomicity indicators found. The `ownerGroup` field is an additive, optional-on-read schema change. Merging Task 1 alone leaves `main` working. Tasks 2–4 depend on Task 1 but do not break anything if they land later. There is no breaking API change, coordinated migration, or cross-cutting refactor, and no frontend/backend split.

## Epic grouping (by-sub-feature, assumed approved)

- **TC-9007: Owner group capture**: Task 1 (store schema), Task 2 (registration)
- **TC-9007: Owner group display**: Task 3 (summary API), Task 4 (export report), Task 5 (documentation)

## Inherited fields

- Priority: **Major** (propagated to all Epics and Tasks)
- fixVersions: **omitted** (the Feature has no fixVersions; scope config is `both`, but there is nothing to inherit)
