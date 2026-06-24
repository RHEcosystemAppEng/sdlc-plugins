## Review Comment Classification: #30002

**Reviewer**: reviewer-a
**File**: `migration/src/m0042_sbom_soft_delete/mod.rs`, line 14
**Comment**: The migration should also add an index on `deleted_at` for the sbom table. Queries filtering by `deleted_at IS NULL` will be frequent and a partial index would help. Something like: `CREATE INDEX idx_sbom_not_deleted ON sbom (deleted_at) WHERE deleted_at IS NULL;`

### Classification: Suggestion

**Reasoning**: The reviewer uses suggestive language: "should also add" and "would help". The phrase "should also" indicates an additive recommendation beyond the current scope rather than a mandatory fix to existing code. The phrase "would help" signals that this is a performance optimization that the reviewer believes is beneficial but is not framing as a blocking requirement. The reviewer provides a SQL example as a helpful illustration, not as a demand. Compare this to comment #30001 where the reviewer uses imperative language about a correctness bug -- here the existing code is functionally correct without the index; the index is a performance improvement.

### Convention Upgrade Eligibility

The comment suggests adding a database index, which could be considered a convention if there were a documented project convention requiring indexes on nullable filter columns. Reviewing the repository conventions in `CONVENTIONS.md` and the key conventions listed in the repository structure:

- **Framework**: Axum for HTTP, SeaORM for database
- **Module pattern**: model/ + service/ + endpoints/ structure
- **Error handling**: Result<T, AppError> with .context() wrapping
- **Endpoint registration**: routes in endpoints/mod.rs
- **Response types**: PaginatedResults<T>
- **Query helpers**: shared filtering, pagination, sorting
- **Testing**: integration tests in tests/api/
- **Caching**: tower-http caching middleware

None of these documented conventions mandate adding indexes on soft-delete columns or nullable filter columns. There is no documented convention in the repository that backs upgrading this suggestion to a code change request.

**Conclusion**: The suggestion is reasonable from a performance perspective, but no documented convention supports upgrading it. Per the classification rules, this remains a **suggestion** and does NOT create a sub-task.

**Action**: No sub-task created.
