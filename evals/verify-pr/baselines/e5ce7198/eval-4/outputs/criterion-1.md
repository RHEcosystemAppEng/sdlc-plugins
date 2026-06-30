## Criterion 1: `PackageSummary` includes a `vulnerability_count: i64` field

### Result: PASS

### Evidence

The diff in `modules/fundamental/src/package/model/summary.rs` shows:

```diff
@@ -8,6 +8,8 @@ pub struct PackageSummary {
     pub name: String,
     pub version: String,
     pub license: String,
+    /// Number of known vulnerability advisories affecting this package.
+    pub vulnerability_count: i64,
 }
```

The field `vulnerability_count` is added with type `i64` to the `PackageSummary` struct. The field includes a doc comment explaining its purpose. This exactly matches the acceptance criterion.

### Conclusion

PASS -- the field is present with the correct type and appropriate documentation.
