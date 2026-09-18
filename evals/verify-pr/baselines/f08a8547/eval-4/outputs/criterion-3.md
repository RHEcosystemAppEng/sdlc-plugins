# Criterion 3: The count reflects unique advisories only (no duplicates from multiple SBOMs)

## Verdict: FAIL

## Analysis

This criterion requires that `vulnerability_count` accurately reflects the number of unique vulnerability advisories affecting each package, computed by joining through `sbom_package`, `sbom_advisory`, and `advisory` tables with `COUNT(DISTINCT a.id)` deduplication.

The PR diff shows that the `vulnerability_count` field is hardcoded to `0` in `modules/fundamental/src/package/service/mod.rs`:

```rust
vulnerability_count: 0, // TODO: implement subquery
```

The `// TODO: implement subquery` comment explicitly acknowledges that the actual advisory count computation has not been implemented. The value `0` is returned for every package regardless of how many advisories affect it. This means:

1. Packages with actual vulnerabilities will incorrectly report a count of 0.
2. There is no subquery joining through `sbom_package` -> `sbom_advisory` -> `advisory`.
3. The `COUNT(DISTINCT a.id)` deduplication logic specified in the Implementation Notes does not exist.
4. The test `test_package_with_vulnerabilities_has_count` (which asserts `vulnerability_count == 3`) would fail at runtime because the hardcoded value is always 0.
5. The test `test_vulnerability_count_deduplicates_across_sboms` (which asserts `vulnerability_count == 2`) would also fail at runtime for the same reason.

The criterion explicitly requires that the count "reflects unique advisories only" -- a hardcoded zero does not reflect anything.

## Evidence

- File: `modules/fundamental/src/package/service/mod.rs` -- line contains `vulnerability_count: 0, // TODO: implement subquery`
- No subquery exists in the diff to compute advisory counts
- No join through `sbom_package`, `sbom_advisory`, or `advisory` tables
- Test `test_package_with_vulnerabilities_has_count` expects count of 3 but implementation returns 0
- Test `test_vulnerability_count_deduplicates_across_sboms` expects count of 2 but implementation returns 0
