# Implementation Plan for TC-9207: Remove version-based filter from SBOM list endpoint

## Summary

Remove the version-based filtering logic from the SBOM list endpoint. The `version_filter`
parameter was used to filter SBOMs by version string, but version filtering has moved to the
client side. This task removes the filter logic from the service method body and then
propagates the removal through all layers: the parameter itself, all call sites, the endpoint
query parameter extraction, and the related test.

## Files to Modify

### 1. `modules/fundamental/src/sbom/service/sbom.rs` -- Service method (primary change)

**What changes:**

- Locate the `SbomService::list` method. Its current signature is:

  ```rust
  pub async fn list(
      &self,
      search: Query,
      paginated: Paginated,
      version_filter: &str,
      tx: &Transactional<'_>,
  ) -> Result<PaginatedResults<SbomSummary>, AppError>
  ```

- **Remove the filtering logic** in the method body that uses `version_filter` to apply a
  `VersionMatches` filter to the query. Keep the rest of the query pipeline (search,
  pagination, transaction handling) intact.

- **Remove the `version_filter` parameter** from the function signature entirely. The
  updated signature becomes:

  ```rust
  pub async fn list(
      &self,
      search: Query,
      paginated: Paginated,
      tx: &Transactional<'_>,
  ) -> Result<PaginatedResults<SbomSummary>, AppError>
  ```

- **Why not rename to `_version_filter`?** The implement-task skill's Step 9 "Dead parameter
  detection" guidance is explicit: when removing code that was the only consumer of a
  parameter, the correct fix is removal, not underscore-prefixing. Renaming to
  `_version_filter` silences the compiler warning but leaves dead code in the interface,
  pollutes every call site with an argument that does nothing, and misleads future readers
  into thinking the parameter still has a purpose. See `outputs/parameter-cleanup.md` for
  the full rationale.

### 2. `modules/fundamental/src/sbom/endpoints/list.rs` -- Endpoint handler (call site 1 of 3)

**What changes:**

- Remove the extraction of the `version` query parameter from the HTTP request. This likely
  involves removing a query parameter struct field or a `.query()` / `Query<>` extractor
  related to `version`.

- Update the call to `SbomService::list(...)` to remove the `version_filter` argument.
  The call changes from something like:

  ```rust
  sbom_service.list(search, paginated, &query.version, &tx).await
  ```

  to:

  ```rust
  sbom_service.list(search, paginated, &tx).await
  ```

- If the `version` field was part of a query params struct used only for this parameter,
  also remove the field from the struct. If the struct had other fields, keep the struct and
  only remove the `version` field.

### 3. `modules/search/src/service/mod.rs` -- Search service (call site 2 of 3)

**What changes:**

- The search service calls `SbomService::list` with an empty version filter (likely `""`).
  Remove the empty string argument from the call.

  From:
  ```rust
  sbom_service.list(search, paginated, "", &tx).await
  ```

  To:
  ```rust
  sbom_service.list(search, paginated, &tx).await
  ```

### 4. `tests/api/sbom.rs` -- Integration tests (call site 3 of 3)

**What changes:**

- **Remove or update `test_list_sboms_version_filtered`**: this test exercises the version
  filtering feature that is being removed. Since the feature no longer exists, the test
  should be deleted entirely -- it would test nonexistent behavior.

- **Update other test call sites**: any other tests that call `SbomService::list` directly
  (or hit the endpoint with a `version` query parameter) need updating:
  - Direct calls: remove the `version_filter` argument.
  - HTTP calls: remove the `?version=...` query parameter from request URLs.

- **Verify remaining tests still pass**: after removing the version-specific test and
  updating call sites, run the test suite to confirm no regressions.

## Files NOT Modified

- `modules/fundamental/src/sbom/service/mod.rs` -- Only if `list` is re-exported here,
  but the signature change propagates automatically.
- `modules/fundamental/src/sbom/endpoints/mod.rs` -- Route registration; no change needed
  since the handler function signature for Axum routing is unaffected.
- `common/` -- No changes to shared query helpers or pagination.
- `entity/` -- No schema changes required.

## API Changes

- `GET /api/v2/sbom` -- The `version` query parameter is no longer accepted. Clients
  sending `?version=...` will have the parameter silently ignored (it is no longer extracted).
  This is a backward-compatible removal in the sense that no errors are introduced, but
  clients relying on server-side version filtering will no longer see filtered results.

## Handling the `version_filter` Parameter After Removing Filtering Logic

The key insight is that removing the filtering logic from the method body creates a
**dead parameter** -- `version_filter` would still appear in the signature but have zero
references in the body. The implement-task skill (Step 9, "Dead parameter detection")
prescribes a specific protocol:

1. **Identify**: after removing the `VersionMatches` filter logic, `version_filter` has no
   remaining references in the `list` method body. It is dead.

2. **Remove, do not rename**: the correct action is to remove `version_filter` from the
   function signature entirely. Prefixing with underscore (`_version_filter`) would only
   suppress the compiler warning while leaving the dead parameter in place -- this is
   explicitly called out as the wrong approach in the skill guidance.

3. **Propagate to all call sites**: use `find_referencing_symbols` (Serena) or Grep to
   locate every caller of `SbomService::list`. There are exactly 3 call sites:
   - `modules/fundamental/src/sbom/endpoints/list.rs`
   - `modules/search/src/service/mod.rs`
   - `tests/api/sbom.rs`

   Each call site must have the corresponding argument removed.

4. **Re-run tests**: after all call sites are updated, run `cargo test` (or the
   project-specific test command) to confirm everything compiles and passes.

## Verification Steps

1. **Compile check**: `cargo check` across affected crates to ensure no type errors from
   the signature change.
2. **Test run**: `cargo test -p trustify-fundamental` and `cargo test -p trustify-search`
   (or equivalent crate names resolved via `cargo metadata`) to verify no regressions.
3. **Integration tests**: run tests in `tests/api/sbom.rs` to confirm the endpoint still
   works without the version parameter.
4. **Scope containment**: `git diff --name-only` should show exactly the 4 files listed
   above -- no out-of-scope modifications.
5. **Acceptance criteria check**:
   - The `list` method no longer filters by version.
   - The `version` query parameter is no longer extracted by the endpoint.
   - All 3 call sites compile and pass without `version_filter`.
   - Existing tests that do not depend on version filtering still pass.
