# Criterion 1

**Criterion:** `GET /api/v2/purl/recommend?purl=pkg:maven/org.apache/commons-lang3` returns versioned PURLs without qualifiers

**Verdict:** PASS

## Evidence

- `modules/fundamental/src/purl/service/mod.rs` (`PurlService::recommend`): the item mapping now calls
  `p.without_qualifiers()` and serializes that value (`purl: simplified.to_string()`) instead of
  `p.to_string()`. This follows the Implementation Notes, which point to `without_qualifiers()` on the
  `PackageUrl` builder.
- The `LeftJoin` to `purl::Relation::PurlQualifier` is removed from the query, so qualifier rows no longer
  feed into the result.
- `without_qualifiers()` drops only the qualifier part, so the version stays in the PURL
  (e.g. `pkg:maven/org.apache/commons-lang3@3.12`).
- Test coverage: `test_recommend_purls_basic` (tests/api/purl_recommend.rs) seeds two qualified
  commons-lang3 PURLs, calls this exact endpoint, and asserts
  `body.items[0].purl == "pkg:maven/org.apache/commons-lang3@3.12"`. That is the versioned PURL with no qualifiers.
- The endpoint handler (`endpoints/recommend.rs`) still calls `PurlService::recommend` and returns its result.
  The only changes there are removing the now-unused `JoinType` import and a whitespace-only line.

## Conclusion

The code path and its test both show that the endpoint returns versioned PURLs without qualifiers.
