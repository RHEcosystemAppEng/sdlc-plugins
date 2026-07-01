# Criterion 2: Response PURLs do not contain `?` query parameters (no qualifiers present)

## Verdict: PASS

## Reasoning

### Code evidence

The service layer change in `modules/fundamental/src/purl/service/mod.rs` calls `p.without_qualifiers()` on every PURL result before converting to string. The `without_qualifiers()` method (from the `PackageUrl` builder in `common/src/purl.rs`, as noted in the task's Implementation Notes) strips all qualifier key-value pairs from the PURL. Since qualifiers in the PURL spec are serialized after a `?` character, calling `without_qualifiers()` ensures no `?` appears in the output string.

### Test evidence

Multiple test assertions explicitly verify the absence of `?` in response PURLs:

1. In `tests/api/purl_recommend.rs`, `test_recommend_purls_basic`:
   ```rust
   assert!(!body.items[0].purl.contains('?'));
   assert!(!body.items[1].purl.contains('?'));
   ```

2. In `tests/api/purl_simplify.rs`, `test_simplified_purl_no_version`:
   ```rust
   assert!(!body.items[0].purl.contains('?'));
   ```

3. In `tests/api/purl_simplify.rs`, `test_simplified_purl_mixed_types`:
   ```rust
   assert!(!body.items[0].purl.contains("vcs_url"));
   ```
   This checks that specific qualifier keys are absent from the response.

4. In `tests/api/purl_simplify.rs`, `test_simplified_purl_ordering_preserved`:
   ```rust
   assert!(!body.items[0].purl.contains('?'));
   assert!(!body.items[1].purl.contains('?'));
   ```

### Evidence

- Service layer uses `without_qualifiers()` to strip all qualifiers before serialization
- 6 distinct `contains('?')` or `contains("vcs_url")` negative assertions across test files confirm no qualifiers appear in responses
- The qualifier join was also removed from the query itself (`JoinType::LeftJoin, purl::Relation::PurlQualifier.def()` was deleted), so qualifier data is not even fetched from the database
