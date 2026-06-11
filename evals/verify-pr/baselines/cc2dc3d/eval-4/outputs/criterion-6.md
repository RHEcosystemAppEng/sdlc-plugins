# Criterion 6: Existing package list endpoint tests continue to pass (backward compatible)

## Verdict: PASS (conditional)

## Evidence

The diff shows changes to three existing files and adds one new test file:

1. **`modules/fundamental/src/package/model/summary.rs`** -- adds a new field. This is additive; existing fields are unchanged.
2. **`modules/fundamental/src/package/service/mod.rs`** -- the mapping now constructs `PackageSummary` with the new field. Existing fields (`id`, `name`, `version`, `license`) are preserved.
3. **`modules/fundamental/src/package/endpoints/list.rs`** -- only a comment change, no functional modification.
4. **`tests/api/package_vuln_count.rs`** -- new test file, does not modify existing tests.

The repository structure shows existing tests in `tests/api/` for `sbom.rs`, `advisory.rs`, and `search.rs`. There are no pre-existing package-specific test files visible in the tree.

## Reasoning

The changes are additive: a new field is added to the struct and populated in the service layer. No existing fields are removed or renamed. The endpoint behavior is unchanged apart from the additional field in the JSON response. Adding a new field to a JSON response is generally backward compatible (consumers should ignore unknown fields). CI checks are reported as passing, which supports this assessment.

This is marked PASS conditional on CI confirmation, which the eval scenario states passes.
