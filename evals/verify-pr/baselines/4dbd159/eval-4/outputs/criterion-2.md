# Criterion 2: Packages with no vulnerabilities show vulnerability_count: 0

## Result: PARTIAL PASS (functionally passes by accident, but implementation is incomplete)

## Analysis

The diff in `modules/fundamental/src/package/service/mod.rs` shows:

```rust
+        let items = items.into_iter().map(|p| {
+            PackageSummary {
+                id: p.id,
+                name: p.name,
+                version: p.version,
+                license: p.license,
+                vulnerability_count: 0, // TODO: implement subquery
+            }
+        }).collect();
```

The `vulnerability_count` is hardcoded to `0` for ALL packages -- not just those with no vulnerabilities. This means packages with no vulnerabilities will indeed show `0`, but this is a coincidence of the hardcoded value rather than a correct implementation. The value is `0` regardless of the actual vulnerability state.

The `// TODO: implement subquery` comment explicitly confirms the implementation is incomplete. The task description specifies that the count should be "computed by joining through sbom_package -> sbom_advisory -> advisory tables," and the implementation notes specify a correlated subquery. Neither is present.

While the literal criterion ("packages with no vulnerabilities show vulnerability_count: 0") is technically satisfied, the implementation is a stub. The criterion's intent -- that the system correctly identifies packages without vulnerabilities and returns 0 for them -- is NOT met, because the value would be 0 regardless.

## Evidence

- `vulnerability_count: 0, // TODO: implement subquery` -- hardcoded to 0 for all packages
- No subquery or join logic is present in the diff
- The test `test_package_with_vulnerabilities_has_count` expects `vulnerability_count == 3`, which would FAIL with this implementation

## Verdict

FAIL -- the value is hardcoded to 0, not computed. The criterion is only superficially met for the zero case, and the implementation does not distinguish between packages with and without vulnerabilities.
