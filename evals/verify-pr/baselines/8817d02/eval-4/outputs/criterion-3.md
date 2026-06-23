# Criterion 3: The count reflects unique advisories only (no duplicates from multiple SBOMs)

## Verdict: FAIL

## Reasoning

This criterion requires that the `vulnerability_count` field correctly computes the number of unique advisory records affecting a package, specifically handling deduplication across multiple SBOMs. The task's implementation notes describe the required subquery:

```sql
SELECT COUNT(DISTINCT a.id) FROM sbom_package sp
JOIN sbom_advisory sa ON sp.sbom_id = sa.sbom_id
JOIN advisory a ON sa.advisory_id = a.id
WHERE sp.package_id = p.id
```

However, the actual implementation in `modules/fundamental/src/package/service/mod.rs` does not implement this subquery at all. Instead, the vulnerability count is hardcoded to 0:

```rust
vulnerability_count: 0, // TODO: implement subquery
```

The `TODO` comment explicitly acknowledges that the subquery has not been implemented. This means:

1. Packages with vulnerabilities will incorrectly show `vulnerability_count: 0`.
2. Deduplication logic (using `COUNT(DISTINCT ...)`) is entirely absent.
3. The core functional requirement of this feature -- computing the actual vulnerability count -- is not implemented.

The test `test_package_with_vulnerabilities_has_count` expects `vulnerability_count == 3` for a package seeded with 3 advisories, but the hardcoded implementation would return 0, causing the test to fail at runtime. Similarly, `test_vulnerability_count_deduplicates_across_sboms` expects `vulnerability_count == 2` but would receive 0.

## Evidence

- **File:** `modules/fundamental/src/package/service/mod.rs`, diff line 31: `vulnerability_count: 0, // TODO: implement subquery`
- The TODO comment is an explicit admission that the required subquery was not implemented.
- No join logic, no `COUNT(DISTINCT ...)`, no reference to `sbom_package`, `sbom_advisory`, or `advisory` tables anywhere in the diff.
- Tests in `tests/api/package_vuln_count.rs` assert non-zero values (lines 74 and 99) that the hardcoded implementation cannot satisfy.
