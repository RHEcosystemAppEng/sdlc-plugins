# Repository Impact Map — TC-9007: Add an owner group to Service Catalog records

**Status: PENDING SCOPE CLARIFICATION.** The stakeholder scope instruction (onboarding and display only) conflicts with two Feature acceptance criteria that apply to the shared Service Catalog record. Those criteria stay **unresolved** until the stakeholder confirms or widens scope (see "Scope conflict" below).

## Shared-artifact lifecycle (Step 3 analysis)

Shared artifact: **Service Catalog record** (schema and persistence in `src/catalog/store.py`, tests in `tests/catalog/test_store.py`).

| Role | Path | Test path | Planning status |
|---|---|---|---|
| Schema / persistence | `src/catalog/store.py` | `tests/catalog/test_store.py` | In scope (Task 1) |
| Writer — initial registration (primary) | `src/workflows/registration.py` | `tests/workflows/test_registration.py` | In scope (Task 2) |
| Writer — scheduled synchronization | `src/workflows/scheduled_sync.py` | `tests/workflows/test_scheduled_sync.py` | **UNRESOLVED — excluded by stakeholder** |
| Writer — fallback/recovery import | `src/workflows/fallback_import.py` | `tests/workflows/test_fallback_import.py` | **UNRESOLVED — excluded by stakeholder** |
| Writer — on-demand refresh (`POST /api/catalog/refresh`) | `src/api/on_demand_refresh.py` | `tests/api/test_on_demand_refresh.py` | **UNRESOLVED — excluded by stakeholder** |
| Consumer — summary API | `src/api/catalog_summary.py` | `tests/api/test_catalog_summary.py` | In scope (Task 3) |
| Consumer — downloadable report | `src/reports/catalog_export.py` | `tests/reports/test_catalog_export.py` | In scope (Task 3) |

## catalog-service

changes:
- Add `ownerGroup` to the shared Service Catalog record schema and persistence helpers
- Make store update semantics preserve an existing `ownerGroup` when an update omits it, and replace it when a new value is supplied; keep stable IDs and existing population behavior unchanged
- Collect `ownerGroup` during initial registration and persist it on the created record
- Expose `ownerGroup` in the catalog summary API response
- Include `ownerGroup` in the downloadable catalog report
- Document `ownerGroup` and the Service Catalog record contract (scope of the population-path statement depends on the clarification below)

## Scope conflict — UNRESOLVED (clarification requested)

The stakeholder instructed that this is strictly an onboarding-and-display change and that files and tests for scheduled synchronization, fallback import, and on-demand refresh stay out of scope. The repository evidence shows those three paths write the **same** shared Service Catalog record. Two Feature acceptance criteria therefore **cannot be confirmed as covered** by the planned tasks:

| Acceptance criterion | Why it is not covered under the current scope |
|---|---|
| "Every Service Catalog record has an `ownerGroup` value after creation or update." | Records created or updated by scheduled sync, fallback import, or on-demand refresh are not planned. The store-level preserve-on-omit rule (Task 1) keeps an existing value when one of those writers updates a record. It does **not** give a value to records that those writers create first (for example, fallback import loading services that never went through registration), and it does not cover records that exist before this change. |
| "The summary API and downloadable report display `ownerGroup` for a record regardless of how that record was populated." | Task 3 makes the consumers display `ownerGroup` from the stored record. Nothing in scope checks that records written by the three excluded writers actually carry the field, so the "regardless of how populated" part cannot be verified end to end. |

The third criterion, "Existing catalog population behavior and stable IDs remain unchanged", is covered at the store level (Task 1 tests). There is no regression coverage for it in the excluded writer suites.

Excluded paths and the coverage gap for each:

- `src/workflows/scheduled_sync.py` / `tests/workflows/test_scheduled_sync.py`: no check that a scheduled sync keeps an existing `ownerGroup` or applies a supplied replacement. No check that records first created by sync get a value.
- `src/workflows/fallback_import.py` / `tests/workflows/test_fallback_import.py`: no check that imported (previously exported) data carries or keeps `ownerGroup`. Records created only by an import may have no value.
- `src/api/on_demand_refresh.py` / `tests/api/test_on_demand_refresh.py`: no check that `POST /api/catalog/refresh` keeps or replaces `ownerGroup`. No check of whether the refresh request contract should accept the field.

**Question for the stakeholder:** Do you want to (a) widen scope so that these three writers and their tests are planned as additional tasks, which lets the two universal criteria be met, or (b) keep the current scope and formally narrow or defer the two acceptance criteria (for example, "records created through registration have `ownerGroup`") with a follow-up Feature for the alternate writers? Until you answer, the plan below covers only the in-scope paths and does **not** claim the universal criteria are satisfied.

## Excluded requirements

- **Updates keep the current owner group unless a new value is supplied (scheduled sync, fallback import, on-demand refresh paths).** Missing input: stakeholder approval to include these writer paths. Store-level semantics are planned (Task 1). Writer-level checks are not.
- **`ownerGroup` on every record regardless of population path.** Missing input: scope decision above. A backfill strategy for records that exist before this change is also unspecified in the Feature.

## Workflow mode

**direct-to-main.** No atomicity indicators were found:
- No coordinated schema migration across tasks. The new field is additive in `src/catalog/store.py`, and Task 1 lands first with a default that keeps existing records valid.
- No breaking API change. The summary API and report gain an additive field.
- No cross-cutting refactor.
- The tasks are not tightly coupled. Each task can merge on its own after Task 1 without breaking `main`.
