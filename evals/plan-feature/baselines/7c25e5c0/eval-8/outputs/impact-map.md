# Repository Impact Map — TC-9007: Add an owner group to Service Catalog records

## catalog-service

### Changes (in-scope per stakeholder instruction)

- Add `ownerGroup` field to the shared catalog record schema in `src/catalog/store.py`, including persistence helpers for setting, preserving, and replacing the value
- Capture `ownerGroup` during initial registration in `src/workflows/registration.py`
- Expose `ownerGroup` in the summary API response via `src/api/catalog_summary.py`
- Expose `ownerGroup` in the downloadable report via `src/reports/catalog_export.py`
- Add tests for `ownerGroup` persistence in `tests/catalog/test_store.py`
- Add tests for `ownerGroup` capture in `tests/workflows/test_registration.py`
- Add tests for `ownerGroup` display in `tests/api/test_catalog_summary.py` and `tests/reports/test_catalog_export.py`

## Unresolved scope conflict — stakeholder exclusion vs. acceptance criteria

The following acceptance criterion applies universally across all population paths:

> "Every Service Catalog record has an `ownerGroup` value after creation or update."
> "The summary API and downloadable report display `ownerGroup` for a record regardless of how that record was populated."

The stakeholder explicitly excluded scheduled synchronization, fallback import, and on-demand refresh from scope. However, these three paths also populate Service Catalog records and are therefore subject to the universal acceptance criteria above. Covering only registration and display does **not** satisfy these criteria — records created or updated by the excluded paths would lack `ownerGroup` handling.

**Scope clarification is required before these criteria can be marked as met.**

### Excluded writer files and matching tests (unresolved)

| Excluded writer path | Matching test path | Impact |
|---|---|---|
| `src/workflows/scheduled_sync.py` | `tests/workflows/test_scheduled_sync.py` | Sync-refreshed records would not preserve or receive `ownerGroup` |
| `src/workflows/fallback_import.py` | `tests/workflows/test_fallback_import.py` | Fallback-imported records would not preserve or receive `ownerGroup` |
| `src/api/on_demand_refresh.py` | `tests/api/test_on_demand_refresh.py` | Operator-refreshed records would not preserve or receive `ownerGroup` |

These paths are listed here as unresolved exclusions only. They do **not** appear in any task's Files to Modify, Files to Create, or Test Requirements, per the stakeholder instruction.

### Unresolved acceptance criteria

The following acceptance criteria **cannot** be claimed as met by the in-scope tasks alone:

1. **"Every Service Catalog record has an `ownerGroup` value after creation or update"** — only registration is in scope; records created or updated via scheduled sync, fallback import, or on-demand refresh are not covered.
2. **"The summary API and downloadable report display `ownerGroup` for a record regardless of how that record was populated"** — display code will show the field, but records populated by excluded paths may have no `ownerGroup` value to display.
3. **"Existing catalog population behavior and stable IDs remain unchanged"** — cannot verify this for excluded paths without their test coverage.

## Workflow mode

**Direct-to-main** — no atomicity constraints identified among the in-scope changes. The schema change, registration update, and consumer updates can be merged incrementally.

## Inherited field propagation

- **Priority**: Major (inherited from Feature TC-9007; will be propagated to all created tasks)
- **Fix Versions**: None on the Feature — fixVersion inheritance skipped
