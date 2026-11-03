# Repository Impact Map — TC-9007: Add an owner group to Service Catalog records

## Shared-artifact producer and consumer analysis

**Shared artifact:** the Service Catalog record (schema and persistence in `src/catalog/store.py`).

The acceptance criteria are about the shared artifact, not one workflow:

- "Every Service Catalog record has an `ownerGroup` value after creation **or update**."
- "The summary API and downloadable report display `ownerGroup` for a record **regardless of how that record was populated**."
- "Existing catalog population behavior and stable IDs remain unchanged."

So every path that writes the catalog record is in scope, along with every path that reads it. The repository structure shows four population paths. Registration is only one of them.

### Producers / writers

| # | Path | Kind | Source | Tests | What has to change |
|---|---|---|---|---|---|
| P0 | Catalog schema + persistence helpers | Shared schema | `src/catalog/store.py` | `tests/catalog/test_store.py` | Add `ownerGroup` to the record schema. Persistence must reject a missing or empty `ownerGroup` (fail closed). The merge-on-update helper keeps the existing value when the incoming value is absent. |
| P1 | Initial registration (onboarding) | Primary | `src/workflows/registration.py` | `tests/workflows/test_registration.py` | Collect `ownerGroup` during registration and persist it on the new record. |
| P2 | Scheduled synchronization | Scheduled / background | `src/workflows/scheduled_sync.py` | `tests/workflows/test_scheduled_sync.py` | Preserve the existing `ownerGroup` when refreshing provider metadata. Set `ownerGroup` on any record this path creates. Do not change sync behavior or stable IDs. |
| P3 | Fallback import | Fallback / recovery | `src/workflows/fallback_import.py` | `tests/workflows/test_fallback_import.py` | Carry `ownerGroup` from previously exported data when present. Otherwise keep the stored value. Records that the import creates must have `ownerGroup`. Do not change import behavior or stable IDs. |
| P4 | On-demand refresh (`POST /api/catalog/refresh`) | On-demand / manual / API | `src/api/on_demand_refresh.py` | `tests/api/test_on_demand_refresh.py` | Keep the current `ownerGroup` unless the request supplies a new value. Never clear it during a refresh. |

### Consumers / readers

| # | Path | Source | Tests | What has to change |
|---|---|---|---|---|
| C1 | Catalog summary API | `src/api/catalog_summary.py` | `tests/api/test_catalog_summary.py` | Add `ownerGroup` to each record in the summary response. |
| C2 | Downloadable report | `src/reports/catalog_export.py` | `tests/reports/test_catalog_export.py` | Add an `ownerGroup` column or field to the export. |

### Scope reconciliation (needs stakeholder confirmation)

The stakeholder sees this as "mainly an onboarding change" and wants the plan small. The repository evidence contradicts that framing:

- If only `src/workflows/registration.py` changes, three other writers still populate the same record: `src/workflows/scheduled_sync.py`, `src/workflows/fallback_import.py` and `src/api/on_demand_refresh.py`. Depending on how each one writes, it could do either of two things:
  - **Drop or overwrite `ownerGroup`** on update. That breaks AC "has an `ownerGroup` value after creation or update" and requirement "Updates … preserve the current owner group".
  - **Create records without `ownerGroup`** when the record first appears through sync, fallback import or refresh. Those records would then show a blank owner in the summary API and report, which breaks AC "regardless of how that record was populated".
- **Coverage gap if the scope were onboarding-only.** Nothing would test `tests/workflows/test_scheduled_sync.py`, `tests/workflows/test_fallback_import.py` or `tests/api/test_on_demand_refresh.py` for `ownerGroup` preservation or population. Nothing would test that stable IDs stay unchanged on those paths.

**Resolution in this plan.** The stakeholder asked for focus and a small plan. Nobody explicitly excluded any population path. So the plan keeps the stakeholder's preferences where it can:

- one implementation task;
- one repository;
- a narrow, additive field change;
- no change to population behavior.

That single task covers all four writers and both readers. The alternative paths were not dropped, because dropping them would leave the shared-artifact criteria unmet.

**Question for the stakeholder.** Please confirm you accept writers P2–P4 in scope. If you want them **excluded**, these acceptance criteria become **unresolved** and are not covered by the plan:

- "has an `ownerGroup` value after creation or update"
- "display `ownerGroup` … regardless of how that record was populated"
- "Updates … preserve the current owner group"

In that case the plan would remove `src/workflows/scheduled_sync.py`, `src/workflows/fallback_import.py` and `src/api/on_demand_refresh.py`, plus their tests, from the task. They would stay listed here as unresolved paths. A registration-only task set must not be presented as satisfying these criteria.

### Open questions (non-blocking; recorded in the task)

1. **Where `ownerGroup` comes from for records first created outside registration.** Options are provider metadata, the exported data, the refresh request, or a documented placeholder value such as `unassigned`. The feature does not say. The task requires a non-empty value and asks the implementer to confirm the source with the stakeholder.
2. **Legacy records persisted before this change.** They have no `ownerGroup` yet. The ACs only cover records created or updated after the change, so this plan has no backfill. Readers must handle a missing value without failing.

## Impact map

```
catalog-service:
  changes:
    - Add a required ownerGroup field to the shared Service Catalog record schema; reject missing or empty ownerGroup on persist; keep the stored value on update when no new value is supplied (src/catalog/store.py)
    - Collect ownerGroup during initial registration and store it on the new record (src/workflows/registration.py)
    - Keep ownerGroup through scheduled synchronization and set it on records sync creates, without changing sync behavior or stable IDs (src/workflows/scheduled_sync.py)
    - Keep or carry over ownerGroup through fallback import, without changing import behavior or stable IDs (src/workflows/fallback_import.py)
    - Keep ownerGroup on POST /api/catalog/refresh unless the request supplies a new value (src/api/on_demand_refresh.py)
    - Show ownerGroup in the catalog summary API response (src/api/catalog_summary.py)
    - Show ownerGroup in the downloadable catalog report (src/reports/catalog_export.py)
    - Add tests for every writer and reader above, including stable-ID and update-preservation checks (tests/catalog, tests/workflows, tests/api, tests/reports)
    - Document that all four population paths use the same catalog contract, including ownerGroup (documentation task)
```

### Excluded requirements

None. Every MVP requirement maps to the implementation task or the documentation task. The scope reconciliation above is waiting on stakeholder confirmation.

## Workflow mode decision

**Mode: `direct-to-main`**

Rationale: there is one implementation task in one repository. The schema change, all writers, both readers and their tests ship in a single PR. None of the atomicity indicators apply:

- **Coordinated schema migration across tasks:** not present. The schema change and every writer that depends on it are in the same task.
- **Breaking API change consumed by another task:** not present. The summary API and refresh endpoint changes are additive and in the same task.
- **Cross-cutting refactor split across tasks:** not present.
- **Tightly coupled frontend/backend split:** not present.

The documentation task depends on the implementation task. Merging it later does not break `main`.

## Planning context and assumptions

- **Code intelligence.** No Serena instance is configured. The repository is not in this project's Repository Registry, so its source could not be inspected. The file paths and their behavior come from the repository structure in the TC-9007 feature description.
- **CONVENTIONS.md:** not available for `catalog-service`. No convention enrichment was applied.
- **`docs/testing-readiness.md`:** not available for `catalog-service`. No testing tasks were generated.
- **Documentation signals:** Doc Impact = **Updates**, so a documentation task was generated.
- **Issue types / Epics.** Issue types could not be discovered offline. The Hierarchy Configuration default is `by-sub-feature`. If a level-1 (Epic) type is discovered, both tasks form one sub-feature and go under a single Epic, "TC-9007: Service Catalog owner group". If no level-1 type exists, tasks link directly to the Feature.
- **Inherited fields:** priority **Major** is propagated to the tasks. fixVersions is **omitted** because the Feature has none.
- **Fail-open risk.** A writer could persist a blank or `None` `ownerGroup` without any error. The record would look fine but display an empty owner. The task lowers this into a fail-closed acceptance criterion and test at the `src/catalog/store.py` persist gate.

---
This comment was AI-generated by [sdlc-workflow/plan-feature](https://github.com/RHEcosystemAppEng/sdlc-plugins) v0.13.10.
