# Repository Impact Map — TC-9007

## catalog-service

### Shared artifact: Service Catalog record

The Service Catalog record is a shared artifact populated by four distinct writer paths and consumed by two reader paths. The acceptance criteria require that every record has an `ownerGroup` value "regardless of how that record was populated," so all writers and consumers must be covered.

### Writer paths (producers)

| Writer | Path | Test path | Path-specific behavior |
|---|---|---|---|
| Registration | `src/workflows/registration.py` | `tests/workflows/test_registration.py` | Persists the supplied `ownerGroup` during initial onboarding |
| Scheduled sync | `src/workflows/scheduled_sync.py` | `tests/workflows/test_scheduled_sync.py` | Preserves existing `ownerGroup` when omitted; applies a supplied replacement |
| Fallback import | `src/workflows/fallback_import.py` | `tests/workflows/test_fallback_import.py` | Preserves existing `ownerGroup` when omitted; applies a supplied replacement |
| On-demand refresh | `src/api/on_demand_refresh.py` | `tests/api/test_on_demand_refresh.py` | Preserves existing `ownerGroup` when omitted; applies a supplied replacement |

### Consumer paths (readers)

| Consumer | Path | Test path |
|---|---|---|
| Summary API | `src/api/catalog_summary.py` | `tests/api/test_catalog_summary.py` |
| Downloadable report | `src/reports/catalog_export.py` | `tests/reports/test_catalog_export.py` |

### Store layer

| Path | Test path | Changes |
|---|---|---|
| `src/catalog/store.py` | `tests/catalog/test_store.py` | Add `ownerGroup` field to catalog record schema and persistence helpers |

### Changes

- Add `ownerGroup` field to catalog record schema in `src/catalog/store.py`
- Update `src/workflows/registration.py` to persist `ownerGroup` during initial registration
- Update `src/workflows/scheduled_sync.py` to preserve existing `ownerGroup` when omitted and apply a supplied replacement
- Update `src/workflows/fallback_import.py` to preserve existing `ownerGroup` when omitted and apply a supplied replacement
- Update `src/api/on_demand_refresh.py` to preserve existing `ownerGroup` when omitted and apply a supplied replacement
- Update `src/api/catalog_summary.py` to include `ownerGroup` in summary API response
- Update `src/reports/catalog_export.py` to include `ownerGroup` in downloadable report output
- Update all corresponding test files to cover `ownerGroup` persistence, preservation, replacement, and display
- Existing catalog population behavior and stable IDs remain unchanged

### Workflow mode

**direct-to-main** — no atomicity constraints; each task can be merged independently without breaking main.

### Inherited field propagation

- **Priority**: Major (inherited from Feature TC-9007, propagated to all created tasks)
- **fixVersions**: None on Feature — fixVersion inheritance skipped
