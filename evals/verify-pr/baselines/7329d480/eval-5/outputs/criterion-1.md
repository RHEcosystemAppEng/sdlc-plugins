# Criterion 1: Versioned PURLs without qualifiers

**Acceptance Criterion**: `GET /api/v2/purl/recommend?purl=pkg:maven/org.apache/commons-lang3` returns versioned PURLs without qualifiers

**Verdict**: PASS

## Evidence

### Product code -- qualifier stripping in service layer

In `modules/fundamental/src/purl/service/mod.rs`, the response mapping was changed to strip qualifiers before serialization:

```rust
-            .map(|p| PurlSummary {
-                purl: p.to_string(),
+            .map(|p| {
+                let simplified = p.without_qualifiers();
+                PurlSummary {
+                    purl: simplified.to_string(),
+                }
             })
```

The `without_qualifiers()` call produces a PURL with only type, namespace, name, and version -- no qualifier string.

### Product code -- qualifier join removed

In `modules/fundamental/src/purl/service/mod.rs`, the qualifier join was removed from the query:

```rust
-            .filter(purl::Column::Name.eq(&base_purl.name))
-            .join(JoinType::LeftJoin, purl::Relation::PurlQualifier.def());
+            .filter(purl::Column::Name.eq(&base_purl.name));
```

The `JoinType::LeftJoin` on `PurlQualifier` was only needed to include qualifier data in the response; removing it is consistent with the simplified response.

### Test evidence -- assertion on versioned PURL

In `tests/api/purl_recommend.rs`, the `test_recommend_purls_basic` test now asserts the simplified format:

```rust
-    assert_eq!(
-        body.items[0].purl,
-        "pkg:maven/org.apache/commons-lang3@3.12?repository_url=https://repo1.maven.org&type=jar"
-    );
+    assert_eq!(body.items[0].purl, "pkg:maven/org.apache/commons-lang3@3.12");
```

The expected value is a versioned PURL (`@3.12`) without any qualifiers (no `?` suffix). The test hits `GET /api/v2/purl/recommend?purl=pkg:maven/org.apache/commons-lang3`, directly matching the criterion's endpoint.
