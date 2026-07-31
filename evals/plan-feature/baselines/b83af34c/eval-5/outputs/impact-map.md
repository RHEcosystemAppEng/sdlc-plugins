# Impact Map: TC-9005 — Drop status table and migrate to enum column

## Feature Summary

Replace the `advisory_status` lookup table with a PostgreSQL enum column on the `advisory` table. Eliminates unnecessary join overhead on advisory queries, simplifies the schema, and reduces advisory list endpoint p95 latency by ~40ms.

## Workflow Mode Decision

**Mode: feature-branch**

**Rationale:** The feature has explicit atomicity constraints that mandate feature-branch mode:

1. **Migration atomicity** — The database migration must be atomic. A partial migration (enum column exists but lookup table already dropped, or vice versa) would leave the database in an inconsistent state.
2. **Code-migration coupling** — Merging the migration without code changes breaks all advisory queries (they still join the now-dropped table). Merging code changes without the migration references a column that does not exist.
3. **Zero downtime requirement** — The migration must be safe to run while the application is serving traffic, requiring all changes to be coordinated.

These constraints require all changes to land together, which is the defining characteristic of feature-branch mode. Incremental direct-to-main delivery would risk leaving the application in a broken state between merges.

**Label decision:** Apply `workflow:feature-branch` label to TC-9005.

## Inherited Field Propagation

- **Priority:** High (propagated from TC-9005 to all created tasks)
- **Fix Versions:** RHTPA 2.0.0 (propagated from TC-9005 to all created tasks)

## Repository Impact

### trustify-backend

| Area | Impact | Files |
|---|---|---|
| Database Migration | New migration to create enum type, add column, backfill data, drop FK, drop lookup table | `migration/src/m0002_advisory_status_enum/mod.rs` (new), `migration/src/lib.rs` |
| Entity Definitions | Update advisory entity to use enum column, remove advisory_status entity | `entity/src/advisory.rs`, `entity/src/lib.rs` |
| Advisory Service & Endpoints | Remove status table joins from all advisory queries, update model structs | `modules/fundamental/src/advisory/service/advisory.rs`, `modules/fundamental/src/advisory/model/summary.rs`, `modules/fundamental/src/advisory/model/details.rs`, `modules/fundamental/src/advisory/model/mod.rs`, `modules/fundamental/src/advisory/endpoints/list.rs`, `modules/fundamental/src/advisory/endpoints/get.rs` |
| Ingestion Pipeline | Update advisory ingestion to write enum values directly instead of lookup table inserts | `modules/ingestor/src/graph/advisory/mod.rs` |
| Integration Tests | Update advisory endpoint tests for new schema | `tests/api/advisory.rs` |
| Documentation | Minor update to internal architecture docs reflecting schema change | Internal docs |

## Task Plan

| Task | Summary | Target Branch | Dependencies | Type |
|---|---|---|---|---|
| Task 1 | Create feature branch TC-9005 from main | main | None | Bookend (create-branch) |
| Task 2 | Create database migration for advisory status enum | TC-9005 | Task 1 | Implementation |
| Task 3 | Update SeaORM entity definitions for advisory status enum | TC-9005 | Task 1, Task 2 | Implementation |
| Task 4 | Update advisory service, model, and endpoints to use enum column | TC-9005 | Task 1, Task 3 | Implementation |
| Task 5 | Update advisory ingestion pipeline to write enum values directly | TC-9005 | Task 1, Task 3 | Implementation |
| Task 6 | Update internal architecture documentation for schema change | TC-9005 | Task 2, Task 3, Task 4, Task 5 | Documentation |
| Task 7 | Merge feature branch TC-9005 to main | main | Task 2, Task 3, Task 4, Task 5 | Bookend (merge-branch) |

## Atomicity Verification

All implementation tasks (2-5) target the feature branch TC-9005, ensuring:
- No partial changes reach main
- The migration, entity updates, service changes, and ingestion changes are merged atomically via the merge-branch bookend
- Zero-downtime requirement is satisfied by coordinated delivery
