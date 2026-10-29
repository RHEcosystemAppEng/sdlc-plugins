## Repository
catalog-service

## Target Branch
main

## Description
Add an `ownerGroup` field to the Service Catalog record schema and propagate it through all four population paths and both consumers. The Service Catalog is a shared artifact populated by four distinct writer paths: registration (primary onboarding), scheduled sync, fallback import, and on-demand refresh. Two consumers read the catalog: the summary API and the downloadable report.

The registration workflow collects `ownerGroup` during initial onboarding and persists it on the new record. The three update paths (scheduled sync, fallback import, on-demand refresh) must preserve the existing `ownerGroup` value when no replacement is supplied, and apply the new value when one is explicitly provided. Both consumers must include `ownerGroup` in their output regardless of which path populated the record.

Existing catalog population behavior and stable IDs must remain unchanged.

## Files to Modify
- `src/catalog/store.py` — Add `ownerGroup` field to catalog record schema and update persistence helpers for create/update
- `src/workflows/registration.py` — Accept and persist `ownerGroup` from onboarding input
- `src/workflows/scheduled_sync.py` — Preserve existing `ownerGroup` on sync when omitted; apply replacement when supplied
- `src/workflows/fallback_import.py` — Preserve existing `ownerGroup` on import when omitted; apply replacement when supplied
- `src/api/on_demand_refresh.py` — Preserve existing `ownerGroup` on refresh when omitted; apply replacement when supplied
- `src/api/catalog_summary.py` — Include `ownerGroup` in summary API response
- `src/reports/catalog_export.py` — Include `ownerGroup` in downloadable report output
- `tests/catalog/test_store.py` — Add tests for ownerGroup persistence, omitted-update preservation, explicit replacement, and stable-ID compatibility
- `tests/workflows/test_registration.py` — Add test verifying registration persists ownerGroup
- `tests/workflows/test_scheduled_sync.py` — Add tests for preserve-on-omit and apply-on-replace semantics
- `tests/workflows/test_fallback_import.py` — Add tests for preserve-on-omit and apply-on-replace semantics
- `tests/api/test_on_demand_refresh.py` — Add tests for preserve-on-omit and apply-on-replace semantics
- `tests/api/test_catalog_summary.py` — Add test verifying summary API includes ownerGroup
- `tests/reports/test_catalog_export.py` — Add test verifying catalog export includes ownerGroup

## Implementation Notes
**Store layer (`src/catalog/store.py`):**
- Add `ownerGroup` as an optional string field on the catalog record schema.
- Update persistence helpers so that create operations accept and store `ownerGroup`, and update operations implement omitted-field preservation: when the update payload does not include `ownerGroup`, the existing value is retained; when the payload includes an explicit value, it replaces the current one.
- Verify that adding the field does not alter existing record identifiers (stable-ID compatibility).

**Registration path (`src/workflows/registration.py`):**
- Accept `ownerGroup` in the onboarding input and pass it to the catalog store's create method.
- PATH-SPECIFIC VALIDATION: Registration persists `ownerGroup` — this is the primary collection point.

**Scheduled sync path (`src/workflows/scheduled_sync.py`):**
- PATH-SPECIFIC VALIDATION: When the sync payload omits `ownerGroup`, the existing catalog record's `ownerGroup` must be preserved. When the sync payload includes `ownerGroup`, the new value replaces the existing one.

**Fallback import path (`src/workflows/fallback_import.py`):**
- PATH-SPECIFIC VALIDATION: When the import data omits `ownerGroup`, the existing catalog record's `ownerGroup` must be preserved. When the import data includes `ownerGroup`, the new value replaces the existing one.

**On-demand refresh path (`src/api/on_demand_refresh.py`):**
- PATH-SPECIFIC VALIDATION: When the refresh payload omits `ownerGroup`, the existing catalog record's `ownerGroup` must be preserved. When the refresh payload includes `ownerGroup`, the new value replaces the existing one.

**Consumer paths:**
- `src/api/catalog_summary.py`: Read `ownerGroup` from the catalog record and include it in the API response. No transformation needed.
- `src/reports/catalog_export.py`: Read `ownerGroup` from the catalog record and include it in the report output. No transformation needed.

**Preservation pattern:** All three update paths (sync, fallback, on-demand) share the same omitted-field preservation logic. Implement the preservation semantics in the store layer's update helper so each writer delegates to the shared behavior rather than reimplementing it.

**Existing behavior:** Do not change the fixture's existing-population behavior. Ensure test fixtures for existing tests continue to work after adding the new field.

## Acceptance Criteria
- [ ] `src/catalog/store.py` schema includes `ownerGroup` field
- [ ] Registration workflow persists `ownerGroup` from onboarding input
- [ ] Scheduled sync preserves existing `ownerGroup` when the sync payload omits it
- [ ] Scheduled sync replaces `ownerGroup` when a new value is supplied in the sync payload
- [ ] Fallback import preserves existing `ownerGroup` when the import data omits it
- [ ] Fallback import replaces `ownerGroup` when a new value is supplied in the import data
- [ ] On-demand refresh preserves existing `ownerGroup` when the refresh payload omits it
- [ ] On-demand refresh replaces `ownerGroup` when a new value is supplied in the refresh payload
- [ ] Summary API response includes `ownerGroup` for every catalog record
- [ ] Downloadable report includes `ownerGroup` for every catalog record
- [ ] Existing catalog population behavior remains unchanged
- [ ] Stable IDs remain unchanged after adding the new field

## Test Requirements
- [ ] `tests/catalog/test_store.py`: ownerGroup persistence on create — a new record stores the provided ownerGroup value
- [ ] `tests/catalog/test_store.py`: omitted-update preservation — updating a record without ownerGroup in the payload retains the existing ownerGroup value
- [ ] `tests/catalog/test_store.py`: explicit replacement — updating a record with a new ownerGroup value replaces the existing one
- [ ] `tests/catalog/test_store.py`: stable IDs unchanged — adding ownerGroup to a record does not alter the record's identifier
- [ ] `tests/workflows/test_registration.py`: registration persists the ownerGroup value from onboarding input
- [ ] `tests/workflows/test_scheduled_sync.py`: sync preserves existing ownerGroup when sync payload omits ownerGroup
- [ ] `tests/workflows/test_scheduled_sync.py`: sync applies supplied ownerGroup replacement when sync payload includes ownerGroup
- [ ] `tests/workflows/test_fallback_import.py`: fallback import preserves existing ownerGroup when import data omits ownerGroup
- [ ] `tests/workflows/test_fallback_import.py`: fallback import applies supplied ownerGroup replacement when import data includes ownerGroup
- [ ] `tests/api/test_on_demand_refresh.py`: on-demand refresh preserves existing ownerGroup when refresh payload omits ownerGroup
- [ ] `tests/api/test_on_demand_refresh.py`: on-demand refresh applies supplied ownerGroup replacement when refresh payload includes ownerGroup
- [ ] `tests/api/test_catalog_summary.py`: summary API response includes ownerGroup for a catalog record
- [ ] `tests/reports/test_catalog_export.py`: catalog export output includes ownerGroup for a catalog record

## Documentation Updates
- Update Service Catalog documentation to describe the `ownerGroup` field and the shared catalog contract across all four population paths (registration, scheduled sync, fallback import, on-demand refresh)

## Dependencies
- None
