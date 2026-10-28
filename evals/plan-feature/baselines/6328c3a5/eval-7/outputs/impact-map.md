# Repository Impact Map -- TC-9007

## catalog-service

changes:
  - Add `ownerGroup` field to the shared catalog record schema in `src/catalog/store.py` with persistence support
  - Update `src/workflows/registration.py` to collect and persist `ownerGroup` during initial onboarding registration
  - Update `src/workflows/scheduled_sync.py` to preserve existing `ownerGroup` unless a new value is supplied during scheduled sync
  - Update `src/workflows/fallback_import.py` to persist `ownerGroup` from imported data during fallback import
  - Update `src/api/on_demand_refresh.py` to preserve existing `ownerGroup` unless a new value is supplied during on-demand refresh
  - Update `src/api/catalog_summary.py` to include `ownerGroup` in summary API responses
  - Update `src/reports/catalog_export.py` to include `ownerGroup` in downloadable report output
  - Add persistence tests for `ownerGroup` in `tests/catalog/test_store.py`
  - Add/update tests for all four writer paths and both consumer paths

## Shared-Artifact Analysis

**Artifact:** Service Catalog record (shared record contract in `src/catalog/store.py`)

### Writers (populate the artifact)

| # | Path | Role | Test Path |
|---|---|---|---|
| 1 | `src/workflows/registration.py` | Adds a service during initial onboarding registration | `tests/workflows/test_registration.py` |
| 2 | `src/workflows/scheduled_sync.py` | Synchronizes service metadata on a scheduled run | `tests/workflows/test_scheduled_sync.py` |
| 3 | `src/workflows/fallback_import.py` | Loads exported service data when sync is unavailable | `tests/workflows/test_fallback_import.py` |
| 4 | `src/api/on_demand_refresh.py` | Handles `POST /api/catalog/refresh` for operator-requested refresh | `tests/api/test_on_demand_refresh.py` |

### Consumers (read the artifact)

| # | Path | Role | Test Path |
|---|---|---|---|
| 1 | `src/api/catalog_summary.py` | Reads catalog records for the summary API | `tests/api/test_catalog_summary.py` |
| 2 | `src/reports/catalog_export.py` | Reads catalog records for the downloadable report | `tests/reports/test_catalog_export.py` |

### Schema / Persistence

| Path | Test Path |
|---|---|
| `src/catalog/store.py` | `tests/catalog/test_store.py` |

## Workflow Mode Decision

**Selected mode:** direct-to-main

**Rationale:** No atomicity indicators detected. Adding the `ownerGroup` field is an additive schema change. Each writer and consumer can be updated incrementally without leaving `main` in a broken state. No coordinated schema migrations, breaking API changes, cross-cutting refactors, or tightly coupled components were identified.
