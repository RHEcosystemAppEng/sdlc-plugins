# Criterion 2: Packages with no vulnerabilities show vulnerability_count: 0

## Criterion Text

> Packages with no vulnerabilities show `vulnerability_count: 0`

## Verdict: PASS (trivially satisfied)

## Reasoning

The PR diff for `modules/fundamental/src/package/service/mod.rs` shows that `vulnerability_count` is hardcoded to `0` for all packages:

```rust
+            vulnerability_count: 0, // TODO: implement subquery
```

Because every package receives `vulnerability_count: 0` regardless of its actual vulnerability state, packages with no vulnerabilities will indeed show `vulnerability_count: 0`. This criterion is technically satisfied.

However, this is only trivially true because the value is hardcoded rather than computed. The same hardcoded value also means that packages WITH vulnerabilities will incorrectly show 0. This is not a violation of this specific criterion (which only speaks to the no-vulnerability case), but it indicates incomplete implementation that affects criterion 3.

A corresponding test exists in `tests/api/package_vuln_count.rs`:

```rust
async fn test_package_without_vulnerabilities_has_zero_count(ctx: &TestContext) {
    let pkg_id = ctx.seed_package("pkg-safe", "MIT").await;
    // ...
    assert_eq!(pkg.vulnerability_count, 0);
}
```

This test would pass given the hardcoded 0, but it would pass for the wrong reason (hardcoded value rather than computed result).

## Evidence

- **File:** `modules/fundamental/src/package/service/mod.rs`, line with `vulnerability_count: 0, // TODO: implement subquery`
- **Test file:** `tests/api/package_vuln_count.rs`, function `test_package_without_vulnerabilities_has_zero_count`
- **Status:** Criterion narrowly satisfied, but implementation is incomplete (see criterion 3)
