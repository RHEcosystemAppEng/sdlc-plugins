# Criterion 2: Response PURLs do not contain ? query parameters (no qualifiers present)

## Verdict: PASS

## Reasoning

Multiple test functions explicitly assert the absence of the `?` character in response PURLs, which is the delimiter that introduces qualifier query parameters in PURL syntax.

**In `tests/api/purl_recommend.rs`** (`test_recommend_purls_basic`):
```rust
assert!(!body.items[0].purl.contains('?'));
assert!(!body.items[1].purl.contains('?'));
```

These assertions were added alongside the updated equality check. The test seeds PURLs that do have qualifiers in the database (`?repository_url=https://repo1.maven.org&type=jar`), so these assertions confirm the qualifiers are actively stripped rather than simply absent from the seed data.

**In `tests/api/purl_simplify.rs`**:
- `test_simplified_purl_no_version`: `assert!(!body.items[0].purl.contains('?'));`
- `test_simplified_purl_mixed_types`: `assert!(!body.items[0].purl.contains("vcs_url"));` (checks specific qualifier key absence)
- `test_simplified_purl_ordering_preserved`: `assert!(!body.items[0].purl.contains('?'));` and `assert!(!body.items[1].purl.contains('?'));`

The production code achieves this via the `without_qualifiers()` method call in the service layer, which constructs a new PURL object without qualifier key-value pairs. The `?` absence checks in tests provide a safety net beyond exact string matching, ensuring no qualifier leakage regardless of qualifier content.
