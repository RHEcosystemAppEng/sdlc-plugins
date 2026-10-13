# Implementation Plan for TC-9207: Remove version-based filter from SBOM list endpoint

## Overview

The task removes the version-based filtering logic from `SbomService::list`. The `version_filter`
parameter was used to apply a `VersionMatches` filter to the SBOM query, but this filtering has
been moved to the client side and is no longer needed server-side.

Removing the filter logic from the method body leaves the `version_filter` parameter dead -- it
is no longer referenced anywhere in the function body. Per Step 9's "Dead parameter detection"
guidance, dead parameters must be removed from the signature (not renamed to `_version_filter`),
and all call sites must be updated to stop passing the corresponding argument.

## Files to Modify

### 1. `modules/fundamental/src/sbom/service/sbom.rs` -- SbomService::list

**Changes:**

a. Remove the version-based filtering logic from the `list` method body. This means removing
   the code that applies the `VersionMatches` filter using the `version_filter` parameter.
   Keep the rest of the query pipeline (search, pagination, transaction) intact.

b. Remove the `version_filter: &str` parameter from the `list` method signature entirely.
   After removing the filter logic, `version_filter` has zero references in the method body,
   making it a dead parameter. The correct action is removal, not renaming to `_version_filter`.

   Before:
   ```rust
   pub async fn list(
       &self,
       search: Query,
       paginated: Paginated,
       version_filter: &str,
       tx: &Transactional<'_>,
   ) -> Result<PaginatedResults<SbomSummary>, AppError>
   ```

   After:
   ```rust
   pub async fn list(
       &self,
       search: Query,
       paginated: Paginated,
       tx: &Transactional<'_>,
   ) -> Result<PaginatedResults<SbomSummary>, AppError>
   ```

### 2. `modules/fundamental/src/sbom/endpoints/list.rs` -- endpoint handler (call site 1 of 3)

**Changes:**

a. Remove the extraction of the `version` query parameter from the request. This means removing
   the struct field or `Query` extractor that captures the `version` parameter from the URL.

b. Update the call to `SbomService::list` to stop passing the version filter argument.

   Before (conceptual):
   ```rust
   let result = sbom_service.list(search, paginated, &params.version, &tx).await?;
   ```

   After:
   ```rust
   let result = sbom_service.list(search, paginated, &tx).await?;
   ```

### 3. `modules/search/src/service/mod.rs` -- search service (call site 2 of 3)

**Changes:**

a. Update the call to `SbomService::list` to remove the version filter argument. The task
   description notes this call site passes an empty version filter (`""`), so removing it
   is straightforward.

   Before (conceptual):
   ```rust
   let sboms = sbom_service.list(search, paginated, "", &tx).await?;
   ```

   After:
   ```rust
   let sboms = sbom_service.list(search, paginated, &tx).await?;
   ```

### 4. `tests/api/sbom.rs` -- integration tests (call site 3 of 3)

**Changes:**

a. Remove or update the `test_list_sboms_version_filtered` test entirely, since the feature
   under test no longer exists. A test for removed functionality should be removed, not
   left as a no-op.

b. Update any other test calls to `SbomService::list` that pass a version filter argument --
   remove the version filter argument from those calls. Tests that exercise non-version-related
   SBOM listing behavior should remain unchanged apart from dropping the removed argument.

c. If any tests send a `version` query parameter in HTTP requests to `GET /api/v2/sbom`,
   remove that query parameter from the request construction.

## Verification Steps

1. **Compile check**: Run `cargo check` (or `cargo build`) to verify all three call sites
   compile without the removed parameter. The Rust compiler will catch any missed call sites
   as a type error.

2. **Run tests**: Run `cargo test -p trustify-fundamental` and `cargo test -p trustify-search`
   (or the appropriate crate names resolved via `cargo metadata`) to verify the modified
   crates pass. Also run the integration test suite (`cargo test --test api` or equivalent)
   to confirm the endpoint tests pass.

3. **CI checks from CONVENTIONS.md**: If CONVENTIONS.md lists CI check commands (formatting,
   linting, clippy), run those as well.

4. **Scope containment**: Verify via `git diff --name-only` that only the four files listed
   above were modified. If any other file was touched, flag it for user approval.

## Dead Parameter Detection Reasoning

The key insight is that removing the `VersionMatches` filter logic from the `list` method body
eliminates all references to the `version_filter` parameter within that function. At that point:

- The parameter appears in the signature but is never read in the body.
- Simply prefixing it with an underscore (`_version_filter`) would suppress the Rust compiler's
  `unused variable` warning, but the parameter would still be part of the public API surface.
- All three call sites would still need to construct and pass a value that is never used.
- The correct fix per the skill's Step 9 guidance is to remove the parameter from the signature
  and update all callers.

The Rust compiler enforces this naturally: after removing `version_filter` from the signature,
any call site still passing the argument will fail to compile, making it impossible to miss
a call site.
