# Parameter Cleanup: Dead Parameter Detection and Removal

## Context

Task TC-9207 removes the version-based filtering logic from `SbomService::list`. After removing the `VersionMatches` filter code from the method body, the `version_filter: &str` parameter is no longer referenced anywhere in the function body. This makes it a dead parameter.

## Dead Parameter Detection Reasoning

### How the dead parameter was identified

1. **Code removal created the dead parameter**: The task requires removing the version-based filtering logic from `SbomService::list`. Before the change, the `version_filter` parameter was used in the method body to apply a `VersionMatches` filter. After removing that filter logic, the parameter has zero references in the method body.

2. **The `git diff` reveals it**: The removed lines contained the only references to `version_filter` in the function body. After the diff is applied, scanning the remaining function body shows no occurrences of `version_filter`.

3. **Compiler confirmation**: The Rust compiler would emit a warning: "unused variable: `version_filter`". This confirms the parameter is dead.

## Why Removal, Not Underscore Prefix

Dead parameters should be **removed from the function signature entirely**, not prefixed with an underscore (e.g., `_version_filter`).

### The underscore prefix is the wrong fix

Prefixing a parameter with an underscore (`_version_filter`) suppresses the Rust compiler's unused-variable warning, but it does NOT fix the underlying problem. The parameter is still there:

- **Unnecessary API surface**: Every caller must still pass a value for the dead parameter, even though it is ignored. This is confusing to callers who must wonder what value to pass for a parameter that does nothing.
- **Maintenance burden**: Future developers reading the function signature will see the parameter and assume it has a purpose. They may waste time trying to understand what it does or fear removing it.
- **Misleading contract**: The function's signature is its contract. A parameter in the signature promises "I use this value." A dead parameter breaks that promise.
- **Accumulated tech debt**: Underscore-prefixed parameters tend to accumulate over time. Each one is a small lie in the API that compounds into confusion.

### The correct fix is removal

Remove the parameter from the function signature and update all call sites to stop passing the corresponding argument. This:

- Simplifies the API surface
- Eliminates confusion for callers
- Ensures the function signature accurately reflects what the function actually uses
- Prevents accumulation of dead parameters over time

## Call Site Updates

Removing `version_filter` from the `SbomService::list` signature requires updating all 3 call sites:

### 1. Endpoint handler (`modules/fundamental/src/sbom/endpoints/list.rs`)

```rust
// Before:
service.list(search, paginated, &version, &tx).await
// After:
service.list(search, paginated, &tx).await
```

Also remove the `version` query parameter extraction from the handler, since there is no longer a parameter to pass it to.

### 2. Search service (`modules/search/src/service/mod.rs`)

```rust
// Before:
sbom_service.list(search, paginated, "", &tx).await
// After:
sbom_service.list(search, paginated, &tx).await
```

Note: this call site was passing an empty string `""` for the version filter, which already indicated the parameter was not meaningfully used here.

### 3. Integration tests (`tests/api/sbom.rs`)

```rust
// Before:
service.list(search, paginated, "1.0", &tx).await
// After:
service.list(search, paginated, &tx).await
```

Remove version_filter arguments from all test calls to `SbomService::list`. Also remove or update `test_list_sboms_version_filtered` since the feature is being removed entirely.

## Verification

After removing the parameter and updating all call sites, re-run the full test suite to confirm nothing broke:

```
cargo test
```

This verifies that:
- The code compiles without errors (no missing arguments at any call site)
- The code compiles without warnings (no unused parameter warnings)
- All remaining tests pass (no behavioral regressions)
- The search service and endpoint handler work correctly without the version filter

If any test fails after the parameter removal and call site updates, it indicates an undiscovered call site or a test that depended on the version filtering behavior, which would need to be addressed.
