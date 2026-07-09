## Criterion 2: Response PURLs do not contain `?` query parameters (no qualifiers present)

**Verdict: PASS**

### Reasoning

The PR ensures that response PURLs contain no qualifier parameters by calling `p.without_qualifiers()` in the service layer before serializing the PURL to a string. Since qualifiers are appended after a `?` character in PURL syntax, removing qualifiers guarantees the absence of `?` in the output.

Multiple tests explicitly assert this behavior using `contains('?')` checks:

In `tests/api/purl_recommend.rs`, the updated `test_recommend_purls_basic`:
```rust
assert!(!body.items[0].purl.contains('?'));
assert!(!body.items[1].purl.contains('?'));
```

In the new file `tests/api/purl_simplify.rs`:
- `test_simplified_purl_no_version` asserts `!body.items[0].purl.contains('?')`
- `test_simplified_purl_mixed_types` asserts `!body.items[0].purl.contains("vcs_url")`
- `test_simplified_purl_ordering_preserved` asserts `!body.items[0].purl.contains('?')` and `!body.items[1].purl.contains('?')`

These assertions directly verify the criterion across multiple PURL types and scenarios, confirming that no `?` query parameters appear in any response PURL.
