# Criterion 2: Packages with no vulnerabilities show vulnerability_count: 0

## Criterion Text
Packages with no vulnerabilities show `vulnerability_count: 0`

## Verdict: PASS (trivially, due to hardcoded value)

## Reasoning

The PR diff for `modules/fundamental/src/package/service/mod.rs` shows the `vulnerability_count` field being set:

```rust
+                vulnerability_count: 0, // TODO: implement subquery
```

All packages will show `vulnerability_count: 0` because the value is hardcoded to 0 for every package. This means packages with no vulnerabilities will indeed show 0 -- but so will packages WITH vulnerabilities, because the actual subquery is not implemented.

While this criterion technically passes (packages with no vulnerabilities do return 0), the hardcoded value is a significant concern. The TODO comment explicitly acknowledges the subquery is not implemented. The criterion is satisfied in the narrow sense, but only because the implementation is incomplete -- it does not correctly compute the count for any package.

## Evidence
- File: `modules/fundamental/src/package/service/mod.rs`
- The `vulnerability_count` is hardcoded to `0` with a `// TODO: implement subquery` comment
- This means all packages return 0, regardless of actual vulnerability count
- The criterion is technically satisfied for the no-vulnerability case, but the implementation is degenerate
