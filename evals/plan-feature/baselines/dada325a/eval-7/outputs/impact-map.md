# Repository Impact Map — TC-9007: Add an owner group to Service Catalog records

> Analysis source: the repository structure in the Feature description (catalog-service).
> catalog-service has no Serena instance and is not in the CLAUDE.md Repository Registry,
> so the paths below come from the Feature's repository table. No CONVENTIONS.md,
> `docs/testing-readiness.md` or eval infrastructure is known for this repository.

## Scope conflict: stakeholder framing vs. acceptance criteria (needs your decision)

The stakeholder sees this as mostly an onboarding change and would like one task. The
Feature's own acceptance criteria apply to the **shared** Service Catalog record, not only
to onboarding:

- AC1: "Every Service Catalog record has an `ownerGroup` value after creation **or update**."
- AC2: "The summary API and downloadable report display `ownerGroup` for a record
  **regardless of how that record was populated**."
- AC3: "Existing catalog population behavior and stable IDs remain unchanged."

The repository has **four** workflows that write the shared record. Registration
(onboarding) is only one of them. If only `src/workflows/registration.py` changes, AC1
and AC2 are **not met** for records written or refreshed by scheduled sync, fallback
import, or on-demand refresh. Those paths could drop or blank an existing `ownerGroup`,
and the summary API and report would then show no value.

**Recommendation:** keep a single implementation task, as the stakeholder asked, but have
it cover every writer and reader of the shared record (listed below). One task is also
the safest delivery unit. If the store schema or validation required `ownerGroup` before
the non-onboarding writers carried or preserved it, `main` would break.

**Please confirm one of:**
1. **Approve the full shared-artifact scope** (recommended). Task 1 as drafted covers all
   writers and readers.
2. **Keep onboarding-only scope.** Task 1 is then reduced to the store, registration and
   the two readers. AC1 (update path) and AC2 ("regardless of how populated") stay
   **unresolved** for the paths listed under "Unresolved if scope is limited" below. The
   plan will not claim those criteria are satisfied.

The task files in this output assume option 1 and are **pending your approval of the
scope**.

## Shared-artifact lifecycle trace: Service Catalog record

| Role | Path | Kind | Effect on `ownerGroup` | Test coverage |
|---|---|---|---|---|
| Schema / persistence | `src/catalog/store.py` | Shared record schema + persistence helpers | Add field; central merge/preserve + validation on write | `tests/catalog/test_store.py` |
| Writer — primary | `src/workflows/registration.py` | Initial onboarding (create) | Collect and persist `ownerGroup` on creation | `tests/workflows/test_registration.py` |
| Writer — scheduled/background | `src/workflows/scheduled_sync.py` | Scheduled provider sync (update/upsert) | Must preserve existing `ownerGroup` unless a new value is supplied | `tests/workflows/test_scheduled_sync.py` |
| Writer — fallback/recovery | `src/workflows/fallback_import.py` | Loads previously exported data when provider sync is unavailable | Must carry `ownerGroup` from the export if present, otherwise preserve the existing value | `tests/workflows/test_fallback_import.py` |
| Writer — on-demand/API | `src/api/on_demand_refresh.py` | `POST /api/catalog/refresh`, operator-requested refresh | Must preserve existing `ownerGroup` unless the request supplies a new value | `tests/api/test_on_demand_refresh.py` |
| Reader | `src/api/catalog_summary.py` | Summary API | Expose `ownerGroup` | `tests/api/test_catalog_summary.py` |
| Reader | `src/reports/catalog_export.py` | Downloadable report | Include `ownerGroup` column/field | `tests/reports/test_catalog_export.py` |

Round trip: `catalog_export.py` produces the "previously exported service data" that
`fallback_import.py` consumes. The export must therefore include `ownerGroup` so that a
fallback import restores it instead of blanking it.

## Impact map

```
catalog-service:
  changes:
    - Add an ownerGroup field to the shared Service Catalog record schema and persistence helpers (src/catalog/store.py), with a single merge rule: keep the existing ownerGroup unless a new non-empty value is supplied
    - Reject (fail closed) any write that would persist a record without an ownerGroup after merging, instead of silently storing an empty value
    - Collect and persist ownerGroup during initial registration/onboarding (src/workflows/registration.py)
    - Keep the existing ownerGroup when scheduled sync refreshes a record (src/workflows/scheduled_sync.py)
    - Carry ownerGroup from exported data during fallback import, otherwise keep the existing value (src/workflows/fallback_import.py)
    - Keep the existing ownerGroup on POST /api/catalog/refresh unless a new value is supplied (src/api/on_demand_refresh.py)
    - Expose ownerGroup in the catalog summary API (src/api/catalog_summary.py)
    - Include ownerGroup in the downloadable catalog report/export (src/reports/catalog_export.py)
    - Add or extend tests for the store, all four writers and both readers, including no change to existing population behavior and stable IDs
    - Document that catalog records may be populated through registration, scheduled synchronization, fallback import, or on-demand refresh, and that all paths share the same catalog contract (including ownerGroup)
```

## Requirement to plan traceability

| Feature requirement / AC | Covered by | Status |
|---|---|---|
| Registered record includes `ownerGroup` (onboarding) | Task 1: `store.py`, `registration.py` | Covered |
| Summary API and report show `ownerGroup` | Task 1: `catalog_summary.py`, `catalog_export.py` | Covered |
| Updates keep the current owner group unless a new value is supplied | Task 1: `store.py` merge rule + `scheduled_sync.py`, `fallback_import.py`, `on_demand_refresh.py` | Covered (pending scope approval) |
| Focused tests for onboarding and display | Task 1 Test Requirements | Covered |
| AC1: every record has `ownerGroup` after creation **or update** | Task 1: all four writers + store validation | Covered (pending scope approval) |
| AC2: display regardless of how the record was populated | Task 1: all writers + both readers + export/import round trip | Covered (pending scope approval) |
| AC3: existing population behavior and stable IDs unchanged | Task 1: regression tests per writer | Covered |
| Doc Impact: Updates | Task 2 (documentation) | Covered |

### Unresolved if scope is limited (option 2 only)

If you choose onboarding-only scope, these paths would be left out and the related ACs stay
**open**:

- `src/workflows/scheduled_sync.py` / `tests/workflows/test_scheduled_sync.py`: an update
  may drop or blank `ownerGroup` (AC1 update, requirement 3)
- `src/workflows/fallback_import.py` / `tests/workflows/test_fallback_import.py`: imported
  records may lack `ownerGroup` (AC1, AC2)
- `src/api/on_demand_refresh.py` / `tests/api/test_on_demand_refresh.py`: an operator
  refresh may drop `ownerGroup` (AC1 update, AC2)

## Open questions (for clarification, do not block approval)

1. **Records created by a non-registration path.** If scheduled sync or fallback import
   creates a record that never went through onboarding, where does its `ownerGroup` come
   from? Options: the provider metadata field, an explicit "unassigned" sentinel, or
   rejecting the record. AC1 requires a value. The task currently specifies fail-closed
   validation in the store, so which value to use must be confirmed.
2. **Existing records.** Do records persisted before this feature need a backfill or
   migration to reach "every record has an ownerGroup"? Nothing in the Feature mentions
   one. Task 1 tolerates legacy records on read but will not invent values.

## Excluded requirements

None. Every requirement can be planned, provided the scope above is approved.

## Workflow mode decision

- **Mode:** `direct-to-main`
- **Rationale:** there is one implementation task, and the schema change, all writers and
  both readers land together in one PR. So no cross-task schema migration, API contract
  break, cross-cutting refactor or frontend/backend coupling spans several tasks. The
  documentation task (Task 2) does not affect runtime behavior and depends on Task 1.
  No atomicity indicator applies across tasks.
- All tasks target `main`.

## Epic grouping

Hierarchy Configuration default strategy: `by-sub-feature`. Proposed single Epic
**"TC-9007: Service Catalog ownerGroup"** containing Task 1 and Task 2 (subject to Epic
type discovery in the Jira project).

---
This comment was AI-generated by [sdlc-workflow/plan-feature](https://github.com/RHEcosystemAppEng/sdlc-plugins) v0.13.10.
