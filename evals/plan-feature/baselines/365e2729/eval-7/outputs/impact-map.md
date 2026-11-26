# Repository Impact Map — TC-9007: Add an owner group to Service Catalog records

> Eval mode: this content would be posted as a Jira comment on TC-9007 (Step 4 + Step 4.5). Jira, Figma, and Serena were not contacted. Repository evidence comes from the "Repository Structure: catalog-service" table in the feature description. No Figma link was given, so Step 2 was skipped.

## Shared-artifact lifecycle analysis (Step 3)

**Shared artifact:** the Service Catalog record (`src/catalog/store.py`: schema and persistence helpers).

Two acceptance criteria apply to the shared artifact, not only to onboarding:
- AC1: "Every Service Catalog record has an `ownerGroup` value after creation **or update**."
- AC2: "The summary API and downloadable report display `ownerGroup` for a record **regardless of how that record was populated**."
- AC3: "Existing catalog population behavior and stable IDs remain unchanged."

### Producers / writers (every path that populates the catalog)

| # | Path | Kind | Source | Tests | Needed for |
|---|---|---|---|---|---|
| W1 | Initial registration (onboarding) | Primary create | `src/workflows/registration.py` | `tests/workflows/test_registration.py` | AC1, AC3 |
| W2 | Scheduled provider sync | Scheduled/background update | `src/workflows/scheduled_sync.py` | `tests/workflows/test_scheduled_sync.py` | AC1 (update preserves value), AC2, AC3 |
| W3 | Fallback import of previously exported data | Fallback/recovery | `src/workflows/fallback_import.py` | `tests/workflows/test_fallback_import.py` | AC1, AC2, AC3 |
| W4 | `POST /api/catalog/refresh` | On-demand/operator API | `src/api/on_demand_refresh.py` | `tests/api/test_on_demand_refresh.py` | AC1 (update preserves value), AC2, AC3 |
| S | Schema + persistence helpers shared by all writers | Shared contract | `src/catalog/store.py` | `tests/catalog/test_store.py` | AC1, AC3 |

### Consumers / readers

| # | Path | Source | Tests | Needed for |
|---|---|---|---|---|
| R1 | Catalog summary API | `src/api/catalog_summary.py` | `tests/api/test_catalog_summary.py` | AC2 |
| R2 | Downloadable report | `src/reports/catalog_export.py` | `tests/reports/test_catalog_export.py` | AC2 |

### Finding: scope conflict with the stakeholder framing

The stakeholder sees this as mainly an onboarding change. The repository says otherwise. Registration (W1) creates records. Scheduled sync (W2), fallback import (W3) and on-demand refresh (W4) also write to the same record. Any of them can overwrite or drop `ownerGroup` unless they are updated. Fallback import can also create records that registration never saw.

Changing only `registration.py` (plus the readers) **does not satisfy AC1 or AC2**:
- A refresh through W2 or W4 that rewrites the record without carrying `ownerGroup` would leave the record with no `ownerGroup`. That breaks AC1 ("after ... update") and Requirement 3 ("updates preserve the current owner group").
- A record restored or loaded through W3 would have no `ownerGroup` for R1 and R2 to show. That breaks AC2 ("regardless of how that record was populated").

The stakeholder emphasized the onboarding flow but did not exclude W2, W3 or W4. Per Step 3, that emphasis does not make the other writers irrelevant. This plan therefore **includes all four writers**. It also keeps the stakeholder's preference for a single implementation task: each writer change is small (carry or preserve one field through a shared store helper), so one task stays sized for one engineer.

**Clarification requested from the stakeholder before tasks are finalized:**
1. Confirm that the scope covers all four writers (W1–W4). This plan assumes yes, because AC1 and AC2 cannot be met otherwise.
2. If the stakeholder wants **onboarding only**, W2/W3/W4 and their tests (`src/workflows/scheduled_sync.py`, `src/workflows/fallback_import.py`, `src/api/on_demand_refresh.py`, `tests/workflows/test_scheduled_sync.py`, `tests/workflows/test_fallback_import.py`, `tests/api/test_on_demand_refresh.py`) will be removed from Task 1. AC1 (update half), AC2 (non-onboarding populations) and Requirement 3 will then be recorded as **UNRESOLVED / not covered**. They must not be reported as satisfied.
3. Decide what happens when a record is created through a non-onboarding path (for example a fallback import of legacy exported data) and no `ownerGroup` value is available. **Proposed default:** fail closed. The store rejects a write that would leave `ownerGroup` empty, and the writer reports or logs the record as an import error instead of silently saving a blank value. The alternative is a documented placeholder such as `"unassigned"`. Please confirm.

## Impact map

```
catalog-service:
  changes:
    - Add required `ownerGroup` field to the shared Service Catalog record schema and persistence helpers, with merge semantics that preserve the existing value when an update does not supply one (src/catalog/store.py)
    - Collect and persist `ownerGroup` during initial registration (src/workflows/registration.py)
    - Preserve existing `ownerGroup` (or apply a provider-supplied value) when scheduled sync updates a record (src/workflows/scheduled_sync.py)
    - Carry `ownerGroup` from exported data through fallback import, preserving the existing value when the export lacks it (src/workflows/fallback_import.py)
    - Accept optional `ownerGroup` on POST /api/catalog/refresh and preserve the existing value when it is omitted (src/api/on_demand_refresh.py)
    - Expose `ownerGroup` in the catalog summary API response (src/api/catalog_summary.py)
    - Include an `ownerGroup` column in the downloadable catalog report (src/reports/catalog_export.py)
    - Add or extend tests for the store, every writer path and both readers, including stable-ID and update-preservation checks (tests/catalog/test_store.py, tests/workflows/test_registration.py, tests/workflows/test_scheduled_sync.py, tests/workflows/test_fallback_import.py, tests/api/test_on_demand_refresh.py, tests/api/test_catalog_summary.py, tests/reports/test_catalog_export.py)
    - Document that catalog records can be populated through registration, scheduled sync, fallback import or on-demand refresh, and that all four share the `ownerGroup` contract (documentation task)
```

### Acceptance-criterion coverage trace

| Criterion | Covered by | Paths |
|---|---|---|
| AC1: `ownerGroup` present after creation or update | Task 1 | S, W1, W2, W3, W4 |
| AC2: summary API and report show `ownerGroup` regardless of population path | Task 1 | R1, R2, plus W1–W4 so every population path writes the field |
| AC3: existing population behavior and stable IDs unchanged | Task 1 (regression tests on every writer) | S, W1–W4 |
| Req 4: focused tests for onboarding and display | Task 1 | all test files above |
| Documentation Considerations (Updates) | Task 2 | docs (chosen by implementer) |

### Excluded requirements

None. Every requirement can be planned with the information available. Coverage of AC1 and AC2 depends on the stakeholder confirming that the scope includes all writers (see clarification 1). If that is declined, the paths in clarification 2 become unresolved.

## Workflow mode decision (Step 4.5)

**Mode: `direct-to-main`**

Rationale: no atomicity indicators were found.
- Coordinated schema migrations: the schema change and all writers and readers that depend on it are in the same task (Task 1), so no other task depends on a half-landed schema.
- Breaking API changes: `POST /api/catalog/refresh` only gains an optional field, and the summary response only gains an additive field. Neither is breaking.
- Cross-cutting refactors: none.
- Tightly coupled frontend/backend components: not applicable (single repository).

The documentation task (Task 2) depends on Task 1 but leaves `main` in a working state on its own. All tasks target `main`.

## Hierarchy note (Step 2.5)

Issue types could not be discovered (Jira was not contacted). CLAUDE.md sets `Default epic grouping strategy: by-sub-feature`. If the project has a level-1 Epic type, the proposed grouping is one Epic, "TC-9007: Service Catalog ownerGroup", containing Tasks 1 and 2. Otherwise tasks are created directly under the Feature.

---
This comment was AI-generated by [sdlc-workflow/plan-feature](https://github.com/RHEcosystemAppEng/sdlc-plugins) v0.14.0.
