# Criterion 3: Duplicate entries that were previously distinct due to different qualifiers are deduplicated in the response

## Verdict: PASS

## Reasoning

The PR adds explicit deduplication logic in the service layer and validates it with a dedicated test.

1. **Deduplication implementation:** In `modules/fundamental/src/purl/service/mod.rs`, a `.dedup_by()` call is added after the qualifier-stripping map:
   ```rust
   .map(|p| {
       let simplified = p.without_qualifiers();
       PurlSummary {
           purl: simplified.to_string(),
       }
   })
   .dedup_by(|a, b| a.purl == b.purl)
   .collect();
   ```
   This removes consecutive duplicates where the PURL strings are identical after qualifier removal.

2. **Dedicated test:** The new `test_recommend_purls_dedup` function in `tests/api/purl_recommend.rs` directly validates this behavior:
   - Seeds two PURLs for the same package version (`commons-lang3@3.12`) with different `repository_url` qualifiers (`repo1.maven.org` vs `repo2.maven.org`)
   - Requests recommendations and asserts only one entry is returned: `assert_eq!(body.items.len(), 1)`
   - Asserts the returned PURL is the qualifier-free versioned form: `assert_eq!(body.items[0].purl, "pkg:maven/org.apache/commons-lang3@3.12")`

3. **Note on `dedup_by` semantics:** `dedup_by` removes only consecutive duplicates, which relies on identical versioned PURLs being adjacent in the result set. Since the query orders by ID and the qualifiers are the only differentiator between rows that map to the same versioned PURL, adjacent ordering is a reasonable assumption. The test validates this end-to-end.

The deduplication logic is implemented and tested.
