# Criterion 6: Existing package list endpoint tests continue to pass (backward compatible)

## Verdict: PASS

## Analysis

Per the eval scenario, all CI checks pass. The change is additive: a new field (`vulnerability_count`) is added to the `PackageSummary` response struct. Additive field changes are generally backward compatible for API consumers -- existing tests that deserialize the response would either ignore unknown fields or would need to be updated to include the new field.

The endpoint handler signature and routing remain unchanged. The `list` function in the service retains the same parameters (`offset`, `limit`). The only structural change is the addition of the new field in the mapping closure, which does not alter the existing field mappings.

The diff does not remove or rename any existing fields, and the existing endpoint structure (`GET /api/v2/package`) is preserved.

## Evidence

- CI checks pass (per eval scenario)
- No existing fields removed or renamed in `PackageSummary`
- Endpoint route and handler signature unchanged in `list.rs`
- Service method signature unchanged in `service/mod.rs`
- Change is purely additive (new field added)
