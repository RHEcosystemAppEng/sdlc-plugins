# Repository Impact Map — TC-9007: Add an owner group to Service Catalog records

> Status: **PENDING USER DECISION on a scope conflict** (see "Unresolved scope conflict" below). The task set generated so far covers only the in-scope (onboarding-focused) paths and does **not** satisfy the shared-artifact acceptance criteria on its own.

## Shared-artifact lifecycle trace (Step 3)

Shared artifact: **Service Catalog record** (schema and persistence in `src/catalog/store.py`).

### Producers / writers

| Path | Workflow | Kind | Test coverage | In stakeholder scope? |
|---|---|---|---|---|
| `src/workflows/registration.py` | Initial registration / onboarding | Primary create | `tests/workflows/test_registration.py` | Yes |
| `src/workflows/scheduled_sync.py` | Scheduled provider metadata sync | Scheduled / background update | `tests/workflows/test_scheduled_sync.py` | **No** (outside "onboarding flow" focus) |
| `src/workflows/fallback_import.py` | Import of previously exported data when provider sync is unavailable | Fallback / recovery populate | `tests/workflows/test_fallback_import.py` | **No** |
| `src/api/on_demand_refresh.py` | `POST /api/catalog/refresh` operator-requested refresh | On-demand / manual / API update | `tests/api/test_on_demand_refresh.py` | **No** |

Shared persistence layer used by all writers: `src/catalog/store.py` (tests: `tests/catalog/test_store.py`).

### Consumers / readers

| Path | Consumer | Test coverage |
|---|---|---|
| `src/api/catalog_summary.py` | Catalog summary API | `tests/api/test_catalog_summary.py` |
| `src/reports/catalog_export.py` | Downloadable catalog report | `tests/reports/test_catalog_export.py` |

## Repository Impact Map (in-scope changes)

```
catalog-service:
  changes:
    - Add an ownerGroup field to the shared Service Catalog record schema and persistence helpers (src/catalog/store.py)
    - Make the persistence helpers preserve the stored ownerGroup on update unless a new value is supplied (src/catalog/store.py)
    - Collect ownerGroup during initial registration and persist it on the created record (src/workflows/registration.py)
    - Expose ownerGroup in the catalog summary API response (src/api/catalog_summary.py)
    - Include ownerGroup in the downloadable catalog report (src/reports/catalog_export.py)
    - Add tests for store schema/preservation, registration, summary API, and export
    - Update documentation describing the ownerGroup field and catalog population paths (documentation task)
```

## Unresolved scope conflict (requires user decision before finalizing tasks)

The stakeholder/Feature instructs: *"Keep the implementation small and focus on the onboarding flow where records are first created"* and prefers a single task. However, the Feature acceptance criteria apply to the shared artifact across **all** population paths:

| Acceptance criterion | Covered by onboarding-only scope? | Gap |
|---|---|---|
| "Every Service Catalog record has an `ownerGroup` value after creation **or update**." | **No** | Updates happen through `src/workflows/scheduled_sync.py`, `src/workflows/fallback_import.py`, and `src/api/on_demand_refresh.py`. None of these writers (or `tests/workflows/test_scheduled_sync.py`, `tests/workflows/test_fallback_import.py`, `tests/api/test_on_demand_refresh.py`) are in scope, so there is no guarantee or test that they set or preserve `ownerGroup`. |
| "The summary API and downloadable report display `ownerGroup` for a record **regardless of how that record was populated**." | **No** | Records created or replaced by fallback import (and possibly refreshed by scheduled sync / on-demand refresh) are not exercised; the consumers are only validated with onboarding-created records. |
| "Updates to a service record preserve the current owner group unless a new value is supplied" (MVP requirement) | **No** | All update paths are the excluded writers. A preservation rule in `src/catalog/store.py` helps only if every writer goes through the same helper and does not replace the whole record (fallback import "loads previously exported data" and may overwrite) — this must be verified per writer and tested per writer. |
| "Existing catalog population behavior and stable IDs remain unchanged." | **Partially** | Stable-ID / population regression tests are needed for every writer that touches the record, not only registration. |

**Excluded paths needed by the acceptance criteria (unresolved):**

- `src/workflows/scheduled_sync.py` + `tests/workflows/test_scheduled_sync.py`
- `src/workflows/fallback_import.py` + `tests/workflows/test_fallback_import.py`
- `src/api/on_demand_refresh.py` + `tests/api/test_on_demand_refresh.py`

**Question for the user / stakeholder — please choose one:**

1. **Expand scope (recommended).** Add a second implementation task, "Preserve and populate `ownerGroup` in scheduled sync, fallback import, and on-demand refresh", covering the three writers above with path-specific tests (ownerGroup preserved on update when not supplied, overwritten only when supplied, fallback-imported records carry `ownerGroup` from the export or a defined default, stable IDs unchanged), plus consumer tests using records from each path. This makes a single task impractical; the plan would be 2 implementation tasks + 1 documentation task.
2. **Narrow the acceptance criteria.** Formally amend TC-9007 so the "after update" and "regardless of how populated" criteria and the update-preservation requirement are deferred to a follow-up Feature. The current task set would then fully cover the (narrowed) criteria.

Until one option is approved, the shared-artifact criteria above are **not** considered covered, and the excluded paths are intentionally not listed in any task's Files to Modify or Test Requirements.

## Excluded requirements

- None excluded for missing inputs. (The requirements above are blocked by a scope conflict, not by missing inputs.) No Figma design was provided; none is needed — this feature has no UI mockup requirements.

## Workflow mode decision (Step 4.5)

- **Mode: `direct-to-main`**
- Rationale: single repository (`catalog-service`). The new `ownerGroup` field is additive: the schema change, the registration writer, and both consumers land together in Task 1, so no coordinated migration across tasks, no breaking API change (summary API response gains an additive field), no cross-cutting rename, and no frontend/backend split. If scope option 1 is approved, the additional writer task depends on Task 1 but merging Task 1 alone leaves `main` working (writers that do not yet set `ownerGroup` keep functioning), so the mode remains `direct-to-main`.

---
This comment was AI-generated by [sdlc-workflow/plan-feature](https://github.com/RHEcosystemAppEng/sdlc-plugins) v0.14.0.
