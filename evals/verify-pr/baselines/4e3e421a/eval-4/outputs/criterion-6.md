# Criterion 6: Existing package list endpoint tests continue to pass (backward compatible)

**Verdict: PASS**

## What was checked
- CI status: all CI checks pass (per PR state).
- The PR diff, for changes to existing tests.
- The repository structure, for existing package tests.

## Evidence
- The PR modifies no existing tests and deletes none. The only test file is the new
  `tests/api/package_vuln_count.rs`.
- The repository has no dedicated `tests/api/package.rs`. The existing integration tests are `sbom.rs`,
  `advisory.rs`, and `search.rs`, and none of them are touched.
- The change to the API is additive. One new field is added to the response, and no existing field is renamed,
  removed, or retyped. The endpoint signature and route (`GET /api/v2/package`) are unchanged. Existing clients
  that ignore unknown fields are not affected.
- Adding a required struct field would break any other code that builds `PackageSummary` with a struct literal.
  CI passing shows the crate still compiles and the existing tests pass.

## Caveat
The **new** tests in `package_vuln_count.rs` (the vulnerable-package and dedup cases) would fail against the
hardcoded `0`. That is a Criterion 3 problem, not a backward-compatibility regression. Because CI is green even
though those tests would fail, the DB-backed integration tests are probably not run in CI. Backward
compatibility is therefore inferred from the additive diff plus green CI, not from a DB-backed run.
