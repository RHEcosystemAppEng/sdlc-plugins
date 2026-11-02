# Parameter Cleanup — TC-9207: Dead Parameter Detection and Removal

## Dead Parameter Detection Reasoning

When removing the version filtering logic from `SbomService::list`, the `version_filter: &str` parameter becomes dead — it is no longer referenced anywhere in the function body. The Rust compiler would emit a warning about the unused parameter, but the correct fix is **removal**, not suppression.

### Why removal, not underscore prefixing

Prefixing with an underscore (`_version_filter`) suppresses the compiler warning but:
- **Leaves unnecessary API surface**: every caller must still construct and pass a value that is never used
- **Misleads readers**: the parameter's presence suggests it does something
- **Violates the interface segregation principle**: callers are coupled to an argument they don't need
- **Accumulates cruft**: underscore-prefixed parameters tend to persist indefinitely

Dead parameters should be removed from the signature entirely. This forces updating all call sites, which is the correct outcome — each caller gets simpler, and the API accurately reflects what the function uses.

## Call Site Analysis

The `SbomService::list` method has **3 call sites** that must be updated when removing the `version_filter` parameter:

### 1. Endpoint handler — `modules/fundamental/src/sbom/endpoints/list.rs`

**Current**: Extracts `version` from query parameters and passes it to `service.list(search, paginated, &version, &tx)`

**After**: Remove the `version` query parameter extraction. Call becomes `service.list(search, paginated, &tx)`. The `version` field can also be removed from the query parameter struct.

### 2. Search service — `modules/search/src/service/mod.rs`

**Current**: Calls `sbom_service.list(search, paginated, "", &tx)` with an empty string for version filter (search service never filters by version).

**After**: Call becomes `sbom_service.list(search, paginated, &tx)`. This simplifies the search service code by removing the vestigial empty argument.

### 3. Integration tests — `tests/api/sbom.rs`

**Current**: `test_list_sboms_version_filtered` calls `list` with various version filter values. Other tests may also pass a version filter argument.

**After**:
- Remove `test_list_sboms_version_filtered` entirely — the feature under test no longer exists
- Update all remaining test calls to `list` to remove the version filter argument
- Verify remaining tests still pass

## Verification

After removing the parameter and updating all call sites:

1. **Compile check**: `cargo check -p <fundamental-crate>` and `cargo check -p <search-crate>` — ensures no call sites were missed
2. **Test run**: `cargo test -p <fundamental-crate>` and the integration test crate — ensures no behavioral regressions
3. **Grep verification**: `grep -rn "version_filter" modules/ tests/` — confirms no remaining references to the removed parameter
