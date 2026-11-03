# Criterion 1 — PASS

**Criterion:** `GET /api/v2/purl/recommend?purl=pkg:maven/org.apache/commons-lang3` returns versioned PURLs without qualifiers.

## What was checked
- `modules/fundamental/src/purl/service/mod.rs` (`PurlService::recommend`): the item mapping changed from `purl: p.to_string()` to:
  ```rust
  let simplified = p.without_qualifiers();
  PurlSummary { purl: simplified.to_string() }
  ```
  Every returned item is therefore serialized from a qualifier-stripped PURL. The version component is not touched by `without_qualifiers()`, so the result is still a versioned PURL.
- The qualifier `LeftJoin` on `purl::Relation::PurlQualifier` was removed from the query, as the Implementation Notes required.
- `modules/fundamental/src/purl/endpoints/recommend.rs`: the handler still calls `PurlService::recommend` and returns its result unchanged. Its only edits are dropping the unused `use sea_orm::JoinType;` import and a whitespace-only line.

## Test evidence
- `test_recommend_purls_basic` (tests/api/purl_recommend.rs) seeds `...commons-lang3@3.12?repository_url=...&type=jar` and `...@3.11?...`. It calls exactly this endpoint and asserts `body.items[0].purl == "pkg:maven/org.apache/commons-lang3@3.12"`. That is an exact match on a versioned PURL with no qualifiers.
- `test_simplified_purl_ordering_preserved` (tests/api/purl_simplify.rs) also checks versioned maven PURLs.
- All CI checks pass.

## Notes
- The Implementation Notes point to the `PackageUrl` builder in `common/src/purl.rs`. The diff instead calls `without_qualifiers()` on the value returned by the SeaORM query. CI passes, so the method exists on that type. This is a minor implementation detail and does not affect the criterion.

**Verdict: PASS**
