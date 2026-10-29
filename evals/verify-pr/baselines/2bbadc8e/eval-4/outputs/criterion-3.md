# Criterion 3: The count reflects unique advisories only (no duplicates from multiple SBOMs)

## Verdict: FAIL

## Analysis

The PR diff for `modules/fundamental/src/package/service/mod.rs` shows:

```rust
vulnerability_count: 0, // TODO: implement subquery
```

The `vulnerability_count` is hardcoded to `0` for every package. The required subquery to count unique advisories — `SELECT COUNT(DISTINCT a.id) FROM sbom_package sp JOIN sbom_advisory sa ON sp.sbom_id = sa.sbom_id JOIN advisory a ON sa.advisory_id = a.id WHERE sp.package_id = p.id` — is not implemented.

The TODO comment confirms this is an intentional placeholder, not a completed implementation. Since the count does not reflect any advisories at all (let alone unique ones), this criterion is not satisfied.

The test file `tests/api/package_vuln_count.rs` includes a test (`test_vulnerability_count_deduplicates_across_sboms`) that asserts `vulnerability_count == 2` for a package with shared advisories — this test would fail at runtime because the service always returns 0.

## Evidence

- **File:** `modules/fundamental/src/package/service/mod.rs`
- **Hardcoded value:** `vulnerability_count: 0` with `// TODO: implement subquery`
- **No subquery exists** anywhere in the diff to count advisories
- **Test would fail:** `test_package_with_vulnerabilities_has_count` expects `vulnerability_count == 3`, but the service returns 0
- **Test would fail:** `test_vulnerability_count_deduplicates_across_sboms` expects `vulnerability_count == 2`, but the service returns 0
- The implementation is incomplete — the field exists but its value is never computed
