# Repository Impact Map — TC-9007: Add an owner group to Service Catalog records

## Shared-artifact path map (Service Catalog record)

The `ownerGroup` acceptance criteria apply to a shared artifact — the Service Catalog record defined in `src/catalog/store.py`. Per repository evidence, the artifact has the following producers and consumers:

| Role | Path | Lifecycle | Test coverage | Scope status |
|---|---|---|---|---|
| Schema / persistence | `src/catalog/store.py` | Shared record schema and persistence helpers used by all writers | `tests/catalog/test_store.py` | In scope |
| Producer (primary) | `src/workflows/registration.py` | Creates the record during initial onboarding | `tests/workflows/test_registration.py` | In scope |
| Producer (scheduled/background) | `src/workflows/scheduled_sync.py` | Updates/repopulates records from the provider on a scheduled run | `tests/workflows/test_scheduled_sync.py` | **Excluded by stakeholder — UNRESOLVED** |
| Producer (fallback/recovery) | `src/workflows/fallback_import.py` | Populates records from previously exported data when provider sync is unavailable | `tests/workflows/test_fallback_import.py` | **Excluded by stakeholder — UNRESOLVED** |
| Producer (on-demand/API) | `src/api/on_demand_refresh.py` (`POST /api/catalog/refresh`) | Operator-requested refresh of a record | `tests/api/test_on_demand_refresh.py` | **Excluded by stakeholder — UNRESOLVED** |
| Consumer | `src/api/catalog_summary.py` | Reads records for the summary API | `tests/api/test_catalog_summary.py` | In scope |
| Consumer | `src/reports/catalog_export.py` | Reads records for the downloadable report | `tests/reports/test_catalog_export.py` | In scope |

## catalog-service

changes:
  - Add an `ownerGroup` field to the shared Service Catalog record schema and persistence helpers, with update semantics that preserve the existing `ownerGroup` unless a new value is supplied, and without changing stable record IDs
  - Collect `ownerGroup` during initial registration (onboarding) and persist it on the created record
  - Expose `ownerGroup` in the catalog summary API response
  - Include `ownerGroup` in the downloadable catalog report
  - Add focused tests for onboarding (store + registration) and display (summary API + report), including stable-ID and preserve-on-update behavior at the store level
  - Update documentation for the new `ownerGroup` field (scope of the "all population paths" doc content depends on resolution of the scope conflict below)

## Unresolved scope conflict — clarification required

The stakeholder instructed that this is strictly an onboarding-and-display change and that scheduled synchronization, fallback import, and on-demand refresh files and tests must be kept out of scope. That instruction is honored: none of those paths appear in any task's Files to Modify, Files to Create, or Test Requirements.

However, the following Feature acceptance criteria apply to the shared Service Catalog record across **all** population paths, and **cannot be claimed as satisfied by the registration (primary) writer alone**:

1. **"Every Service Catalog record has an `ownerGroup` value after creation or update."**
   - Records created or updated by scheduled sync, fallback import, or on-demand refresh are not guaranteed to carry or preserve `ownerGroup` under the current plan.
2. **"The summary API and downloadable report display `ownerGroup` for a record regardless of how that record was populated."**
   - Display is planned in both consumers, but a record populated (or overwritten) by an excluded writer may have no `ownerGroup` value to display.
3. **Requirement: "Updates to a service record preserve the current owner group unless a new value is supplied"** ("The record may be refreshed after onboarding").
   - Preserve semantics are planned in `src/catalog/store.py`, but whether each excluded writer routes through that helper (rather than replacing the record wholesale) is unverified and untested.
4. **"Existing catalog population behavior and stable IDs remain unchanged."**
   - Only verified for store and registration; no regression coverage for the other writers.

Exact excluded paths and coverage gaps:

| Excluded path | Gap | Missing test coverage |
|---|---|---|
| `src/workflows/scheduled_sync.py` | Scheduled sync may overwrite/omit `ownerGroup` on update | `tests/workflows/test_scheduled_sync.py` — no assertion that `ownerGroup` is preserved after a scheduled run, nor that stable IDs are unchanged |
| `src/workflows/fallback_import.py` | Imported records (from older exports without `ownerGroup`) may be created without a value or overwrite an existing one | `tests/workflows/test_fallback_import.py` — no assertion that imported records carry/preserve `ownerGroup` |
| `src/api/on_demand_refresh.py` (`POST /api/catalog/refresh`) | Operator refresh may drop `ownerGroup` | `tests/api/test_on_demand_refresh.py` — no assertion that `ownerGroup` survives a refresh |

**Question for the stakeholder / engineer:** Should the scope be expanded to include the three excluded writers (and their tests) so that the shared-artifact acceptance criteria can be fully satisfied? Alternatively, should the acceptance criteria be narrowed to "records created via registration" and "records updated via the shared store helper"? Until this is resolved, acceptance criteria 1–4 above remain **unresolved / partially covered**, and the planned task set must not be presented as satisfying them.

## Excluded requirements

- None excluded for missing inputs. Requirements 1–4 of the Feature are planned within the approved onboarding-and-display scope; the shared-artifact criteria above are flagged as **unresolved due to a stakeholder scope conflict**, not as excluded for missing input.

## Workflow mode

- **Mode:** `direct-to-main`
- **Rationale:** No atomicity indicators found. The `ownerGroup` field is additive (no breaking API contract change, no coordinated migration that must land atomically, no cross-cutting refactor). Task ordering via dependencies (store schema first, then registration and consumers) keeps `main` working after each merge; consumers render an empty/absent value safely if a record lacks `ownerGroup`.

---

This comment was AI-generated by [sdlc-workflow/plan-feature](https://github.com/RHEcosystemAppEng/sdlc-plugins) v0.13.10.
