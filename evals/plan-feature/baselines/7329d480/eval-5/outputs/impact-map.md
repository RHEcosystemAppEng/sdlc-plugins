# Impact Map: TC-9005 — Drop status table and migrate to enum column

## Overview

Replace the `advisory_status` lookup table with a PostgreSQL enum column on the `advisory` table. This eliminates unnecessary join overhead on every advisory query, simplifies the data model, and reduces p95 latency on the advisory list endpoint by approximately 40ms.

## Workflow Mode: Feature-Branch

This feature requires **feature-branch** workflow due to atomicity constraints:

- The migration drops the `advisory_status` table and adds an `advisory_status_enum` column — the code changes depend on the migration being present.
- Merging the migration without the corresponding code changes would break all advisory queries, which still join the now-dropped table.
- Merging the code changes without the migration would reference a column (`status`) that does not exist.
- All changes must land together atomically via a feature branch.

The `workflow:feature-branch` label will be applied to the TC-9005 feature issue.

## Affected Repository

### trustify-backend

| Area | Files | Change Type |
|---|---|---|
| Database migration | `migration/src/m0002_advisory_status_enum/mod.rs` | Create |
| Database migration | `migration/src/lib.rs` | Modify |
| SeaORM entities | `entity/src/advisory.rs` | Modify |
| SeaORM entities | `entity/src/advisory_status.rs` | Remove |
| SeaORM entities | `entity/src/lib.rs` | Modify |
| Advisory model | `modules/fundamental/src/advisory/model/summary.rs` | Modify |
| Advisory model | `modules/fundamental/src/advisory/model/details.rs` | Modify |
| Advisory model | `modules/fundamental/src/advisory/model/mod.rs` | Modify |
| Advisory service | `modules/fundamental/src/advisory/service/advisory.rs` | Modify |
| Advisory endpoints | `modules/fundamental/src/advisory/endpoints/list.rs` | Modify |
| Advisory endpoints | `modules/fundamental/src/advisory/endpoints/get.rs` | Modify |
| Ingestion pipeline | `modules/ingestor/src/graph/advisory/mod.rs` | Modify |
| Ingestion pipeline | `modules/ingestor/src/service/mod.rs` | Modify |
| Integration tests | `tests/api/advisory.rs` | Modify |
| Documentation | Internal architecture docs | Update |

## Task Summary

| Task | Summary | Target Branch |
|---|---|---|
| 1 | Create feature branch TC-9005 from main | main |
| 2 | Write database migration for advisory status enum | TC-9005 |
| 3 | Update SeaORM entity definitions for advisory status enum | TC-9005 |
| 4 | Update advisory service, model, and endpoints to use status enum | TC-9005 |
| 5 | Update advisory ingestion pipeline for direct enum writes | TC-9005 |
| 6 | Update advisory integration tests for status enum | TC-9005 |
| 7 | Update internal architecture documentation for schema change | main |
| 8 | Merge feature branch TC-9005 to main | main |

## Dependency Graph

```
Task 1 (create-branch)
  |
  +---> Task 2 (migration) ---> Task 3 (entities) --+--> Task 4 (service/endpoints) --+--> Task 6 (tests) --+
  |                                                  |                                |                     |
  |                                                  +--> Task 5 (ingestion) ---------+                     |
  |                                                                                                         |
  +--- Task 7 (docs, independent) ------>                                                                   |
                                                                                                            v
                                                                                              Task 8 (merge-branch)
                                                                                    depends on: 2, 3, 4, 5, 6
```

## Atomicity Rationale

The feature branch ensures that the database migration (Task 2), entity updates (Task 3), service/endpoint changes (Task 4), ingestion updates (Task 5), and test updates (Task 6) all land on `main` in a single merge. This prevents any intermediate state where the schema and code are out of sync.
