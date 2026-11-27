# Criterion 3: The count reflects unique advisories only (no duplicates from multiple SBOMs)

**Verdict: FAIL**

## Reasoning

To meet this criterion the service must count distinct advisories by joining `sbom_package` → `sbom_advisory` → `advisory`. The task's Implementation Notes give the exact query: `SELECT COUNT(DISTINCT a.id) FROM sbom_package sp JOIN sbom_advisory sa ON sp.sbom_id = sa.sbom_id JOIN advisory a ON sa.advisory_id = a.id WHERE sp.package_id = p.id`.

The PR implements no count at all.

## Evidence

- `modules/fundamental/src/package/service/mod.rs` sets `vulnerability_count: 0, // TODO: implement subquery` for every package.
- The diff has no subquery, no `COUNT(DISTINCT ...)`, no join, and no reference to the `sbom_package`, `sbom_advisory`, or `advisory` entities (`entity/src/sbom_package.rs`, `entity/src/sbom_advisory.rs`, `entity/src/advisory.rs`).
- The only change in `modules/fundamental/src/package/endpoints/list.rs` is a trailing comment (`// vulnerability_count now included in response`). It changes no behavior.
- The PR's own tests contradict the implementation:
  - `test_package_with_vulnerabilities_has_count` seeds 3 advisories and asserts `vulnerability_count == 3`, but the service returns `0`.
  - `test_vulnerability_count_deduplicates_across_sboms` asserts `vulnerability_count == 2`, but the service returns `0`.
- The test file also looks unable to compile. It uses `PaginatedResults`, `PackageSummary`, and `#[test_context]` without importing them, and it calls seed helpers (`seed_package_with_advisories`, `seed_package_with_shared_advisories`, `seed_package`) that the PR does not define. CI is reported green, so these tests are most likely not being compiled or run. A green CI therefore says nothing about this criterion.

## Required fix

Replace the hardcoded `0` with the correlated `COUNT(DISTINCT a.id)` subquery, and make sure `tests/api/package_vuln_count.rs` compiles and runs in CI.
