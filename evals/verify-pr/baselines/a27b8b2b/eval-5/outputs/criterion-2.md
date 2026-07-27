# Criterion 2: Response PURLs do not contain `?` query parameters (no qualifiers present)

## Verdict: PASS

## Analysis

This criterion is a stricter formulation of Criterion 1, verifying the absence of qualifier syntax in response PURLs.

**Implementation evidence:**
- In `modules/fundamental/src/purl/service/mod.rs`, the `without_qualifiers()` method is called on each PURL before serialization. Per the task's Implementation Notes, the `PackageUrl` builder in `common/src/purl.rs` supports constructing PURLs without qualifiers, and `without_qualifiers()` produces a PURL string that lacks the `?key=value` suffix.

**Test evidence:**
- `test_recommend_purls_basic` includes two explicit negative assertions:
  ```rust
  assert!(!body.items[0].purl.contains('?'));
  assert!(!body.items[1].purl.contains('?'));
  ```
  These directly verify that the `?` character (which introduces query parameters/qualifiers in PURL syntax) is absent from response PURLs.

- `test_simplified_purl_no_version` (new file) also asserts `!body.items[0].purl.contains('?')`.
- `test_simplified_purl_mixed_types` asserts `!body.items[0].purl.contains("vcs_url")`, verifying specific qualifier keys are absent.
- `test_simplified_purl_ordering_preserved` asserts `!body.items[0].purl.contains('?')` and `!body.items[1].purl.contains('?')`.

The implementation removes qualifier data at the service layer, and multiple tests across both test files confirm the absence of query parameters in the response.
