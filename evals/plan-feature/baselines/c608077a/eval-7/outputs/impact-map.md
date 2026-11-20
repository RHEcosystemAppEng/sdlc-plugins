# Repository Impact Map — TC-9007: Add an owner group to Service Catalog records

## Planning context and assumptions

- **Source**: Feature TC-9007 (mock), read from `feature-shared-artifact-multi-writer.md`. Jira, Figma, and Serena were not contacted (eval mode). No Figma link is present, so Step 2 was skipped.
- **Repository**: `catalog-service`. It is not listed in this project's Repository Registry and has no Serena instance. The file inventory in the Feature description is the only repository evidence, so all paths below come from that inventory. No `CONVENTIONS.md` or `docs/testing-readiness.md` is listed for `catalog-service`, so no convention enrichment is applied and no testing tasks are generated.
- **Parent link (Step 1.5)**: skipped. Assumed the user pressed Enter, since the Feature has no parent and linking is optional.
- **Issue types (Step 2.5)**: these could not be fetched. The CLAUDE.md `## Hierarchy Configuration` section sets the strategy to `by-sub-feature`, so this plan assumes TC has a level-1 type named "Epic". Grouping is one Epic, with the user's approval assumed (see `epic-1-service-catalog-owner-group.md`).
- **Priority**: Major. It is propagated to the Epic and all tasks.
- **fixVersions**: none on the Feature, so they are omitted from tasks. The fixVersion scope is `both`, but there is nothing to propagate.

## Shared-artifact producer / consumer analysis (Step 3)

The shared artifact is the **Service Catalog record**, defined in `src/catalog/store.py`. Two Feature acceptance criteria apply to the artifact as a whole, not to one workflow:

- AC1: "Every Service Catalog record has an `ownerGroup` value after creation **or update**."
- AC2: "The summary API and downloadable report display `ownerGroup` for a record **regardless of how that record was populated**."
- AC3: "Existing catalog population behavior and stable IDs remain unchanged."

| Role | Path | Lifecycle path | Test coverage |
|---|---|---|---|
| Schema / persistence | `src/catalog/store.py` | Shared record schema and persistence helpers that every writer goes through | `tests/catalog/test_store.py` |
| Producer (primary) | `src/workflows/registration.py` | Initial onboarding / registration (creates the record) | `tests/workflows/test_registration.py` |
| Producer (scheduled/background) | `src/workflows/scheduled_sync.py` | Scheduled provider synchronization (creates or updates records) | `tests/workflows/test_scheduled_sync.py` |
| Producer (fallback/recovery) | `src/workflows/fallback_import.py` | Loads previously exported data when provider sync is unavailable | `tests/workflows/test_fallback_import.py` |
| Producer (on-demand/API) | `src/api/on_demand_refresh.py` | `POST /api/catalog/refresh`, an operator-requested refresh | `tests/api/test_on_demand_refresh.py` |
| Consumer | `src/api/catalog_summary.py` | Summary API | `tests/api/test_catalog_summary.py` |
| Consumer | `src/reports/catalog_export.py` | Downloadable report | `tests/reports/test_catalog_export.py` |

## Scope conflict (surfaced, not silently resolved)

The stakeholder sees TC-9007 as "mainly an onboarding change" and asked for a small plan. The repository evidence does not support covering only onboarding:

- Registration is only one of **four** writers to the shared record. Scheduled sync, fallback import, and on-demand refresh also create or replace records. If only `registration.py` changes, records from those three paths can lack `ownerGroup`, which fails AC1. Refreshes can also wipe a previously set `ownerGroup`, which fails AC1 and Requirement 3. The summary API and the report would then show nothing for those records, which fails AC2.
- **A plan that changes only `registration.py` must not be presented as meeting AC1 or AC2.**

**How this plan resolves it:** the stakeholder's instruction is a size preference ("prefer a single task if practical"). It does not exclude any named path. All four writers update one field on one shared schema, so covering every path still fits in **one implementation task**, sized for a single engineer. The plan therefore keeps the stakeholder's single-task preference and still covers every writer the acceptance criteria require.

**Confirmation requested from the stakeholder:** if you meant to exclude `src/workflows/scheduled_sync.py`, `src/workflows/fallback_import.py`, and/or `src/api/on_demand_refresh.py`, say so before task creation. If you do:
- those files and their tests (`tests/workflows/test_scheduled_sync.py`, `tests/workflows/test_fallback_import.py`, `tests/api/test_on_demand_refresh.py`) will be removed from Task 1;
- AC1 and AC2 will be recorded here as **unresolved** for records populated by the excluded paths. They will not be reported as satisfied.

## Open question (default value for non-onboarding paths)

Scheduled sync, fallback import, and on-demand refresh can create a record that never went through onboarding. They may also import legacy exports that predate `ownerGroup`. In those cases there may be no source for an owner group. The Feature does not say what value to use.

- **Assumption used in Task 1:** a single named default constant, `UNASSIGNED_OWNER_GROUP = "unassigned"`, defined in `src/catalog/store.py`. It is applied only when a record is **created** without a supplied value and no existing value is present. Updates never replace an existing `ownerGroup` with this default.
- Please confirm the default value, or name a provider field to read the owner group from.

## Impact map

```
catalog-service:
  changes:
    - Add an ownerGroup field to the shared Service Catalog record schema, with preserve-on-update semantics (keep the existing value unless a new non-empty value is supplied) and a single documented default for newly created records without a supplied value
    - Collect ownerGroup during initial registration and persist it on the created record
    - Apply the ownerGroup contract on scheduled sync writes (new records get a value; updates preserve the existing value)
    - Apply the ownerGroup contract on fallback import (imported records, including legacy exports without ownerGroup, end with a value; re-imports preserve existing values)
    - Apply the ownerGroup contract on on-demand refresh (POST /api/catalog/refresh preserves the existing value unless a new one is supplied)
    - Expose ownerGroup in the catalog summary API response
    - Include ownerGroup in the downloadable catalog report
    - Add tests per writer path (value present after create/update, preservation, stable IDs unchanged) and per consumer (ownerGroup shown for records from every population path)
    - Document that catalog records may be populated via registration, scheduled sync, fallback import, or on-demand refresh, and that all paths share the ownerGroup contract
```

## Excluded requirements

None. Every Feature requirement and acceptance criterion maps to Task 1 (implementation) or Task 2 (documentation).

## Workflow mode decision (Step 4.5)

- **Mode: `direct-to-main`**
- Rationale: no atomicity indicators.
  - Coordinated schema migrations: no. The schema change and all writers and readers are in the same task, so one PR.
  - Breaking API changes: no. `ownerGroup` is an additive response field. The refresh request gains only an optional field.
  - Cross-cutting refactor split across tasks: no. The cross-cutting propagation stays inside Task 1.
  - Tightly coupled components split across tasks: no. Task 2 (docs) has no effect on `main` until it merges.
- Every task targets `main`. No bookend tasks are needed.

## Planned issues

| # | Issue | Type | Epic | Depends on |
|---|---|---|---|---|
| E1 | TC-9007: Service Catalog ownerGroup | Epic | — | — |
| 1 | Add ownerGroup to the shared Service Catalog record across all population paths and consumers | Task | E1 | — |
| 2 | Document Service Catalog population paths and the ownerGroup contract | Task | E1 | Task 1 |

A documentation task is required because the Feature's Documentation Considerations section declares doc impact "Updates" (constraint 1.83). That makes two tasks. Task 1 is the only implementation task, which honors the single-task preference.

---
This comment was AI-generated by [sdlc-workflow/plan-feature](https://github.com/RHEcosystemAppEng/sdlc-plugins) v0.14.0.
