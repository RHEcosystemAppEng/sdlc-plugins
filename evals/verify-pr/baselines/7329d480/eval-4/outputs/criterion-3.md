# Criterion 3: The count reflects unique advisories only (no duplicates from multiple SBOMs)

## Verdict: FAIL

## Criterion Text
The count reflects unique advisories only (no duplicates from multiple SBOMs)

## Analysis

The PR diff for `modules/fundamental/src/package/service/mod.rs` shows:

```rust
+                vulnerability_count: 0, // TODO: implement subquery
```

The `vulnerability_count` field is hardcoded to `0` for every package, regardless of how many advisories actually affect the package. The correlated subquery specified in the Implementation Notes has not been implemented:

```sql
SELECT COUNT(DISTINCT a.id) FROM sbom_package sp
JOIN sbom_advisory sa ON sp.sbom_id = sa.sbom_id
JOIN advisory a ON sa.advisory_id = a.id
WHERE sp.package_id = p.id
```

Because the subquery is not implemented:
- Packages with vulnerabilities will incorrectly show `vulnerability_count: 0`
- The count does not reflect actual advisory data at all
- The `COUNT(DISTINCT a.id)` deduplication logic is absent
- The `// TODO: implement subquery` comment explicitly acknowledges this is incomplete

The integration test `test_package_with_vulnerabilities_has_count` (which seeds 3 advisories and asserts `vulnerability_count == 3`) would fail at runtime because the hardcoded 0 would never match the expected count of 3. Similarly, `test_vulnerability_count_deduplicates_across_sboms` would fail because it expects `vulnerability_count == 2` for deduplicated advisories.

## Evidence
- **File:** `modules/fundamental/src/package/service/mod.rs`
- **Line:** `vulnerability_count: 0, // TODO: implement subquery`
- **Missing implementation:** The correlated subquery joining `sbom_package` -> `sbom_advisory` -> `advisory` is not present
- **Impact:** All packages return vulnerability_count = 0 regardless of actual advisory associations
- **TODO comment:** The developer explicitly marked this as incomplete
- **Test expectation mismatch:** Tests assert non-zero counts (3 and 2) that the hardcoded 0 cannot satisfy
