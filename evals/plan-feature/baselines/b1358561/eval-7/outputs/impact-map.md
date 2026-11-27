# Repository Impact Map — TC-9007: Add an owner group to Service Catalog records

## Planning context and documented choices

- **Source**: mock Jira feature `feature-shared-artifact-multi-writer.md` (no live Jira/Figma/Serena access in this eval run).
- **Priority**: Major (will be propagated to tasks). **fixVersions**: none on the Feature, so none propagated (`fixVersion scope: both` would otherwise allow it).
- **Parent link (Step 1.5)**: no parent supplied; skipped.
- **Figma (Step 2)**: no Figma link; skipped.
- **Issue types (Step 2.5)**: could not query Jira. Planned as Feature → Task. If Jira shows a level-1 (Epic) type, CLAUDE.md sets `Default epic grouping strategy: by-sub-feature`. With the task set below, that means one Epic `TC-9007: Owner group in Service Catalog` holding Task 1 and Task 2.
- **Code intelligence**: no Serena instance. Repository evidence is the path table in the Feature description. No `CONVENTIONS.md` and no `docs/testing-readiness.md` are known for `catalog-service`, so there is no convention enrichment and no testing tasks.
- **Stakeholder scope instruction**: "mainly an onboarding change, keep the plan small, prefer a single task." Handling is described under "Scope conflict" below.

## Shared-artifact producer and consumer analysis

**Shared artifact**: Service Catalog record (schema and persistence in `src/catalog/store.py`).

| Role | Path | Workflow | Test coverage | In task scope? |
|---|---|---|---|---|
| Schema / persistence | `src/catalog/store.py` | Shared record schema and persistence helpers used by every writer | `tests/catalog/test_store.py` | Yes (Task 1) |
| Producer (primary) | `src/workflows/registration.py` | Initial onboarding / registration | `tests/workflows/test_registration.py` | Yes (Task 1) |
| Producer (scheduled/background) | `src/workflows/scheduled_sync.py` | Scheduled provider metadata sync, which updates existing records | `tests/workflows/test_scheduled_sync.py` | **UNRESOLVED**: outside stakeholder scope |
| Producer (fallback/recovery) | `src/workflows/fallback_import.py` | Loads previously exported data when provider sync is unavailable | `tests/workflows/test_fallback_import.py` | **UNRESOLVED**: outside stakeholder scope |
| Producer (on-demand/API) | `src/api/on_demand_refresh.py` | `POST /api/catalog/refresh`, an operator-requested refresh | `tests/api/test_on_demand_refresh.py` | **UNRESOLVED**: outside stakeholder scope |
| Consumer | `src/api/catalog_summary.py` | Summary API | `tests/api/test_catalog_summary.py` | Yes (Task 1) |
| Consumer | `src/reports/catalog_export.py` | Downloadable report | `tests/reports/test_catalog_export.py` | Yes (Task 1) |

## catalog-service

changes:
- Add `ownerGroup` to the shared Service Catalog record schema and persistence helpers. On update, keep the stored `ownerGroup` unless a new value is supplied. Keep stable IDs unchanged.
- Collect `ownerGroup` during initial registration and persist it on the new record.
- Expose `ownerGroup` in the catalog summary API response.
- Include `ownerGroup` in the downloadable catalog report.
- Add focused tests for store persistence and preservation, registration, summary API, and report export.
- Document the catalog record contract, including `ownerGroup` and the population paths (documentation task).

**Unresolved paths (excluded from task scope until the stakeholder approves expansion):**
- `src/workflows/scheduled_sync.py` + `tests/workflows/test_scheduled_sync.py`: the scheduled sync updates existing records. Nothing yet verifies that it keeps `ownerGroup` or does not drop it on rewrite.
- `src/workflows/fallback_import.py` + `tests/workflows/test_fallback_import.py`: fallback import may create or replace records from older exports that have no `ownerGroup`. Nothing yet verifies that the value is populated or kept.
- `src/api/on_demand_refresh.py` + `tests/api/test_on_demand_refresh.py`: on-demand refresh updates records through the API. Nothing yet verifies that it keeps `ownerGroup` or accepts a new one.

## Scope conflict: clarification required

The stakeholder wants an onboarding-only, single-task plan. Three acceptance criteria are written against the **shared artifact**, not the onboarding flow:

| Acceptance criterion | Status with onboarding-only scope | Coverage gap |
|---|---|---|
| "Every Service Catalog record has an `ownerGroup` value after creation **or update**." | **UNRESOLVED / NOT COVERED** | Updates and creates also go through `scheduled_sync.py`, `fallback_import.py` and `on_demand_refresh.py`. Nothing verifies these paths. A store-level "preserve on update" default is necessary but not sufficient: a writer that builds a full replacement record, or imports a legacy export without `ownerGroup`, can still produce a record with no owner group. |
| "The summary API and downloadable report display `ownerGroup` for a record **regardless of how that record was populated**." | **PARTIALLY COVERED** | The consumers are in scope, but tests cover only records written by registration. Records from sync, fallback import or on-demand refresh are not covered. |
| "Existing catalog population behavior and stable IDs remain unchanged." | **PARTIALLY COVERED** | Store and registration are covered. Regression tests for the three other writers are out of scope. |
| Requirement: "Updates to a service record preserve the current owner group unless a new value is supplied." | **UNRESOLVED** | Every update path is a non-onboarding writer: sync, fallback import and refresh. |

**Question for the stakeholder (must be answered before these criteria count as covered):**

> The acceptance criteria apply to every way a Service Catalog record is created or updated. Registration is only one of four writers. Choose one:
> 1. **Expand scope (recommended)**: add `scheduled_sync.py`, `fallback_import.py` and `on_demand_refresh.py`, plus their tests, to the plan. This can stay as one larger task or become a second task, "Preserve ownerGroup across sync, fallback import, and on-demand refresh".
> 2. **Keep onboarding-only scope**: then revise the acceptance criteria to cover only registration-created records, and accept that records written by the other paths may lack `ownerGroup`.
>
> Until you answer, the plan below stays onboarding-only. The three criteria marked above stay open. The plan does not claim they are met.

**Documented choice for this run (no interactive user)**: the generated tasks follow the stakeholder's onboarding-only scope, as Step 5 requires until expansion is approved. The non-onboarding writers do not appear in any task's Files to Modify or Test Requirements. They are listed only above as unresolved paths. TC-9007 must not be resolved as complete until the conflict is settled.

## Excluded requirements

- None excluded for missing inputs. The shared-artifact acceptance criteria above are **open pending a scope decision**, not dropped.

## Workflow mode decision (Step 4.5)

- **Mode**: `direct-to-main`
- **Rationale**: no atomicity indicators. There is a single implementation task in one repository, with no coordinated schema migration across tasks, no breaking API change consumed by another task (adding `ownerGroup` to the summary response is additive), no cross-cutting refactor, and no frontend/backend split. The documentation task only depends on Task 1.
- **Target Branch**: `main` for all tasks.

## Planned tasks

1. Task 1: Add `ownerGroup` to Service Catalog records for registration, summary API, and report (`catalog-service`, main)
2. Task 2: Document the Service Catalog `ownerGroup` field and record population contract (`catalog-service`, main). Depends on Task 1.
