# Criterion 3: The count reflects unique advisories only (no duplicates from multiple SBOMs)

## Verdict: FAIL

## Reasoning

This criterion requires that the `vulnerability_count` field computes the number of unique advisories affecting each package by joining through the `sbom_package`, `sbom_advisory`, and `advisory` tables, and deduplicating advisories that appear across multiple SBOMs.

The implementation in `modules/fundamental/src/package/service/mod.rs` does NOT implement this:

```rust
vulnerability_count: 0, // TODO: implement subquery
```

The value is hardcoded to `0` with an explicit `// TODO: implement subquery` comment. No correlated subquery is implemented. No join through `sbom_package -> sbom_advisory -> advisory` is present. No `COUNT(DISTINCT a.id)` or equivalent deduplication logic exists.

The task's Implementation Notes specified: "Use a correlated subquery to count advisories: `SELECT COUNT(DISTINCT a.id) FROM sbom_package sp JOIN sbom_advisory sa ON sp.sbom_id = sa.sbom_id JOIN advisory a ON sa.advisory_id = a.id WHERE sp.package_id = p.id`". This subquery was never implemented.

Furthermore, the test `test_vulnerability_count_deduplicates_across_sboms` asserts that `vulnerability_count == 2` for a package seeded with shared advisories. Since the implementation always returns 0, this test would fail at runtime, contradicting the stated CI pass status.

Similarly, `test_package_with_vulnerabilities_has_count` asserts `vulnerability_count == 3`, which would also fail since the implementation always returns 0.

This is a critical implementation gap -- the core functional requirement of the task is not implemented.
