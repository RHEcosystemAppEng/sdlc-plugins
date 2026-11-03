# Repository Impact Map — TC-9007: Add an owner group to Service Catalog records

> **Status: SCOPE CONFLICT — clarification required before the task set can be treated as satisfying all acceptance criteria.**

## Analysis context

- Single repository: `catalog-service` (structure taken from the Feature description; no Serena instance is configured, so the paths below are the ones the Feature provides).
- No CONVENTIONS.md, no `docs/testing-readiness.md`, no Figma design are available for this repository, so the plan includes no convention enrichment, no testing tasks, and no Figma-derived notes.
- Stakeholder scope instruction: "strictly an onboarding-and-display change — do not include files or tests for scheduled synchronization, fallback import, or on-demand refresh."

## Shared-artifact producer / consumer trace

The shared artifact is the **Service Catalog record** (schema + persistence in `src/catalog/store.py`). Two Feature acceptance criteria apply to the artifact across *all* population paths:

- AC1: "Every Service Catalog record has an `ownerGroup` value after creation **or update**."
- AC2: "The summary API and downloadable report display `ownerGroup` for a record **regardless of how that record was populated**."
- AC3: "Existing catalog population behavior and stable IDs remain unchanged." (applies to every writer)

| Role | Path | Source | Tests | Scope status |
|---|---|---|---|---|
| Schema / persistence (shared) | Shared catalog record schema + persistence helpers | `src/catalog/store.py` | `tests/catalog/test_store.py` | In scope |
| Producer — primary (onboarding) | Initial registration | `src/workflows/registration.py` | `tests/workflows/test_registration.py` | In scope |
| Producer — scheduled/background | Scheduled provider sync | `src/workflows/scheduled_sync.py` | `tests/workflows/test_scheduled_sync.py` | **EXCLUDED by stakeholder — UNRESOLVED** |
| Producer — fallback/recovery | Fallback import of previously exported data | `src/workflows/fallback_import.py` | `tests/workflows/test_fallback_import.py` | **EXCLUDED by stakeholder — UNRESOLVED** |
| Producer — on-demand/API | `POST /api/catalog/refresh` | `src/api/on_demand_refresh.py` | `tests/api/test_on_demand_refresh.py` | **EXCLUDED by stakeholder — UNRESOLVED** |
| Consumer | Summary API | `src/api/catalog_summary.py` | `tests/api/test_catalog_summary.py` | In scope |
| Consumer | Downloadable report | `src/reports/catalog_export.py` | `tests/reports/test_catalog_export.py` | In scope |

## Impact map

```
catalog-service:
  changes:
    - Add `ownerGroup` to the shared Service Catalog record schema and persistence helpers (src/catalog/store.py)
    - Make the store update helper keep the existing `ownerGroup` when an update does not supply a new value, without changing record IDs
    - Collect `ownerGroup` during initial registration and persist it on the new record (src/workflows/registration.py)
    - Expose `ownerGroup` in the catalog summary API response (src/api/catalog_summary.py)
    - Add an `ownerGroup` column/field to the downloadable catalog report (src/reports/catalog_export.py)
    - Add focused tests for store, registration, summary API, and report (tests/catalog/test_store.py, tests/workflows/test_registration.py, tests/api/test_catalog_summary.py, tests/reports/test_catalog_export.py)
    - Update documentation for the `ownerGroup` catalog contract (documentation task)
```

## Unresolved scope conflict (blocks claiming AC1 / AC2 / AC3 coverage)

The stakeholder exclusion removes three producers that write the same shared Service Catalog record. With those paths excluded, the task set **does not** satisfy the shared-artifact criteria. Only the primary writer (registration) and the store-level helper are covered.

| Excluded path | Source | Tests | Coverage gap |
|---|---|---|---|
| Scheduled synchronization | `src/workflows/scheduled_sync.py` | `tests/workflows/test_scheduled_sync.py` | Records created or refreshed by the scheduled sync may have no `ownerGroup` (AC1), or a sync may overwrite and lose the existing `ownerGroup` (Requirement 3 / AC1). The summary/report cannot show a value that was never written (AC2). Nothing tests that sync behavior and IDs stay unchanged (AC3). |
| Fallback import | `src/workflows/fallback_import.py` | `tests/workflows/test_fallback_import.py` | Previously exported data has no `ownerGroup`, so imported or restored records may lack the value or wipe the current one (AC1, AC2). Nothing tests that import behavior and IDs are preserved (AC3). |
| On-demand refresh | `src/api/on_demand_refresh.py` (`POST /api/catalog/refresh`) | `tests/api/test_on_demand_refresh.py` | An operator refresh is a record update. If it replaces the record instead of merging, `ownerGroup` is lost (Requirement 3, AC1, AC2). Nothing tests this (AC3). |

The store-level preserve-on-update helper (Task 1) only protects these paths if each one updates through that helper rather than writing the full record directly. That has not been verified, and the scope instruction forbids verifying or testing it in this plan.

**Clarification requested from the stakeholder / Feature owner (choose one):**

1. **Expand scope.** Add tasks covering `scheduled_sync.py`, `fallback_import.py`, and `on_demand_refresh.py` plus their tests, so AC1–AC3 hold across all population paths.
2. **Narrow the acceptance criteria.** Reword AC1/AC2 to apply only to records created or updated through registration, and record the other paths as a follow-up Feature.
3. **Accept the gap explicitly.** Keep the current task set and record that AC1/AC2/AC3 stay unverified for scheduled sync, fallback import, and on-demand refresh.

Until a choice is made, these three paths appear **only in this impact map**. They are not in any task's Files to Modify, Files to Create, or Test Requirements.

## Excluded requirements

- **Requirement 3 ("Updates to a service record preserve the current owner group unless a new value is supplied"): only partly plannable.** The store-level preserve semantics are planned (Task 1). The real update paths (scheduled sync, fallback import, on-demand refresh) are excluded by the stakeholder instruction, so end-to-end coverage of this requirement is pending the clarification above.
- **Documentation "Doc Impact: Updates" asks for docs that cover all four population paths.** The documentation task covers the `ownerGroup` contract for registration and the display surfaces. Documenting scheduled sync, fallback import, and on-demand refresh behavior waits on the same clarification.

## Workflow mode

**direct-to-main.** No atomicity indicators were found:
- No coordinated migration. `ownerGroup` is added to the record schema in Task 1, and the later tasks depend on it, but merging Task 1 alone leaves `main` working.
- No breaking API change. The summary API gains an additive field.
- No cross-cutting refactor, and no frontend/backend pair.

Dependencies are expressed as ordinary task dependencies.

## Hierarchy

Project issue types could not be discovered (no Jira access in this eval run). If a level-1 Epic type exists, the configured strategy is `by-sub-feature`, with these suggested groups:
- "TC-9007: Owner group capture" — Tasks 1, 2
- "TC-9007: Owner group display" — Tasks 3, 4, 5

Otherwise tasks are created directly under the Feature.

## Proposed tasks (pending scope clarification)

| # | Task | Depends on |
|---|---|---|
| 1 | Add `ownerGroup` to the Service Catalog record schema and persistence helpers | — |
| 2 | Collect `ownerGroup` during service registration | 1 |
| 3 | Show `ownerGroup` in the catalog summary API | 1 |
| 4 | Show `ownerGroup` in the downloadable catalog report | 1 |
| 5 | Document the `ownerGroup` Service Catalog field | 1–4 |

---
This comment was AI-generated by [sdlc-workflow/plan-feature](https://github.com/RHEcosystemAppEng/sdlc-plugins) v0.13.10.
