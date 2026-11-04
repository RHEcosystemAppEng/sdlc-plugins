# Repository Impact Map — TC-9007: Add an owner group to Service Catalog records

> **Status: SCOPE CONFLICT — CLARIFICATION REQUIRED BEFORE TASKS ARE FINALIZED.**
> Some Feature acceptance criteria apply to the shared Service Catalog record no matter which workflow fills it in. The stakeholder's scope instruction excludes three of the workflows that fill it in. Those criteria are marked **UNRESOLVED** below. The proposed tasks do **not** satisfy them in full.

```
catalog-service:
  changes:
    - Add an `ownerGroup` field to the shared Service Catalog record schema and persistence helpers, and keep the current `ownerGroup` on update unless a new value is supplied (src/catalog/store.py, tests/catalog/test_store.py)
    - Collect `ownerGroup` during initial registration and store it on the new catalog record (src/workflows/registration.py, tests/workflows/test_registration.py)
    - Show `ownerGroup` in the catalog summary API response (src/api/catalog_summary.py, tests/api/test_catalog_summary.py)
    - Show `ownerGroup` in the downloadable catalog report (src/reports/catalog_export.py, tests/reports/test_catalog_export.py)
    - Document the `ownerGroup` field for operators and API consumers (Documentation Considerations: Updates)
```

## Shared-artifact producer / consumer analysis

**Shared artifact:** the Service Catalog record (schema and persistence in `src/catalog/store.py`).

### Producers (workflows that create, update, replace, import or refresh the record)

| Producer | Source path | Test path | Kind | Scope status |
|---|---|---|---|---|
| Initial registration | `src/workflows/registration.py` | `tests/workflows/test_registration.py` | Primary (creates) | In scope, covered by Task 2 |
| Scheduled synchronization | `src/workflows/scheduled_sync.py` | `tests/workflows/test_scheduled_sync.py` | Scheduled/background (updates) | **EXCLUDED by stakeholder, UNRESOLVED** |
| Fallback import | `src/workflows/fallback_import.py` | `tests/workflows/test_fallback_import.py` | Fallback/recovery (loads/restores) | **EXCLUDED by stakeholder, UNRESOLVED** |
| On-demand refresh (`POST /api/catalog/refresh`) | `src/api/on_demand_refresh.py` | `tests/api/test_on_demand_refresh.py` | On-demand/manual/API (refreshes) | **EXCLUDED by stakeholder, UNRESOLVED** |

### Shared schema / persistence

| Component | Source path | Test path | Scope status |
|---|---|---|---|
| Catalog record schema + persistence helpers | `src/catalog/store.py` | `tests/catalog/test_store.py` | In scope, covered by Task 1 |

### Consumers (read or present the record)

| Consumer | Source path | Test path | Scope status |
|---|---|---|---|
| Catalog summary API | `src/api/catalog_summary.py` | `tests/api/test_catalog_summary.py` | In scope, covered by Task 3 |
| Downloadable catalog report | `src/reports/catalog_export.py` | `tests/reports/test_catalog_export.py` | In scope, covered by Task 4 |

## Acceptance-criteria coverage

| Feature acceptance criterion | Coverage with current (stakeholder-limited) scope | Status |
|---|---|---|
| Every Service Catalog record has an `ownerGroup` value after creation or update. | Creation through registration is covered (Tasks 1, 2). Updates through scheduled sync, fallback import and on-demand refresh are **not** covered. Those writers may create, replace or restore records without `ownerGroup`, or may overwrite it with an empty value. The store-level preserve-on-update rule (Task 1) only protects writers that call the store's update helper with a partial update. Nobody has confirmed that the three excluded writers do this, and their tests are not in scope. | **UNRESOLVED (partial)** |
| The summary API and downloadable report display `ownerGroup` for a record regardless of how that record was populated. | The display code is covered (Tasks 3, 4). But "regardless of how that record was populated" needs every writer to populate or preserve `ownerGroup`, and needs tests for records written by each path. Records from sync, fallback import or refresh are not checked. | **UNRESOLVED (partial)** |
| Existing catalog population behavior and stable IDs remain unchanged. | Registration and store behavior are covered by regression tests (Tasks 1, 2). The behavior and stable IDs of scheduled sync, fallback import and on-demand refresh are not checked by any planned test. | **UNRESOLVED (partial)** |
| Requirement: updates keep the current owner group unless a new value is supplied ("the record may be refreshed after onboarding"). | The store helper rule and its tests are covered (Task 1). The refresh/update paths that trigger it (`scheduled_sync.py`, `fallback_import.py`, `on_demand_refresh.py`) are excluded, so the requirement is unverified end to end. | **UNRESOLVED (partial)** |
| Requirement: registered record includes `ownerGroup` (onboarding). | Tasks 1, 2 | Covered |
| Requirement: summary API and report show `ownerGroup`. | Tasks 3, 4 | Covered (display layer) |
| Requirement: focused tests for onboarding and display. | Tasks 1–4 | Covered |

### Unresolved impact-map paths (excluded by stakeholder instruction, not in any task)

These paths are needed to fully meet the acceptance criteria above. Following the stakeholder instruction, they are **not** in any task's Files to Modify, Files to Create or Test Requirements:

- `src/workflows/scheduled_sync.py`: must set or keep `ownerGroup` when it synchronizes provider metadata into existing records. It must not wipe the value or replace the whole record.
- `tests/workflows/test_scheduled_sync.py`: needs a test that `ownerGroup` survives a scheduled sync and that stable IDs do not change.
- `src/workflows/fallback_import.py`: must give `ownerGroup` a value (from exported data or kept from the existing record) when it loads previously exported data. Older exports may not have the field.
- `tests/workflows/test_fallback_import.py`: needs a test that imported records have `ownerGroup` and that stable IDs do not change.
- `src/api/on_demand_refresh.py`: must keep `ownerGroup` on `POST /api/catalog/refresh` unless a new value is supplied.
- `tests/api/test_on_demand_refresh.py`: needs a test that refresh keeps `ownerGroup` and stable IDs.

### Clarification requested

The stakeholder asked for an onboarding-and-display-only change. That conflicts with acceptance criteria that cover every record, after any creation or update, "regardless of how that record was populated". Please choose one:

1. **Expand scope.** Add the three excluded writers and their tests (one task per writer, each depending on Task 1). Then the acceptance criteria can be marked fully covered.
2. **Narrow the acceptance criteria.** Amend TC-9007 so the criteria cover only records created through registration. Track the other writers in a follow-up Feature.
3. **Proceed as planned and accept the gap.** Tasks 1–5 go ahead. The criteria above stay explicitly **UNRESOLVED** on TC-9007 and must not be reported as satisfied.

Until a choice is made, the task set below covers the onboarding and display paths only. **It is not presented as satisfying the shared-artifact acceptance criteria.**

## Excluded requirements

- None excluded for missing inputs. Every requirement has a target repository and enough detail to plan. The partial coverage above comes from the stakeholder scope instruction, not from missing inputs.

## Documentation signals

- Doc impact: **Updates**. The Feature asks for docs saying records "may be populated through registration, scheduled synchronization, fallback import, or on-demand refresh" and that "all paths use the same catalog contract". The claim that every path uses the same contract (including `ownerGroup`) only holds once the scope conflict is resolved. The documentation task (Task 5) is limited to what this plan delivers and flags that claim as pending.

## Workflow mode decision

- **Mode: `direct-to-main`**
- Rationale: none of the atomicity indicators apply.
  - Coordinated schema migration: no. `ownerGroup` is an additive field with a defined default and handling for missing values in `src/catalog/store.py` (Task 1). Task 1 can merge alone without breaking `main`.
  - Breaking API change: no. The summary API and report only gain a field. Existing fields are unchanged.
  - Cross-cutting refactor: no.
  - Tightly coupled components: no. Tasks 2–4 depend on Task 1 (ordering only), but `main` stays working after each merge.
- Target Branch for all tasks: `main`. No bookend tasks.

## Proposed tasks

| # | Task | Depends on |
|---|---|---|
| 1 | Add `ownerGroup` to the shared Service Catalog record schema with preserve-on-update semantics | — |
| 2 | Collect `ownerGroup` during initial service registration | Task 1 |
| 3 | Show `ownerGroup` in the catalog summary API | Task 1 |
| 4 | Show `ownerGroup` in the downloadable catalog report | Task 1 |
| 5 | Document the Service Catalog `ownerGroup` field | Tasks 1–4 |

Epic grouping (Hierarchy Configuration: `by-sub-feature`, if the project has a level-1 type). Suggested groups for approval: "TC-9007: Owner group capture" (Tasks 1, 2), "TC-9007: Owner group display" (Tasks 3, 4), "TC-9007: Documentation" (Task 5).
