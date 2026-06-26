# Impact Map — TC-9005: Drop status table and migrate to enum column

## Workflow Mode

**Mode**: feature-branch

**Rationale**: This feature requires feature-branch mode because:
1. **Atomic migration**: The database migration creates an enum type, backfills data, and drops the lookup table — a partial migration would leave the database in an inconsistent state.
2. **Breaking code-schema coupling**: The code changes (entity definitions, service queries, endpoints, ingestion pipeline) depend on the migration, and the migration would break existing code that joins the now-dropped table. All changes must land on main simultaneously.
3. **All-or-nothing delivery**: Merging the migration without the code changes would break all advisory queries; merging code changes without the migration would reference a column that does not exist.

**Label**: Apply `workflow:feature-branch` to the TC-9005 feature issue.

## Summary

Replace the `advisory_status` lookup table with a PostgreSQL `advisory_status_enum` column on the `advisory` table. This eliminates a join from every advisory query, simplifies the ingestion pipeline, and reduces schema complexity. The change spans the migration layer, entity definitions, service/query layer, REST endpoints, ingestion pipeline, and integration tests.

## Impacted Areas

### Database Schema
- **Migration** (`migration/src/`): New migration creates enum type, adds column, backfills, drops FK and lookup table
- **Risk**: High — atomic migration with data backfill; failure leaves inconsistent state if not transactional

### Entity Layer
- **Entity definitions** (`entity/src/`): Advisory entity gains enum column, loses FK relation; advisory_status entity removed
- **Risk**: Medium — all downstream code depends on entity definitions compiling correctly

### Advisory Module — Service Layer
- **Service** (`modules/fundamental/src/advisory/service/`): All queries updated to remove advisory_status join
- **Models** (`modules/fundamental/src/advisory/model/`): Summary and detail structs read from enum column
- **Risk**: Medium — query changes affect all advisory read paths

### Advisory Module — Endpoints
- **Endpoints** (`modules/fundamental/src/advisory/endpoints/`): Status filter parameter parses to enum; route cleanup
- **Risk**: Low — API response shape unchanged; only internal plumbing changes

### Ingestion Pipeline
- **Advisory ingestion** (`modules/ingestor/src/graph/advisory/`): Writes enum values directly instead of lookup table insert
- **Ingestor service** (`modules/ingestor/src/service/`): Status mapping updated
- **Risk**: Medium — incorrect mapping could silently store wrong status values

### Search Module
- **Search** (`modules/search/src/`): May need updates if search indexes advisory status via the lookup table join
- **Risk**: Low — likely only affected if search queries join advisory_status

### Integration Tests
- **Advisory tests** (`tests/api/advisory.rs`): Test setup and assertions updated for enum-based status
- **Search tests** (`tests/api/search.rs`): Status-related search assertions updated
- **Risk**: Low — test-only changes

## Task Dependency Graph

```
Task 1: Create feature branch TC-9005 from main
  |
  +---> Task 2: Create atomic migration
  |       |
  |       +---> Task 3: Update SeaORM entity definitions
  |               |
  |               +---> Task 4: Update advisory service and models
  |               |       |
  |               |       +---> Task 5: Update advisory endpoints
  |               |                       |
  |               +---> Task 6: Update ingestion pipeline
  |                       |             |
  |                       +-------------+
  |                               |
  |                       Task 7: Update integration tests
  |                               |
  +-------------------------------+
  |
  Task 8: Merge feature branch TC-9005 to main
```

## Task Summary

| # | Task | Target Branch | Type |
|---|------|---------------|------|
| 1 | Create feature branch TC-9005 from main | main | bookend (create-branch) |
| 2 | Create atomic migration: enum type, backfill, and table drop | TC-9005 | implementation |
| 3 | Update SeaORM entity definitions for advisory status enum | TC-9005 | implementation |
| 4 | Update advisory service layer and models to use enum column | TC-9005 | implementation |
| 5 | Update advisory endpoints for enum-based status filtering | TC-9005 | implementation |
| 6 | Update advisory ingestion pipeline to write enum values directly | TC-9005 | implementation |
| 7 | Update integration tests for advisory status enum | TC-9005 | implementation |
| 8 | Merge feature branch TC-9005 to main | main | bookend (merge-branch) |

## Files Impacted

| File | Tasks | Change Type |
|------|-------|-------------|
| `migration/src/lib.rs` | 2 | Modify |
| `migration/src/m0002_advisory_status_enum/mod.rs` | 2 | Create |
| `entity/src/advisory.rs` | 3 | Modify |
| `entity/src/lib.rs` | 3 | Modify |
| `modules/fundamental/src/advisory/service/advisory.rs` | 4 | Modify |
| `modules/fundamental/src/advisory/model/summary.rs` | 4 | Modify |
| `modules/fundamental/src/advisory/model/details.rs` | 4 | Modify |
| `modules/fundamental/src/advisory/model/mod.rs` | 4 | Modify |
| `modules/fundamental/src/advisory/endpoints/list.rs` | 5 | Modify |
| `modules/fundamental/src/advisory/endpoints/get.rs` | 5 | Modify |
| `modules/fundamental/src/advisory/endpoints/mod.rs` | 5 | Modify |
| `modules/ingestor/src/graph/advisory/mod.rs` | 6 | Modify |
| `modules/ingestor/src/service/mod.rs` | 6 | Modify |
| `tests/api/advisory.rs` | 7 | Modify |
| `tests/api/search.rs` | 7 | Modify |

## Risk Assessment

- **Overall risk**: Medium-High
- **Primary risk**: The atomic migration must execute correctly in production with existing data; a backfill error could corrupt status values
- **Mitigation**: Test migration against a production-sized dataset clone; feature branch ensures all changes land together; down migration enables rollback
