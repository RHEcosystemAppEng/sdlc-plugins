# Criterion 1 — PASS

**Criterion:** `GET /api/v2/purl/recommend?purl=pkg:maven/org.apache/commons-lang3` returns versioned PURLs without qualifiers.

## Reasoning

- `modules/fundamental/src/purl/service/mod.rs` now calls `without_qualifiers()` on every row before it serializes it:
  ```rust
  .map(|p| {
      let simplified = p.without_qualifiers();
      PurlSummary {
          purl: simplified.to_string(),
      }
  })
  ```
  This is the `without_qualifiers()` approach the Implementation Notes ask for. It strips only the qualifiers, so the version stays in the PURL.
- The qualifier join is removed from the recommendation query, as the notes require:
  `- .join(JoinType::LeftJoin, purl::Relation::PurlQualifier.def());`
  The unused `use sea_orm::JoinType;` import is also removed from `endpoints/recommend.rs`.
- Test coverage: `test_recommend_purls_basic` now asserts
  `assert_eq!(body.items[0].purl, "pkg:maven/org.apache/commons-lang3@3.12");`. That is a versioned PURL with no qualifiers.

## Caveats (they do not change the verdict)

- The `items[0] == ...@3.12` assertion depends on row order, but the query has no `ORDER BY` (see Criterion 4). The test could become flaky.
- The diff alone cannot confirm that the entity model `p` exposes `without_qualifiers()`, because the method is documented on `PackageUrl` in `common/src/purl.rs`. CI passes, which means the code compiles.
