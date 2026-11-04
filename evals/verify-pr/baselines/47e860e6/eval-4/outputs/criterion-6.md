# Criterion 6: Existing package list endpoint tests continue to pass (backward compatible)

**Verdict: PASS**

- The change only adds a field to a JSON response, which is backward compatible for existing clients.
- The endpoint route, signature, and parameters (`offset`, `limit`) are unchanged.
- All CI checks pass on the PR. Any other place that builds a `PackageSummary` without the new field would cause a compile error, and CI would not be green.
- The repository's `tests/api/` lists `sbom.rs`, `advisory.rs`, and `search.rs`. None of them touch the package endpoint, and the PR modifies no existing test files (Test Change Classification: ADDITIVE).
