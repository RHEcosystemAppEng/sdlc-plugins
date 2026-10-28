# Dead Parameter Cleanup: `version_filter` in `SbomService::list`

## What Makes `version_filter` a Dead Parameter

After removing the `VersionMatches` filtering logic from the `list` method body (the
primary task in TC-9207), the `version_filter: &str` parameter remains in the function
signature but is never read, used, or referenced anywhere in the function body. This
makes it a dead parameter -- a parameter that exists in the API contract but serves no
purpose at runtime.

## Why Dead Parameters Must Be Removed, Not Underscore-Prefixed

The implement-task skill's dead parameter detection step (Step 9) is explicit:
"The correct fix is removal, not renaming." There are several concrete reasons for this:

### 1. Underscore-prefixing hides the problem instead of fixing it

Renaming `version_filter` to `_version_filter` silences the compiler warning but
preserves the dead parameter in the public API. Every caller must still construct and
pass a value that is immediately discarded. This is misleading -- callers (including the
endpoint handler and search service) appear to support version filtering when they do not.

### 2. It imposes maintenance cost on all callers

With 3 call sites, each one must continue to pass a meaningless argument:
- The endpoint handler must continue to extract a `version` query parameter from the
  HTTP request, even though it has no effect.
- The search service must continue to pass an empty string `""` as a version filter.
- Tests must continue to construct version filter values for a feature that no longer
  exists.

Every future caller of `SbomService::list` will also need to figure out what to pass
for a parameter that does nothing.

### 3. It violates the principle of least surprise

A function signature is a contract. When a caller sees `version_filter: &str` in the
signature, they reasonably expect that value to affect behavior. A dead parameter
violates this expectation and wastes the caller's time investigating what values to pass
and what effect they have (answer: none).

### 4. It creates false API surface

The `version` query parameter on `GET /api/v2/sbom` would remain documented and
accepted, leading API consumers to believe version filtering works. Removing the
parameter from the function signature naturally drives removal of the query parameter
from the endpoint, keeping the external API honest about its capabilities.

### 5. Underscore-prefixing is for intentional non-use, not accidental dead code

The underscore prefix convention (`_version_filter`, `_ctx`) exists for parameters that
are intentionally unused in a specific implementation but required by a trait, interface,
or callback signature. For example, a trait method `fn on_event(&self, _ctx: &Context)`
where a particular implementation does not need the context. That is a legitimate use
of the convention. Dead parameters created by removing their only usage are not in this
category -- there is no trait or interface requiring the parameter to exist.

## Approach to Removal

### Step 1: Remove from function signature

Remove `version_filter: &str` from the `SbomService::list` method signature:

```rust
// Before
pub async fn list(
    &self,
    search: Query,
    paginated: Paginated,
    version_filter: &str,       // REMOVE
    tx: &Transactional<'_>,
) -> Result<PaginatedResults<SbomSummary>, AppError>

// After
pub async fn list(
    &self,
    search: Query,
    paginated: Paginated,
    tx: &Transactional<'_>,
) -> Result<PaginatedResults<SbomSummary>, AppError>
```

### Step 2: Identify all call sites

Use `find_referencing_symbols` on `SbomService::list` (or Grep for `\.list(` in the
relevant modules) to locate every call site. The task identifies 3:

| # | File | Current Call | Updated Call |
|---|------|-------------|--------------|
| 1 | `modules/fundamental/src/sbom/endpoints/list.rs` | `service.list(search, paginated, &version, &tx)` | `service.list(search, paginated, &tx)` |
| 2 | `modules/search/src/service/mod.rs` | `sbom_service.list(search, paginated, "", &tx)` | `sbom_service.list(search, paginated, &tx)` |
| 3 | `tests/api/sbom.rs` | `service.list(search, paginated, "1.0", &tx)` (and similar) | `service.list(search, paginated, &tx)` |

### Step 3: Update each call site

For each call site, remove the `version_filter` argument from the function call. This is
a positional argument in Rust, so removing it shifts subsequent arguments forward. The
compiler will catch any call sites that are missed -- they will fail to compile with an
argument count mismatch.

**Call site 1 -- endpoint handler (`list.rs`):**
- Remove the `version` query parameter extraction (e.g., `let version = query.version.unwrap_or_default();`).
- Remove the version argument from the service call.
- Remove any related struct field from the query parameter struct (e.g., `version: Option<String>` from a `ListQuery` struct).

**Call site 2 -- search service (`mod.rs`):**
- Remove the empty string argument `""` from the call.
- No other changes needed.

**Call site 3 -- integration tests (`sbom.rs`):**
- Remove version filter arguments from all `list` calls in remaining tests.
- Delete the `test_list_sboms_version_filtered` test entirely (it tests removed functionality).

### Step 4: Re-run tests

After all call sites are updated, re-run the test suite for all affected crates:

```bash
cargo test -p <fundamental-crate>
cargo test -p <search-crate>
cargo test --test api
```

This confirms:
- No compilation errors from mismatched arguments.
- No runtime failures from the removed feature.
- Existing tests that do not depend on version filtering still pass.

## Scope Note

The search service file (`modules/search/src/service/mod.rs`) is not listed in the
task's "Files to Modify" section but must be updated as part of dead parameter cleanup.
The implement-task skill requires all call sites to be updated when removing a parameter
(Step 9, dead parameter detection). This out-of-scope modification would be flagged
during the scope containment check and presented to the user for explicit approval
before committing.
