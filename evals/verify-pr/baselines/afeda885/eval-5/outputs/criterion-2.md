# Criterion 2: Response PURLs do not contain `?` query parameters

## Criterion Text
Response PURLs do not contain `?` query parameters (no qualifiers present)

## Verdict: PASS

## Analysis

The diff demonstrates this criterion is satisfied through both implementation and test coverage.

### Implementation evidence
In `modules/fundamental/src/purl/service/mod.rs`, the mapping pipeline now calls `p.without_qualifiers()` before converting to string. The `without_qualifiers()` method on the `PackageUrl` builder (referenced in the task's Implementation Notes as existing in `common/src/purl.rs`) strips all qualifier key-value pairs from the PURL. Since qualifiers are the portion after the `?` character in a PURL string, the resulting `to_string()` output will not contain a `?` character.

### Test evidence
Multiple test assertions explicitly verify the absence of `?` in response PURLs:

1. In `test_recommend_purls_basic` (modified):
   ```rust
   assert!(!body.items[0].purl.contains('?'));
   assert!(!body.items[1].purl.contains('?'));
   ```

2. In `test_simplified_purl_no_version` (new file):
   ```rust
   assert!(!body.items[0].purl.contains('?'));
   ```

3. In `test_simplified_purl_mixed_types` (new file):
   ```rust
   assert!(!body.items[0].purl.contains("vcs_url"));
   ```

4. In `test_simplified_purl_ordering_preserved` (new file):
   ```rust
   assert!(!body.items[0].purl.contains('?'));
   assert!(!body.items[1].purl.contains('?'));
   ```

The combination of the `without_qualifiers()` call in the service layer and the explicit `contains('?')` assertions in tests provides strong evidence that response PURLs will not contain query parameters.
