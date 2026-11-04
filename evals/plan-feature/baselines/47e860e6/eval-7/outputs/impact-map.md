# Repository Impact Map — TC-9007: Add an owner group to Service Catalog records

**Status: scope conflict unresolved — awaiting stakeholder clarification before tasks are finalized.**

## Planning inputs

- Feature: TC-9007 (Priority: Major, Fix Versions: none, Labels: ai-generated-jira)
- Figma: none linked, so Step 2 was skipped
- Repository: `catalog-service` (structure from the Feature description). No Serena instance is configured, so analysis used the repository structure listed in the Feature.
- CONVENTIONS.md: not provided for `catalog-service`, so no conventions were applied
- Testing readiness template (`docs/testing-readiness.md`): not present, so no testing tasks were generated
- Documentation signals: **Updates**. Document that catalog records may be populated through registration, scheduled synchronization, fallback import, or on-demand refresh.
- Stakeholder guidance: "mainly an onboarding change, keep the plan small, prefer a single task if practical"

## Shared-artifact producer and consumer analysis

**Shared artifact:** the Service Catalog record (schema and persistence in `src/catalog/store.py`).

Acceptance criteria that depend on the shared artifact:

- AC1: "Every Service Catalog record has an `ownerGroup` value after creation **or update**."
- AC2: "The summary API and downloadable report display `ownerGroup` for a record **regardless of how that record was populated**."
- AC3: "Existing catalog population behavior and stable IDs remain unchanged."
- Requirement 3: "Updates to a service record preserve the current owner group unless a new value is supplied."

### Schema and persistence

| Path | Role | Test coverage |
|---|---|---|
| `src/catalog/store.py` | Shared record schema and persistence helpers. `ownerGroup` field and preserve-on-update semantics go here | `tests/catalog/test_store.py` |

### Producers and writers (every path that creates, updates, or populates the record)

| Path | Population path | Kind | Test coverage | In stakeholder's stated focus? |
|---|---|---|---|---|
| `src/workflows/registration.py` | Initial registration / onboarding (creates the record) | Primary | `tests/workflows/test_registration.py` | Yes |
| `src/workflows/scheduled_sync.py` | Scheduled provider metadata sync (updates/refreshes the record) | Scheduled/background | `tests/workflows/test_scheduled_sync.py` | **No** |
| `src/workflows/fallback_import.py` | Loads previously exported data when provider sync is unavailable (populates/replaces the record) | Fallback/recovery | `tests/workflows/test_fallback_import.py` | **No** |
| `src/api/on_demand_refresh.py` | `POST /api/catalog/refresh`, operator-requested refresh (updates the record) | On-demand/manual/API | `tests/api/test_on_demand_refresh.py` | **No** |

### Consumers (readers and presenters)

| Path | Consumer | Test coverage |
|---|---|---|
| `src/api/catalog_summary.py` | Catalog summary API | `tests/api/test_catalog_summary.py` |
| `src/reports/catalog_export.py` | Downloadable catalog report | `tests/reports/test_catalog_export.py` |

## Proposed changes

```
catalog-service:
  changes:
    # In scope (onboarding focus + shared schema + consumers): drafted as Task 1
    - Add an `ownerGroup` field to the shared Service Catalog record schema and persistence helpers (src/catalog/store.py), with preserve-on-update semantics when no new value is supplied
    - Collect and persist `ownerGroup` during initial registration (src/workflows/registration.py)
    - Expose `ownerGroup` in the catalog summary API response (src/api/catalog_summary.py)
    - Include `ownerGroup` in the downloadable catalog report (src/reports/catalog_export.py)
    - Add focused tests for store, registration, summary API, and export, including stable-ID and preserve-on-update checks at the persistence layer
    # Documentation: drafted as Task 2
    - Document `ownerGroup` and the catalog record population paths
    # UNRESOLVED: needed for AC1 / AC2 / Requirement 3, but outside the stated onboarding focus (see below)
    - Populate or preserve `ownerGroup` in scheduled synchronization (src/workflows/scheduled_sync.py)
    - Populate or preserve `ownerGroup` in fallback import (src/workflows/fallback_import.py)
    - Populate or preserve `ownerGroup` in on-demand refresh (src/api/on_demand_refresh.py)
```

## Unresolved scope conflict (clarification required)

The stakeholder asked to treat this as an onboarding change and keep it to a single task if practical. The repository evidence shows **four** workflows that populate the same Service Catalog record. AC1, AC2, and Requirement 3 apply to the shared record on every population path, not just to onboarding. A plan that changes only `registration.py` **does not satisfy** these criteria:

| Unresolved path | Why it is needed | Coverage gap if excluded |
|---|---|---|
| `src/workflows/scheduled_sync.py` | Updates records on a schedule. It must keep the existing `ownerGroup` unless the provider supplies a new one (Req 3, AC1). If it writes the whole record, it can drop `ownerGroup`, and the summary API and report would then show it empty (AC2). | No test in `tests/workflows/test_scheduled_sync.py` checks that `ownerGroup` survives a sync, or that IDs and population stay stable (AC3) |
| `src/workflows/fallback_import.py` | Populates records from previously exported data when provider sync is down. Older exports have no `ownerGroup`, so imported records may lack it, which breaks AC1 ("every record has an `ownerGroup` value"). It may also overwrite an existing value. | No test in `tests/workflows/test_fallback_import.py` covers importing data without `ownerGroup`, preserving an existing value, or round-tripping `ownerGroup` through export and import |
| `src/api/on_demand_refresh.py` | `POST /api/catalog/refresh` updates the record on operator request. It must keep `ownerGroup` unless a new value is supplied (Req 3). | No test in `tests/api/test_on_demand_refresh.py` checks that `ownerGroup` survives a refresh or that a supplied value replaces it |

Task 1 adds preserve-on-update semantics in the shared persistence helpers (`src/catalog/store.py`). This **does not** prove that the three alternate writers keep `ownerGroup`, because they may build and replace full records rather than merge through that helper. Each writer needs its own validation and tests before AC1, AC2, and Requirement 3 can be called covered.

There is also a related open question for AC1: what `ownerGroup` value should a record get when its population path has no source for it? Examples are a fallback import of a pre-feature export, or a sync that creates a record the registration flow never saw. The options are a required value, a defined sentinel such as `unassigned`, or rejecting the write. The stakeholder has not answered this, and it changes the behavior of the three alternate paths.

### Question for the stakeholder

> AC1, AC2, and Requirement 3 apply to every Service Catalog record. The catalog is also written by scheduled sync, fallback import, and on-demand refresh, not only by onboarding. How should we proceed?
>
> 1. **Recommended: expand scope while keeping a single task.** Extend Task 1 to also cover `scheduled_sync.py`, `fallback_import.py`, and `on_demand_refresh.py` and their tests. That is three more writer files and three more test files. It is still one engineer's worth of work, and it fully satisfies AC1, AC2, AC3, and Requirement 3. Please also confirm the default `ownerGroup` behavior for records that arrive without one.
> 2. **Keep onboarding-only scope.** Ship Task 1 as drafted, and either (a) narrow AC1, AC2, and Requirement 3 to "records created through registration", or (b) track the three alternate paths in a follow-up task. Until then, the Feature's universal criteria stay **not covered**.

Until the stakeholder approves expanding the scope, the three alternate paths are listed **only** here, as unresolved impact-map paths. They are deliberately left out of the Files to Modify and Test Requirements of the drafted tasks.

## Acceptance-criteria coverage status

| Criterion | Status with the drafted tasks |
|---|---|
| Req 1: registered record includes `ownerGroup` | Covered by Task 1 |
| Req 2 / AC2: summary API and report show `ownerGroup` | Display covered by Task 1. **"Regardless of how populated" is NOT covered** until the alternate writers are confirmed to populate and keep the field |
| Req 3: updates keep `ownerGroup` unless a new value is supplied | Persistence-layer semantics covered by Task 1. **The update paths (scheduled sync, fallback import, on-demand refresh) are NOT covered.** Unresolved |
| AC1: every record has `ownerGroup` after creation or update | Covered for creation through registration only. **Update and alternate-population paths are NOT covered.** Unresolved |
| AC3: existing population behavior and stable IDs unchanged | Covered for store and registration. **The alternate paths are NOT verified.** Unresolved |
| Req 4: focused tests for onboarding and display | Covered by Task 1 |

## Excluded requirements

None are excluded for missing inputs. All requirements can be planned. The paths above are **unresolved** because of a scope conflict, not because inputs are missing.

## Workflow mode decision (Step 4.5)

- **Mode: `direct-to-main`**
- Rationale: the drafted implementation is one task (Task 1) that holds the schema change, the registration writer, and both consumers. No change is split across tasks, so none of the four atomicity indicators applies: no coordinated schema migration across tasks, no API contract split between tasks, no cross-cutting refactor split across tasks, no tightly coupled frontend/backend pair. Task 2 (documentation) depends on Task 1 but does not break `main` if merged alone.
- Note: if Option 1 is approved, the extra writers go into the **same** Task 1, and the mode stays `direct-to-main`. If the alternate writers were split into separate tasks instead, re-run this evaluation. A store schema change that makes `ownerGroup` mandatory would then be a cross-task coordinated schema change.

## Hierarchy / Epic grouping

- CLAUDE.md Hierarchy Configuration: default grouping strategy `by-sub-feature`.
- Issue-type discovery (Step 2.5) could not run in this offline eval. If a level-1 Epic type exists, the suggested grouping for user approval is one Epic, "TC-9007: Service Catalog owner group", containing Task 1 and Task 2. There is only one sub-feature.
