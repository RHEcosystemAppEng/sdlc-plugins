# Criterion 2: No query parameters in response PURLs

**Acceptance Criterion**: Response PURLs do not contain `?` query parameters (no qualifiers present)

**Verdict**: PASS

## Evidence

### Product code -- qualifiers stripped before serialization

In `modules/fundamental/src/purl/service/mod.rs`:

```rust
+                let simplified = p.without_qualifiers();
+                PurlSummary {
+                    purl: simplified.to_string(),
+                }
```

`without_qualifiers()` produces a PURL string that will not contain a `?` character, since qualifiers are the only component that introduces `?` in a PURL.

### Test evidence -- explicit `?` absence assertions in purl_recommend.rs

In `tests/api/purl_recommend.rs`, the modified `test_recommend_purls_basic` test adds explicit assertions that `?` is absent:

```rust
+    assert!(!body.items[0].purl.contains('?'));
+    assert!(!body.items[1].purl.contains('?'));
```

These assertions directly verify the criterion: no PURL in the response contains the `?` character that would indicate qualifier presence.

### Test evidence -- `?` absence assertions in purl_simplify.rs

In the new `tests/api/purl_simplify.rs`, multiple tests assert the absence of `?`:

`test_simplified_purl_no_version`:
```rust
    assert!(!body.items[0].purl.contains('?'));
```

`test_simplified_purl_ordering_preserved`:
```rust
    assert!(!body.items[0].purl.contains('?'));
    assert!(!body.items[1].purl.contains('?'));
```

`test_simplified_purl_mixed_types`:
```rust
    assert!(!body.items[0].purl.contains("vcs_url"));
```

This assertion indirectly confirms no qualifiers are present by checking for a specific qualifier key that was seeded in the test data.
