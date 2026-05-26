# Criterion 2: Response PURLs do not contain `?` query parameters

## Criterion
Response PURLs do not contain `?` query parameters (no qualifiers present).

## Verdict: PASS

## Reasoning

The PR ensures that no response PURL contains the `?` character (which introduces qualifier parameters in PURL syntax) through two mechanisms:

1. **Service-layer stripping:** In `modules/fundamental/src/purl/service/mod.rs`, the `without_qualifiers()` method is called on each PURL entity before serialization. This method, as documented in the task's Implementation Notes, constructs PURLs without qualifier components, meaning the serialized string will never contain `?` followed by query parameters.

2. **Explicit test assertions:** The updated tests include explicit assertions that the `?` character is absent from response PURLs:

   In `test_recommend_purls_basic`:
   ```rust
   assert!(!body.items[0].purl.contains('?'));
   assert!(!body.items[1].purl.contains('?'));
   ```

   In `test_recommend_purls_dedup`:
   ```rust
   assert_eq!(body.items[0].purl, "pkg:maven/org.apache/commons-lang3@3.12");
   ```
   (This string contains no `?`, confirming no qualifiers.)

   In `tests/api/purl_simplify.rs`, multiple tests assert the absence of qualifiers:
   ```rust
   assert!(!body.items[0].purl.contains('?'));        // test_simplified_purl_no_version
   assert!(!body.items[0].purl.contains("vcs_url"));  // test_simplified_purl_mixed_types
   assert!(!body.items[0].purl.contains('?'));         // test_simplified_purl_ordering_preserved
   assert!(!body.items[1].purl.contains('?'));
   ```

The code change removes qualifier inclusion at the service layer, and multiple tests explicitly verify that the `?` character does not appear in response PURLs. This criterion is satisfied.
