# Parameter Cleanup: Removing Dead Parameters and Updating Call Sites

## The Problem

Task TC-9207 removes the version-based filtering logic from `SbomService::list`. After
removing the filter code from the method body, the `version_filter: &str` parameter remains
in the function signature but is no longer referenced anywhere in the method body. This
makes it a **dead parameter**.

## Why Removal, Not Underscore-Prefixing

The implement-task skill (Step 9, "Dead parameter detection") is explicit:

> "The correct fix is removal, not renaming."

Prefixing with underscore (`_version_filter`) is the wrong approach for several reasons:

1. **It hides the problem instead of fixing it.** The underscore prefix tells the Rust
   compiler "I know this is unused, stop warning me." But the parameter is not merely
   temporarily unused -- the feature it supported has been deliberately removed. Silencing
   the warning preserves dead code in a public API.

2. **It pollutes every call site.** All 3 callers would continue passing a value that is
   discarded on arrival. This wastes reader attention and invites confusion: "why is this
   value being passed if nothing uses it?"

3. **It creates maintenance debt.** Future developers will encounter the parameter, wonder
   what it does, search for its usage in the method body, find nothing, and then need to
   trace history to understand it was intentionally dead-coded. Removing it eliminates this
   entirely.

4. **It violates interface cleanliness.** A public API method should only accept parameters
   it uses. Dead parameters in public interfaces are a code smell that suggests incomplete
   refactoring.

The underscore-prefix convention exists for parameters required by a trait signature or
callback contract where the implementation does not need the value but cannot change the
signature. That does not apply here -- `SbomService::list` is a concrete method whose
signature we control.

## Dead Parameter Detection Process

Following the skill's Step 9 guidance:

### Step 1: Identify candidates

After removing the `VersionMatches` filter logic from the `list` method body, run
`git diff` on `modules/fundamental/src/sbom/service/sbom.rs`. The removed lines contain
the only references to `version_filter` in the function body. The parameter is now dead.

### Step 2: Detect dead parameters

Verify that `version_filter` has zero remaining references in the function body. In Rust,
the compiler would emit warning `unused_variable` for `version_filter` (or the code would
not compile if using `#[deny(unused_variables)]`). This confirms the parameter is dead.

### Step 3: Remove the dead parameter

Remove `version_filter: &str` from the `list` method signature:

**Before:**
```rust
pub async fn list(
    &self,
    search: Query,
    paginated: Paginated,
    version_filter: &str,
    tx: &Transactional<'_>,
) -> Result<PaginatedResults<SbomSummary>, AppError>
```

**After:**
```rust
pub async fn list(
    &self,
    search: Query,
    paginated: Paginated,
    tx: &Transactional<'_>,
) -> Result<PaginatedResults<SbomSummary>, AppError>
```

### Step 4: Find and update all call sites

Use `find_referencing_symbols` on `SbomService::list` (via the `serena_backend` Serena
instance) or Grep for `\.list(` across the repository to locate every caller. There are
exactly 3 call sites:

#### Call site 1: `modules/fundamental/src/sbom/endpoints/list.rs`

This is the REST endpoint handler. It extracts the `version` query parameter from the
HTTP request and passes it to `SbomService::list`.

**Changes required:**
- Remove the `version` field from the query parameter extraction (likely a struct field
  in a `Query<ListParams>` or similar Axum extractor).
- Remove the `version_filter` argument from the `list()` call.

**Before (conceptual):**
```rust
let results = sbom_service
    .list(search, paginated, &params.version, &tx)
    .await?;
```

**After:**
```rust
let results = sbom_service
    .list(search, paginated, &tx)
    .await?;
```

Since the endpoint no longer needs the `version` query parameter at all, also remove:
- The `version` field from the query params struct (if it was the only field using it).
- Any deserialization or default logic for the version field.

#### Call site 2: `modules/search/src/service/mod.rs`

The search service calls `SbomService::list` with an empty string for `version_filter`,
since full-text search does not use version filtering.

**Before:**
```rust
sbom_service.list(search, paginated, "", &tx).await
```

**After:**
```rust
sbom_service.list(search, paginated, &tx).await
```

This is a straightforward argument removal -- no other changes needed in this file.

#### Call site 3: `tests/api/sbom.rs`

Integration tests that call `SbomService::list` or hit `GET /api/v2/sbom?version=...`.

**Changes required:**

- **Delete `test_list_sboms_version_filtered`** entirely. This test exercises the version
  filtering feature that is being removed. Keeping it and adapting it would test behavior
  that no longer exists.

- **Update other tests** that call `list()` directly: remove the `version_filter` argument.

- **Update HTTP-level tests**: if any test constructs a request URL with `?version=...`,
  remove the query parameter from the URL. These tests should still pass since the endpoint
  now ignores the parameter (it is simply not extracted).

### Step 5: Re-run tests

After updating all 3 call sites, re-run the test suite to confirm nothing broke:

```bash
cargo test -p <fundamental-crate-name>
cargo test -p <search-crate-name>
```

Where the crate names are resolved via `cargo metadata --no-deps --format-version 1` from
the workspace root (per the skill's Rust-specific guidance -- do not guess crate names from
directory structure or `Cargo.toml` filenames).

Also run any integration tests:

```bash
cargo test --test sbom
```

(or the equivalent target for `tests/api/sbom.rs`).

If `CONVENTIONS.md` contains CI check commands, run those as well before committing.

**All tests must pass before proceeding to commit.** If any test fails, diagnose and fix
the failure. If a test fails 3 times with the same error, stop and ask the user for guidance.

## Trait/Interface Consideration

The skill guidance includes a special case: "For trait/interface methods, only remove if no
implementation references the parameter." In this case, `SbomService::list` is a concrete
method on a struct, not a trait method. There is no trait contract requiring the parameter.
Therefore, removal is unconditionally safe once all call sites are updated.

If `list` were defined in a trait (e.g., `trait SbomRepository`), we would need to:
1. Check all trait implementations to verify none of them use `version_filter`.
2. Only then remove it from the trait definition and all implementations.

This does not apply here, but it is worth noting for completeness.

## Summary

| Action | File | Change |
|--------|------|--------|
| Remove filter logic | `modules/fundamental/src/sbom/service/sbom.rs` | Delete `VersionMatches` filter code from method body |
| Remove parameter | `modules/fundamental/src/sbom/service/sbom.rs` | Delete `version_filter: &str` from signature |
| Update call site 1 | `modules/fundamental/src/sbom/endpoints/list.rs` | Remove version query extraction and argument |
| Update call site 2 | `modules/search/src/service/mod.rs` | Remove empty string argument |
| Update call site 3 | `tests/api/sbom.rs` | Delete version filter test, update other test calls |
| Verify | All affected crates | Re-run `cargo test` to confirm no regressions |
