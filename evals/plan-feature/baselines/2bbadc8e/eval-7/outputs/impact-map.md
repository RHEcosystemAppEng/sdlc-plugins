# Repository Impact Map — TC-9007: Add an owner group to Service Catalog records

## Workflow Mode

**Selected mode:** `direct-to-main`

**Rationale:** No atomicity indicators found. The `ownerGroup` field is additive — adding an optional field to the catalog record schema, updating writers to populate or preserve it, and updating consumers to display it can each be merged independently without leaving `main` in a broken state. All changes are within a single repository (`catalog-service`).

---

## catalog-service

### Shared Artifact: Service Catalog Record

The Service Catalog is the shared artifact. The acceptance criteria require that every record has an `ownerGroup` value "regardless of how that record was populated." This means all four population paths must be covered, not just the primary registration workflow.

### Store (shared schema and persistence)

| Source Path | Test Path | Changes |
|---|---|---|
| `src/catalog/store.py` | `tests/catalog/test_store.py` | Add `ownerGroup` field to catalog record schema; persistence helpers handle create/update with the new field; omitted-update preservation (update without `ownerGroup` retains existing value); explicit replacement (update with `ownerGroup` applies new value); stable IDs unchanged |

### Writer Paths (producers)

| Source Path | Test Path | Validation |
|---|---|---|
| `src/workflows/registration.py` | `tests/workflows/test_registration.py` | Persists `ownerGroup` collected during initial onboarding |
| `src/workflows/scheduled_sync.py` | `tests/workflows/test_scheduled_sync.py` | Preserves existing `ownerGroup` when sync payload omits it; applies supplied replacement |
| `src/workflows/fallback_import.py` | `tests/workflows/test_fallback_import.py` | Preserves existing `ownerGroup` when import data omits it; applies supplied replacement |
| `src/api/on_demand_refresh.py` | `tests/api/test_on_demand_refresh.py` | Preserves existing `ownerGroup` when refresh payload omits it; applies supplied replacement |

### Consumer Paths (readers)

| Source Path | Test Path | Changes |
|---|---|---|
| `src/api/catalog_summary.py` | `tests/api/test_catalog_summary.py` | Include `ownerGroup` in summary API response |
| `src/reports/catalog_export.py` | `tests/reports/test_catalog_export.py` | Include `ownerGroup` in downloadable report output |

### Documentation

- Update documentation to describe the shared Service Catalog contract, including that records may be populated through registration, scheduled synchronization, fallback import, or on-demand refresh, and that all paths use the same catalog contract with `ownerGroup`.

---

## Excluded Requirements

None. All requirements from the Feature description are covered.
