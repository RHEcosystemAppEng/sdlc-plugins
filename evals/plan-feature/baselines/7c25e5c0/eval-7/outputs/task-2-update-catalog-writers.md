## Repository
catalog-service

## Target Branch
main

## Description
Update all four catalog writer paths to handle the `ownerGroup` field correctly. Each writer populates Service Catalog records through a different workflow, and each must handle `ownerGroup` per its path-specific semantics:

- **Registration** (`src/workflows/registration.py`): persists the supplied `ownerGroup` during initial onboarding
- **Scheduled sync** (`src/workflows/scheduled_sync.py`): preserves existing `ownerGroup` when omitted; applies a supplied replacement
- **Fallback import** (`src/workflows/fallback_import.py`): preserves existing `ownerGroup` when omitted; applies a supplied replacement
- **On-demand refresh** (`src/api/on_demand_refresh.py`): preserves existing `ownerGroup` when omitted; applies a supplied replacement

## Files to Modify
- `src/workflows/registration.py` — pass `ownerGroup` through to the catalog store during initial registration
- `src/workflows/scheduled_sync.py` — preserve existing `ownerGroup` when sync payload omits it; apply replacement when supplied
- `src/workflows/fallback_import.py` — preserve existing `ownerGroup` when import data omits it; apply replacement when supplied
- `src/api/on_demand_refresh.py` — preserve existing `ownerGroup` when refresh payload omits it; apply replacement when supplied
- `tests/workflows/test_registration.py` — add tests for `ownerGroup` persistence during registration
- `tests/workflows/test_scheduled_sync.py` — add tests for `ownerGroup` preservation and replacement during sync
- `tests/workflows/test_fallback_import.py` — add tests for `ownerGroup` preservation and replacement during fallback import
- `tests/api/test_on_demand_refresh.py` — add tests for `ownerGroup` preservation and replacement during on-demand refresh

## Implementation Notes
- Follow the existing field-passing pattern in each writer for adding new fields to catalog store calls
- **Registration path** (`src/workflows/registration.py`): this is the primary onboarding path; `ownerGroup` is a required input collected during registration. Pass it directly to the store's create/persist method.
- **Scheduled sync path** (`src/workflows/scheduled_sync.py`): sync payloads from the provider may not include `ownerGroup`. Use the store's preserve-on-omit semantics so existing values are kept when the sync payload does not supply a replacement.
- **Fallback import path** (`src/workflows/fallback_import.py`): same preserve-on-omit semantics as scheduled sync. Previously exported data may or may not include `ownerGroup`.
- **On-demand refresh path** (`src/api/on_demand_refresh.py`): same preserve-on-omit semantics. The `POST /api/catalog/refresh` handler should accept an optional `ownerGroup` in the request body.
- All four writers use `src/catalog/store.py` persistence helpers (Task 1). The preserve-on-omit and explicit-replacement logic lives in the store; writers only need to pass through the value (or omit it).

## Acceptance Criteria
- [ ] Registration workflow persists the supplied `ownerGroup` on newly created catalog records
- [ ] Scheduled sync preserves existing `ownerGroup` when sync payload omits the field
- [ ] Scheduled sync replaces `ownerGroup` when sync payload supplies a new value
- [ ] Fallback import preserves existing `ownerGroup` when import data omits the field
- [ ] Fallback import replaces `ownerGroup` when import data supplies a new value
- [ ] On-demand refresh preserves existing `ownerGroup` when refresh payload omits the field
- [ ] On-demand refresh replaces `ownerGroup` when refresh payload supplies a new value
- [ ] Existing catalog population behavior and stable IDs remain unchanged across all writers

## Test Requirements
- [ ] Test registration persists `ownerGroup` in `tests/workflows/test_registration.py`
- [ ] Test scheduled sync preserves existing `ownerGroup` when omitted in `tests/workflows/test_scheduled_sync.py`
- [ ] Test scheduled sync replaces `ownerGroup` when supplied in `tests/workflows/test_scheduled_sync.py`
- [ ] Test fallback import preserves existing `ownerGroup` when omitted in `tests/workflows/test_fallback_import.py`
- [ ] Test fallback import replaces `ownerGroup` when supplied in `tests/workflows/test_fallback_import.py`
- [ ] Test on-demand refresh preserves existing `ownerGroup` when omitted in `tests/api/test_on_demand_refresh.py`
- [ ] Test on-demand refresh replaces `ownerGroup` when supplied in `tests/api/test_on_demand_refresh.py`

## Dependencies
- Depends on: Task 1 — Add ownerGroup to catalog store
