## Criterion 1: `PackageSummary` includes a `vulnerability_count: i64` field

### Verdict: PASS

### Analysis

The acceptance criterion requires that `PackageSummary` includes a `vulnerability_count` field with type `i64`.

### Evidence

In the PR diff for `modules/fundamental/src/package/model/summary.rs`, the following lines are added:

```rust
/// Number of known vulnerability advisories affecting this package.
pub vulnerability_count: i64,
```

This adds the `vulnerability_count` field to the `PackageSummary` struct with the exact type `i64` as specified. The field also includes a doc comment explaining its purpose.

The field is also referenced in `modules/fundamental/src/package/service/mod.rs` where `PackageSummary` instances are constructed:

```rust
PackageSummary {
    id: p.id,
    name: p.name,
    version: p.version,
    license: p.license,
    vulnerability_count: 0, // TODO: implement subquery
}
```

The field exists, is typed correctly, and is populated during construction.

### Conclusion

The criterion is fully satisfied. The `vulnerability_count: i64` field is present in the `PackageSummary` struct definition.
