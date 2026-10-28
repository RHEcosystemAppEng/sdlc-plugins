# Criterion 3: The count reflects unique advisories only (no duplicates from multiple SBOMs)

## Verdict: FAIL

## Reasoning

The implementation in `modules/fundamental/src/package/service/mod.rs` hardcodes `vulnerability_count` to `0` for every package:

```rust
vulnerability_count: 0, // TODO: implement subquery
```

The TODO comment explicitly acknowledges that the subquery has not been implemented. The task's implementation notes specify the required correlated subquery:

```sql
SELECT COUNT(DISTINCT a.id) FROM sbom_package sp
JOIN sbom_advisory sa ON sp.sbom_id = sa.sbom_id
JOIN advisory a ON sa.advisory_id = a.id
WHERE sp.package_id = p.id
```

This subquery is entirely absent from the diff. The count does not reflect unique advisories -- it does not reflect any advisories at all. It is a static zero regardless of the package's actual vulnerability status. This is a critical defect: the core feature (computing vulnerability counts) is not implemented.

Additionally, the test `test_package_with_vulnerabilities_has_count` asserts `vulnerability_count == 3` and `test_vulnerability_count_deduplicates_across_sboms` asserts `vulnerability_count == 2`, but since the implementation always returns 0, these tests would fail at runtime despite CI reportedly passing.
