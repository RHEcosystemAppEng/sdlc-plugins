# Repository Impact Map — TC-9007: Add an owner group to Service Catalog records

## Planning context and non-interactive decisions

| Step | Prompt / decision point | Choice made (non-interactive default) |
|---|---|---|
| 0 | Project Configuration validation | Passed (Repository Registry, Jira Configuration, Code Intelligence present). Note: `catalog-service` is not in the Registry and has no Serena instance; analysis used the repository structure supplied in the Feature description (synthetic eval input). |
| 1 | Priority / fixVersions | Priority `Major` (propagated to tasks). Fix Versions: none (omitted). |
| 1.5 | Link Feature to a parent issue? | Skipped (no parent key provided). |
| 2 | Figma | No Figma link — Step skipped. |
| 2.5 | Issue type discovery | Jira not reachable offline. Assumed TC has a level-1 "Epic" type; Hierarchy Configuration default `by-sub-feature` applied. If no level-1 type exists, tasks go directly under the Feature (graceful degradation). |
| 3 | CONVENTIONS.md / `docs/testing-readiness.md` | Not present in the supplied repository structure → no convention enrichment, no testing tasks. |
| 4 | Impact map approval | Auto-approved, **with the scope conflict below recorded as an open clarification**. |
| 5 | Epic grouping (by-sub-feature) | One sub-feature → one Epic: `TC-9007: Service Catalog ownerGroup`. |

## Shared-artifact producer / consumer analysis (Step 3)

**Shared artifact:** the Service Catalog record (schema + persistence in `src/catalog/store.py`).

The acceptance criteria are written against the shared artifact, not the onboarding flow:
- AC1: "Every Service Catalog record has an `ownerGroup` value after **creation or update**."
- AC2: "The summary API and downloadable report display `ownerGroup` for a record **regardless of how that record was populated**."
- AC3: "Existing catalog population behavior and stable IDs remain unchanged."

| Role | Path | Lifecycle path | Test coverage | Change needed? |
|---|---|---|---|---|
| Schema / persistence | `src/catalog/store.py` | All writers persist through it | `tests/catalog/test_store.py` | Yes — add `ownerGroup` field, preserve-on-update merge, reject empty persistence |
| Producer (primary) | `src/workflows/registration.py` | Initial onboarding / creation | `tests/workflows/test_registration.py` | Yes — collect and persist `ownerGroup` |
| Producer (scheduled / background) | `src/workflows/scheduled_sync.py` | Scheduled provider sync — updates records | `tests/workflows/test_scheduled_sync.py` | Yes — must not drop/overwrite `ownerGroup`; pass provider value if supplied |
| Producer (fallback / recovery) | `src/workflows/fallback_import.py` | Loads previously exported data when provider sync unavailable — creates/replaces records | `tests/workflows/test_fallback_import.py` | Yes — older exports lack `ownerGroup`; must preserve existing value / import it when present |
| Producer (on-demand / API) | `src/api/on_demand_refresh.py` (`POST /api/catalog/refresh`) | Operator-requested refresh — updates records | `tests/api/test_on_demand_refresh.py` | Yes — preserve current `ownerGroup` unless a new value is supplied |
| Consumer | `src/api/catalog_summary.py` | Summary API | `tests/api/test_catalog_summary.py` | Yes — expose `ownerGroup` |
| Consumer | `src/reports/catalog_export.py` | Downloadable report | `tests/reports/test_catalog_export.py` | Yes — include `ownerGroup` column |

## Scope conflict — clarification requested

The stakeholder framing ("mainly an onboarding change", "keep the plan small", "focus on the onboarding flow where records are first created") conflicts with AC1/AC2, which apply to the shared artifact across **all four** population paths. Repository evidence shows three non-onboarding writers that create or update the same record:

- `src/workflows/scheduled_sync.py` (+ `tests/workflows/test_scheduled_sync.py`)
- `src/workflows/fallback_import.py` (+ `tests/workflows/test_fallback_import.py`)
- `src/api/on_demand_refresh.py` (+ `tests/api/test_on_demand_refresh.py`)

An onboarding-only change (store + registration + consumers) would **not** satisfy AC1 or AC2: a record refreshed by sync/refresh, or loaded by fallback import, could lose or never receive `ownerGroup`, and the summary API/report would show it blank. The registration writer alone cannot be claimed to satisfy these criteria.

**Question for the stakeholder:** Do you approve including the scheduled-sync, fallback-import, and on-demand-refresh writers in scope so AC1/AC2 can be met? If not, AC1 and AC2 must be narrowed (e.g., "records created via registration") or remain open.

**Default chosen (non-interactive):** The stakeholder expressed a *preference* (small, single task if practical), not an explicit exclusion of these paths, and the Feature's own MVP requirement "Updates to a service record preserve the current owner group" can only be met by the update paths. All writers live in one repository and share one persistence helper, so a **single implementation task covering all writers is practical** and honors the "single task" preference while satisfying the ACs. If the stakeholder answers "onboarding only", Task 1 must be revised to remove the three non-onboarding writers and their tests, and AC1/AC2 must be marked **unresolved** on TC-9007 (not covered).

A second (documentation) task is generated because the Feature's Documentation Considerations section declares doc impact "Updates" (required by plan-feature Step 5 / constraint 1.83).

## Impact map

```
catalog-service:
  changes:
    - Add an ownerGroup field to the shared Service Catalog record schema and persistence helpers, preserving the existing value on update unless a new non-empty value is supplied, and refusing to persist a record that would end up without an ownerGroup
    - Collect ownerGroup during initial registration and persist it on the new record
    - Ensure scheduled provider synchronization updates preserve (or set, when the provider supplies one) ownerGroup without altering stable IDs or other sync behavior
    - Ensure fallback import of previously exported service data preserves existing ownerGroup values and imports ownerGroup when present in the export
    - Ensure POST /api/catalog/refresh preserves the current ownerGroup unless a new value is supplied
    - Expose ownerGroup in the catalog summary API response
    - Include ownerGroup in the downloadable catalog report
    - Add per-path tests for every writer and consumer above, plus stable-ID / existing-behavior regression tests
    - Update documentation to describe ownerGroup and the four population paths that share the catalog contract
```

## Excluded requirements

None excluded. (Conditional: if the stakeholder rejects the scope expansion above, AC1 and AC2 become unresolved for the scheduled-sync, fallback-import, and on-demand-refresh paths listed in the Scope conflict section.)

## Open question (not a scope exclusion)

- A record **first created** by a non-registration path (sync, fallback import, or refresh) with no `ownerGroup` in its source data has no existing value to keep. Default in Task 1: the store refuses to persist it (fails closed, raising an error the writer reports), so it never silently writes an empty `ownerGroup`. The alternative, a stakeholder-approved default owner group value, needs confirmation. A backfill of records that existed before this feature is not in scope. AC1 is met on their next create/update.

## Workflow mode (Step 4.5)

**Mode: `direct-to-main`.**
Rationale: none of the atomicity indicators apply. There is one implementation task in one repository. The schema change, writers, and consumers all ship in the same PR, so no other task depends on a partly merged state. The documentation task only adds docs and cannot break `main`. No bookend tasks are generated.

## Tasks

| # | Title | Epic | Depends on |
|---|---|---|---|
| 1 | Add ownerGroup to Service Catalog records across all population paths and displays | TC-9007: Service Catalog ownerGroup | — |
| 2 | Document ownerGroup and the shared catalog population paths | TC-9007: Service Catalog ownerGroup | Task 1 |
