# Criterion 6: Existing package list endpoint tests continue to pass (backward compatible)

**Status**: PASS (with caveat)

## Evidence

The diff does not modify or remove any existing test files. The only test file change is the addition of a new file `tests/api/package_vuln_count.rs`. The existing endpoint behavior is preserved -- the `list` method signature and route registration remain the same.

The endpoint in `list.rs` still calls `PackageService::new(&db).list(params.offset, params.limit)` with identical parameters. The only change to that file is an added comment.

Adding a new field to `PackageSummary` is an additive, backward-compatible change for JSON serialization -- existing consumers that do not expect the field will simply ignore it.

**Caveat**: If existing tests deserialize the full `PackageSummary` struct, they would need to account for the new field. However, since CI checks are reported as passing, this does not appear to be an issue.
