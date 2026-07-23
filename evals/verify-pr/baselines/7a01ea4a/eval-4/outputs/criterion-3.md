# Criterion 3: The count reflects unique advisories only (no duplicates from multiple SBOMs)

## Verdict: FAIL

## Analysis

This criterion requires that `vulnerability_count` be computed by counting unique (distinct) advisories affecting each package, ensuring that advisories shared across multiple SBOMs are not double-counted.

The implementation in `modules/fundamental/src/package/service/mod.rs` does NOT implement the required subquery. Instead, the value is hardcoded to 0:

```rust
vulnerability_count: 0, // TODO: implement subquery
```

The task's Implementation Notes specify the required correlated subquery:

```sql
SELECT COUNT(DISTINCT a.id) FROM sbom_package sp
JOIN sbom_advisory sa ON sp.sbom_id = sa.sbom_id
JOIN advisory a ON sa.advisory_id = a.id
WHERE sp.package_id = p.id
```

This subquery (or an equivalent ORM-based query using SeaORM) is not present anywhere in the PR diff. The `COUNT(DISTINCT a.id)` is the key element that ensures deduplication across SBOMs, and it is entirely absent.

Because the count is hardcoded to 0, it does not "reflect" unique advisories at all -- it reflects nothing. A package with 5 distinct advisories would incorrectly show `vulnerability_count: 0`.

The test `test_vulnerability_count_deduplicates_across_sboms` seeds a package with 2 unique advisories shared across 3 SBOMs and asserts `vulnerability_count == 2`. With the current hardcoded-to-0 implementation, this test would fail (asserting 2 == 0). Similarly, `test_package_with_vulnerabilities_has_count` seeds 3 advisories and asserts `vulnerability_count == 3`, which would also fail.

This represents the core functional gap in the PR: the vulnerability counting logic is not implemented.

## Evidence

- File: `modules/fundamental/src/package/service/mod.rs` -- `vulnerability_count: 0, // TODO: implement subquery`
- No subquery joining `sbom_package`, `sbom_advisory`, and `advisory` tables exists in the diff
- No `COUNT(DISTINCT ...)` or equivalent deduplication logic is present
- The `// TODO` comment explicitly acknowledges the missing implementation
- Tests `test_package_with_vulnerabilities_has_count` and `test_vulnerability_count_deduplicates_across_sboms` would fail with the current code (asserting non-zero counts against a hardcoded 0)
