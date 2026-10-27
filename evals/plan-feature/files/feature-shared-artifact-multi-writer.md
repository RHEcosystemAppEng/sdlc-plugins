<!-- SYNTHETIC TEST DATA — fictional Jira feature and repository paths for shared-artifact planning evals. -->
# Mock Jira Feature Issue

**Key**: TC-9007
**Summary**: Add an owner group to Service Catalog records
**Status**: New
**Priority**: Major
**Fix Versions**: None
**Labels**: ai-generated-jira
**Linked Issues**: None

---

## Feature Overview

The platform stores service records in one shared Service Catalog. Add an `ownerGroup` field so users can see who owns each service. The catalog is used by the summary API and downloadable report. Keep the implementation small and focus on the onboarding flow where records are first created.

## Requirements

| Requirement | Notes | Is MVP? |
|---|---|---|
| A registered service record includes its `ownerGroup` | Collected during initial onboarding | Yes |
| The catalog summary API and downloadable report show `ownerGroup` | Read the shared Service Catalog record | Yes |
| Updates to a service record preserve the current owner group unless a new value is supplied | The record may be refreshed after onboarding | Yes |
| Add focused tests for onboarding and display | Keep scope small where practical | Yes |

## Acceptance Criteria

- Every Service Catalog record has an `ownerGroup` value after creation or update.
- The summary API and downloadable report display `ownerGroup` for a record regardless of how that record was populated.
- Existing catalog population behavior and stable IDs remain unchanged.

## Repository Structure: catalog-service

The following files exist in one repository. The Service Catalog is the shared source of service records, and the feature description names the initial onboarding flow as its focus.

| Path | Existing behavior |
|---|---|
| `src/catalog/store.py` | Shared catalog record schema and persistence helpers |
| `src/workflows/registration.py` | Adds a service to the catalog during initial registration |
| `src/workflows/scheduled_sync.py` | Synchronizes service metadata from the provider on a scheduled run |
| `src/workflows/fallback_import.py` | Loads previously exported service data when provider synchronization is unavailable |
| `src/api/on_demand_refresh.py` | Handles `POST /api/catalog/refresh` for an operator-requested service refresh |
| `src/api/catalog_summary.py` | Reads catalog records for the summary API |
| `src/reports/catalog_export.py` | Reads catalog records for the downloadable report |
| `tests/catalog/test_store.py` | Shared catalog persistence tests |
| `tests/workflows/test_registration.py` | Registration workflow tests |
| `tests/workflows/test_scheduled_sync.py` | Scheduled synchronization tests |
| `tests/workflows/test_fallback_import.py` | Fallback-import tests |
| `tests/api/test_on_demand_refresh.py` | On-demand refresh API tests |
| `tests/api/test_catalog_summary.py` | Summary API tests |
| `tests/reports/test_catalog_export.py` | Catalog export tests |

## Documentation Considerations

- **Doc Impact**: Updates — document that catalog records may be populated through registration, scheduled synchronization, fallback import, or on-demand refresh.
- **User purpose**: Operators and API consumers need to understand that all paths use the same catalog contract.
