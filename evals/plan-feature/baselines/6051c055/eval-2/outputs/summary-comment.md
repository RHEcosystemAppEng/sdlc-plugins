## Plan Summary: TC-9002 "Improve search experience"

### Tasks Created

| # | Task | Scope |
|---|------|-------|
| 1 | Add full-text search indexes | SeaORM migration adding `tsvector` columns and GIN indexes; update query builder and SearchService to use full-text operators |
| 2 | Improve search relevance with weighted ranking | Add `ts_rank` scoring, relevance-based ordering, and `relevance_score` field in API response |
| 3 | Add search filter parameters | Add optional `type`, `date_from`, `date_to`, and `severity` query parameters to the search endpoint with composable `WHERE` clauses |
| 4 | Search integration tests | Comprehensive edge-case and cross-feature integration tests for all search improvements |

### Repositories Affected

- **trustify-backend** (all 4 tasks)

### Ambiguities Flagged

The following items from the feature description were excluded or treated as assumptions due to insufficient specification:

1. **"Search should be faster"** -- no latency targets defined. No baseline measurements, target p95/p99 latency, or dataset size expectations provided. Task 1 adds indexing as a best-practice improvement but cannot validate against undefined targets.
2. **"Results should be more relevant"** -- no relevance criteria defined. No ranking algorithm preference, field-weight priorities, or acceptance test for relevance quality. Task 2 implements `ts_rank` with reasonable defaults pending Product Owner validation.
3. **"Add filters"** -- no filter types specified. Task 3 assumes type, date range, and severity filters based on the expected data model. The actual filter set requires confirmation.
4. **"Better UI"** -- no frontend repository available, no design mockups linked. `trustify-backend` is a backend-only repository. UI work is entirely excluded from this plan.

### Inherited Field Propagation

- **Priority:** Normal -- inherited by all created tasks
- **Fix Versions:** RHTPA 1.6.0 -- inherited by all created tasks (fixVersion scope defaults to "both")

### Notes

- No documentation task generated (feature has no Documentation Considerations section)
- No testing readiness tasks generated (no testing readiness template available)

### Convention Enrichment

For each task, the following CONVENTIONS.md conventions apply based on the files being modified:

**Task 1 (search indexes):**
- Per CONVENTIONS.md §Framework: Use SeaORM for the database migration. Applies: task modifies `migration/src/` and `common/src/db/query.rs` matching the convention's SeaORM scope.
- Per CONVENTIONS.md §Error Handling: Use `Result<T, AppError>` with `.context()`. Applies: task modifies `modules/search/src/service/mod.rs` and `common/src/db/query.rs` matching the convention's error handling scope.

**Task 2 (search relevance):**
- Per CONVENTIONS.md §Framework: Use Axum for HTTP query parameter extraction. Applies: task modifies `modules/search/src/endpoints/mod.rs` matching the convention's Axum scope.
- Per CONVENTIONS.md §Module Pattern: Ranking logic in service layer, serialization in endpoints. Applies: task modifies `modules/search/src/service/mod.rs` and `modules/search/src/endpoints/mod.rs` matching the convention's module pattern scope.
- Per CONVENTIONS.md §Error Handling: Use `Result<T, AppError>` with `.context()`. Applies: task modifies `modules/search/src/service/mod.rs` matching the convention's error handling scope.

**Task 3 (search filters):**
- Per CONVENTIONS.md §Module Pattern: Filter model in `model/`, filter logic in `service/`, parameter extraction in `endpoints/`. Applies: task creates `modules/search/src/model/filters.rs` and modifies `modules/search/src/service/mod.rs` and `modules/search/src/endpoints/mod.rs` matching the convention's module pattern scope.
- Per CONVENTIONS.md §Framework: Use Axum `Query` extractor with `#[derive(Deserialize)]`. Applies: task modifies `modules/search/src/endpoints/mod.rs` matching the convention's Axum scope.
- Per CONVENTIONS.md §Framework: Use SeaORM `Condition::all()` for filter composition. Applies: task modifies `common/src/db/query.rs` matching the convention's SeaORM scope.
- Per CONVENTIONS.md §Error Handling: Use `Result<T, AppError>` with `.context()` for invalid filter values. Applies: task modifies `modules/search/src/endpoints/mod.rs` matching the convention's error handling scope.

**Task 4 (integration tests):**
- Per CONVENTIONS.md §Testing: Integration tests in `tests/api/` with real PostgreSQL. Applies: task modifies `tests/api/search.rs` matching the convention's testing scope.
- Per CONVENTIONS.md §Error Handling: Verify error responses use `AppError` format. Applies: task modifies `tests/api/search.rs` matching the convention's error handling scope.
