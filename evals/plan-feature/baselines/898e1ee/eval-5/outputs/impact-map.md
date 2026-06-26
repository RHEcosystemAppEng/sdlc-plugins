# Impact Map: TC-9005 -- Drop status table and migrate to enum column

## Feature Summary
Replace the `advisory_status` lookup table with a PostgreSQL enum column on the `advisory` table to eliminate unnecessary joins, improve query performance, and reduce schema complexity.

## Workflow
**Label: workflow:feature-branch**

All changes must land atomically. The database migration and code changes are interdependent: merging the migration without the code changes would break all advisory queries (they still join the now-dropped table), and merging the code changes without the migration would reference a column that does not exist. A feature branch (TC-9005) is used to collect all intermediate PRs before merging to main in a single operation.

## Repositories Impacted
- **trustify-backend** -- sole repository; all migration, entity, service, ingestor, and test changes

## Impact by Area

### Database Schema
| File / Area | Change Type | Impact |
|---|---|---|
| `migration/src/m0002_advisory_status_enum/mod.rs` | CREATE | New reversible migration: create enum type, add column, backfill, drop FK, drop table |
| `migration/src/lib.rs` | MODIFY | Register new migration module |

### Entity Layer
| File / Area | Change Type | Impact |
|---|---|---|
| `entity/src/advisory.rs` | MODIFY | Replace `status_id: i32` with `status: AdvisoryStatusEnum`; define DeriveActiveEnum; remove Relation::AdvisoryStatus |
| `entity/src/lib.rs` | MODIFY | Remove `pub mod advisory_status` re-export |

### Service / Endpoint Layer
| File / Area | Change Type | Impact |
|---|---|---|
| `modules/fundamental/src/advisory/service/advisory.rs` | MODIFY | Remove advisory_status joins; filter by enum column directly |
| `modules/fundamental/src/advisory/model/summary.rs` | MODIFY | Source status from enum column instead of joined table |
| `modules/fundamental/src/advisory/model/details.rs` | MODIFY | Source status from enum column instead of joined table |
| `modules/fundamental/src/advisory/model/mod.rs` | MODIFY | Update imports if referencing advisory_status entity |
| `modules/fundamental/src/advisory/endpoints/list.rs` | MODIFY | Status filter compares against enum values |
| `modules/fundamental/src/advisory/endpoints/get.rs` | MODIFY | Remove advisory_status join if present |

### Ingestor
| File / Area | Change Type | Impact |
|---|---|---|
| `modules/ingestor/src/graph/advisory/mod.rs` | MODIFY | Map status strings to enum variants; set status field directly |
| `modules/ingestor/src/service/mod.rs` | MODIFY | Remove advisory_status imports if present |

### Tests
| File / Area | Change Type | Impact |
|---|---|---|
| `tests/api/advisory.rs` | MODIFY | Update fixtures to use enum status; add enum filter test |

## API Changes
None. The advisory API response shape is unchanged -- status remains a string field. This is a backend-only schema and query optimization.

## Risk Assessment
- **High risk**: Database migration is irreversible in production if the down migration is not tested. Mitigation: Task 2 requires a tested reversible migration.
- **Medium risk**: Partial deployment (migration without code or vice versa) breaks the application. Mitigation: Feature-branch workflow ensures atomic landing.
- **Low risk**: Enum values are stable (4 values, unchanged for over a year). Adding new values later requires a migration but is straightforward with PostgreSQL `ALTER TYPE ... ADD VALUE`.

## Task Breakdown

| Task | Title | Target Branch | Dependencies |
|---|---|---|---|
| 1 | Create feature branch TC-9005 from main | main | None |
| 2 | Database migration for advisory_status_enum | TC-9005 | Task 1 |
| 3 | Update SeaORM entity definitions | TC-9005 | Task 1 |
| 4 | Update advisory service and endpoints | TC-9005 | Task 1 |
| 5 | Update advisory ingestor | TC-9005 | Task 1 |
| 6 | Update integration tests | TC-9005 | Task 1 |
| 7 | Merge feature branch TC-9005 to main | main | Tasks 2, 3, 4, 5, 6 |

## Dependency Graph
```
Task 1 (create-branch)
  |
  +-- Task 2 (migration)    --+
  +-- Task 3 (entities)      --+
  +-- Task 4 (service/api)   --+-- Task 7 (merge-branch)
  +-- Task 5 (ingestor)      --+
  +-- Task 6 (tests)         --+
```

Tasks 2-6 can be implemented in parallel after Task 1, though there are logical dependencies (Task 3 defines the enum type used by Tasks 4, 5, and 6). Task 7 executes only after all intermediate tasks are merged into the feature branch.
