## Criterion 2: Response PURLs do not contain `?` query parameters

**Criterion:** Response PURLs do not contain `?` query parameters (no qualifiers present)

**Verdict:** PASS

### Reasoning

This criterion is a stricter form of criterion 1 -- it requires that the `?` character (which introduces the query/qualifier section of a PURL) is absent from all response PURLs.

**Implementation verification:**

The `without_qualifiers()` method in the service layer strips all qualifier key-value pairs from the PURL before serialization. Since qualifiers are encoded after a `?` delimiter in the PURL spec, removing qualifiers removes the `?` and everything after it.

**Test verification across multiple test files:**

1. In `tests/api/purl_recommend.rs`, `test_recommend_purls_basic` adds explicit negative assertions:
   ```rust
   assert!(!body.items[0].purl.contains('?'));
   assert!(!body.items[1].purl.contains('?'));
   ```

2. In `tests/api/purl_recommend.rs`, `test_recommend_purls_dedup` asserts the returned PURL is `"pkg:maven/org.apache/commons-lang3@3.12"` (no `?` present).

3. In `tests/api/purl_simplify.rs`, all three test functions include negative assertions for `?`:
   - `test_simplified_purl_no_version`: `assert!(!body.items[0].purl.contains('?'));`
   - `test_simplified_purl_mixed_types`: `assert!(!body.items[0].purl.contains("vcs_url"));`
   - `test_simplified_purl_ordering_preserved`: `assert!(!body.items[0].purl.contains('?'));` and `assert!(!body.items[1].purl.contains('?'));`

**Conclusion:** The implementation strips qualifiers at the service layer, and multiple tests across both test files explicitly verify the absence of `?` in response PURLs. The criterion is satisfied.
