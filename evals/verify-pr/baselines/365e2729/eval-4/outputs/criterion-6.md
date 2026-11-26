# Criterion 6: Existing package list endpoint tests continue to pass (backward compatible)

**Verdict: PASS**

## What was checked
- The repository structure: `tests/api/` contains `sbom.rs`, `advisory.rs` and `search.rs`. There is no existing package endpoint test file.
- The type of change made to the API response.
- CI status: the task inputs state that all CI checks pass.

## What was found
- The change only adds a field to the response. No existing fields are renamed, removed or retyped, and the endpoint path, query parameters (`offset`, `limit`) and pagination wrapper are unchanged. Clients that ignore unknown fields are not affected.
- No existing test files are modified or deleted.
- All CI checks are reported as passing, so the existing test suite still passes.

## Note
No package-specific list tests existed before this PR, so this criterion is mostly about the rest of the suite. The new tests in `package_vuln_count.rs` probably do not run (see Criterion 3). That does not affect this criterion, which is only about existing tests.
