# Criterion 3: Duplicate entries that were previously distinct due to different qualifiers are deduplicated in the response

## Verdict: FAIL

## Reasoning

The implementation adds `.dedup_by(|a, b| a.purl == b.purl)` to the iterator chain in `modules/fundamental/src/purl/service/mod.rs`. However, `dedup_by` on a Rust iterator only removes **consecutive** duplicates, similar to the Unix `uniq` command. It does NOT perform full deduplication across the entire collection.

For `dedup_by` to work correctly, identical PURLs must appear adjacently in the iterator. The database query has no `ORDER BY` clause — it uses `Purl::find().filter(...).filter(...)` without any `.order_by()`. This means the row ordering is database-implementation-dependent and not guaranteed.

If two purl rows with the same type/namespace/name/version but different qualifiers are stored non-adjacently in the database (e.g., if another version was inserted between them), they would appear non-adjacently in the result set after `without_qualifiers()` strips their distinguishing qualifier data. In this case, `dedup_by` would fail to collapse them.

The test `test_recommend_purls_dedup` seeds two PURLs consecutively and asserts `body.items.len() == 1`. This test passes because the two seeded PURLs happen to be returned adjacently from the database. The test does not exercise the non-adjacent duplicate case, so it provides a false sense of correctness.

Correct alternatives would be:
- Using `itertools::unique_by()` for hash-based deduplication
- Using a `HashSet`-based filter
- Adding an `ORDER BY` clause to the query to guarantee adjacency before `dedup_by`

## Evidence

- `modules/fundamental/src/purl/service/mod.rs`: `.dedup_by(|a, b| a.purl == b.purl)` — only removes consecutive duplicates
- No `.order_by()` call in the query chain
- `tests/api/purl_recommend.rs`: `test_recommend_purls_dedup` seeds 2 consecutive PURLs — does not test non-adjacent dedup
- Rust std docs: `Iterator::dedup_by` — "Removes all but the first of **consecutive** elements"
