# Repository Impact Map — TC-9007: Add an owner group to Service Catalog records

## Run notes (non-interactive defaults)

- Source: mock Jira feature `evals/plan-feature/files/feature-shared-artifact-multi-writer.md` (no live Jira/Figma access).
- Figma: no Figma URL present — Step 2 skipped.
- Step 1.5 (parent link): no parent supplied — skipped (default: press Enter).
- Priority: `Major` (propagated to tasks and Epics). Fix Versions: none (nothing propagated; `fixVersion scope: both` has no effect).
- Repository analysis: `catalog-service` is described only by the feature's repository-structure table; no Serena instance is configured, so paths come from that table. No `CONVENTIONS.md` or `docs/testing-readiness.md` is listed for `catalog-service` — no convention enrichment, no testing tasks generated.
- Issue types: could not query Jira. Assumed the TC project exposes a level-1 `Epic` type and a level-0 `Task` type (Feature type ID 10142 from CLAUDE.md). Epic grouping strategy: `by-sub-feature` (from CLAUDE.md Hierarchy Configuration); suggested groupings accepted by default.
- **Stakeholder scope instruction:** "strictly an onboarding-and-display change; do not include files or tests for scheduled synchronization, fallback import, or on-demand refresh." This was honored in the task set — see the **Unresolved scope conflict** section below.

## Shared-artifact producer/consumer analysis

Shared artifact: **Service Catalog record** (schema + persistence in `src/catalog/store.py`).

| Path | Role | Source | Tests | In planned tasks? |
|---|---|---|---|---|
| Schema / persistence helpers | Shared store | `src/catalog/store.py` | `tests/catalog/test_store.py` | Yes (Task 1) |
| Initial registration (onboarding) | Producer — create | `src/workflows/registration.py` | `tests/workflows/test_registration.py` | Yes (Task 2) |
| Scheduled synchronization | Producer — update/refresh | `src/workflows/scheduled_sync.py` | `tests/workflows/test_scheduled_sync.py` | **No — excluded by stakeholder** |
| Fallback import | Producer — recovery/import | `src/workflows/fallback_import.py` | `tests/workflows/test_fallback_import.py` | **No — excluded by stakeholder** |
| On-demand refresh (`POST /api/catalog/refresh`) | Producer — manual/API update | `src/api/on_demand_refresh.py` | `tests/api/test_on_demand_refresh.py` | **No — excluded by stakeholder** |
| Summary API | Consumer | `src/api/catalog_summary.py` | `tests/api/test_catalog_summary.py` | Yes (Task 3) |
| Downloadable report | Consumer | `src/reports/catalog_export.py` | `tests/reports/test_catalog_export.py` | Yes (Task 4) |

## Impact map

```
catalog-service:
  changes:
    - Add an optional `ownerGroup` field to the shared Service Catalog record schema and persistence helpers, with update semantics that preserve the stored owner group unless a new non-empty value is supplied, and without changing record ID generation
    - Collect `ownerGroup` during initial registration and persist it on the newly created catalog record
    - Expose `ownerGroup` in the catalog summary API response
    - Include an `ownerGroup` column in the downloadable catalog report
    - Update user/API documentation for the new `ownerGroup` field
```

## Unresolved scope conflict — clarification required

The stakeholder instruction excludes three producers of the same shared Service Catalog record. Repository evidence shows each of these paths creates or updates catalog records, so the Feature acceptance criteria below **cannot be claimed as satisfied** by the planned task set, which only covers the primary (registration) writer plus the readers.

| Acceptance criterion / requirement | Status with current scope | Excluded paths needed to satisfy it (source + test) | Coverage gap |
|---|---|---|---|
| AC1: "Every Service Catalog record has an `ownerGroup` value after creation **or update**." | **UNRESOLVED** — covered only for records created by registration | `src/workflows/scheduled_sync.py` + `tests/workflows/test_scheduled_sync.py`; `src/workflows/fallback_import.py` + `tests/workflows/test_fallback_import.py`; `src/api/on_demand_refresh.py` + `tests/api/test_on_demand_refresh.py` | No change or test ensures records created/updated by sync, fallback import, or on-demand refresh carry (or preserve) `ownerGroup`. A record first populated by fallback import or sync would have no `ownerGroup`. |
| AC2: "Summary API and report display `ownerGroup` for a record **regardless of how that record was populated**." | **UNRESOLVED** — readers will render the field, but no test proves a value exists for records written by the excluded paths | Same three paths as above | Consumers (Tasks 3, 4) can only display what producers write; display tests cover registration-created records only. |
| Requirement 3 / AC1 update semantics: "Updates preserve the current owner group unless a new value is supplied" (the record "may be refreshed after onboarding") | **PARTIALLY COVERED** — Task 1 implements and tests preserve-on-update in the shared store helper | `src/workflows/scheduled_sync.py`, `src/api/on_demand_refresh.py`, `src/workflows/fallback_import.py` and their tests | Not verified that these writers go through the preserving helper rather than overwriting/replacing the record; no refresh-path regression test. |
| AC3: "Existing catalog population behavior and stable IDs remain unchanged." | **PARTIALLY COVERED** — Task 1 tests stable IDs and unchanged behavior at the store level; Task 2 for registration | Excluded producers' existing test suites (`test_scheduled_sync.py`, `test_fallback_import.py`, `test_on_demand_refresh.py`) | No new regression assertions on the excluded writers. |

**Clarification requested from stakeholder (TC-9007):**

> The feature's acceptance criteria apply to every Service Catalog record "after creation or update" and "regardless of how that record was populated", but the requested scope excludes three writers of that same record: scheduled sync (`src/workflows/scheduled_sync.py`), fallback import (`src/workflows/fallback_import.py`), and on-demand refresh (`src/api/on_demand_refresh.py`). Please choose one:
> 1. **Expand scope** — add tasks covering ownerGroup population/preservation and tests for those three paths (and their tests under `tests/workflows/` and `tests/api/`).
> 2. **Narrow the acceptance criteria** — restate AC1/AC2 to apply only to records created through onboarding registration, and track the other paths in a follow-up feature.

**Non-interactive default applied:** the stakeholder's explicit exclusion was honored — none of the excluded files or tests appear in any task's Files to Modify, Files to Create, or Test Requirements. AC1 and AC2 remain **open/unresolved** pending the answer above; the task set is **not** presented as satisfying them.

## Excluded requirements

None excluded for missing inputs. (The scope-conflict items above are unresolved, not dropped.)

## Workflow mode decision

- **Selected mode:** `direct-to-main`
- **Rationale:** No atomicity indicators found.
  - Coordinated schema migration: no — `ownerGroup` is added as an optional field in Task 1; existing writers keep working unchanged, so Task 1 can land alone.
  - Breaking API change: no — the summary API and report change additively (new field/column).
  - Cross-cutting refactor: no.
  - Tightly coupled components: no — each consumer task is independently mergeable once Task 1 has landed (expressed via task dependencies).
- All tasks target `main`. No `workflow:feature-branch` label; no bookend tasks.

## Epic grouping (by-sub-feature)

- **Epic A — TC-9007: Owner group data model and onboarding** → Task 1, Task 2
- **Epic B — TC-9007: Owner group display and documentation** → Task 3, Task 4, Task 5

---
This comment was AI-generated by [sdlc-workflow/plan-feature](https://github.com/RHEcosystemAppEng/sdlc-plugins) v0.14.0.
