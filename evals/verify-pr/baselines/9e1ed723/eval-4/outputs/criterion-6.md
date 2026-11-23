# Criterion 6: Existing package list endpoint tests continue to pass (backward compatible)

**Verdict: PASS**

## What was checked
- Whether the change is additive or breaking for `GET /api/v2/package`.
- The existing tests in `tests/api/` (per the repository structure).
- CI status. The eval inputs state that all CI checks pass.

## What was found
- The change only adds a JSON field. No field was removed, renamed, or retyped, the endpoint path and query parameters (`offset`, `limit`) are unchanged, and the `PaginatedResults` wrapper (`total`, `items`) is kept. Existing clients ignore the extra field.
- `PackageService::list` now maps rows into `PackageSummary` explicitly, copying `id`, `name`, `version` and `license` unchanged, so existing field values are preserved.
- The existing test suites (`tests/api/sbom.rs`, `advisory.rs`, `search.rs`) are untouched. The repository has no existing package endpoint test file.
- All CI checks pass.

The criterion is met. However, given the contradiction described under Criterion 3 (new tests that should fail, yet CI passes), it is worth confirming that the integration test suite really runs in CI.
