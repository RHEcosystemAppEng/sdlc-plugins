# Criterion 3: The count reflects unique advisories only (no duplicates from multiple SBOMs)

## Verdict: FAIL

## Reasoning

This criterion requires that `vulnerability_count` be computed by counting unique (deduplicated) advisory records linked to each package through the SBOM join tables. The task description specifies a correlated subquery:

```sql
SELECT COUNT(DISTINCT a.id) FROM sbom_package sp
  JOIN sbom_advisory sa ON sp.sbom_id = sa.sbom_id
  JOIN advisory a ON sa.advisory_id = a.id
  WHERE sp.package_id = p.id
```

The actual implementation in `modules/fundamental/src/package/service/mod.rs` does NOT implement this subquery. Instead, the vulnerability count is hardcoded to zero:

```rust
vulnerability_count: 0, // TODO: implement subquery
```

The `// TODO: implement subquery` comment explicitly acknowledges that this logic has not been implemented. The count does not reflect unique advisories because it does not reflect advisories at all -- it is a static constant.

Furthermore, the test `test_vulnerability_count_deduplicates_across_sboms` seeds a package with 2 unique advisories shared across 3 SBOMs and asserts `vulnerability_count == 2`. With the hardcoded value of 0, this test would fail. Similarly, `test_package_with_vulnerabilities_has_count` seeds 3 advisories and expects count 3, which would also fail against the implementation.

This is the core defect in this PR: the feature's business logic is entirely missing. The field exists structurally but is non-functional.

This criterion FAILS.
