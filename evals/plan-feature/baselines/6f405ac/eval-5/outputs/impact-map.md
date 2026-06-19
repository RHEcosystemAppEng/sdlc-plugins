# Impact Map — TC-9005: Drop status table and migrate to enum column

## Workflow Mode Decision

**Mode: feature-branch**

The feature requires the `workflow:feature-branch` label on the feature issue. Rationale: the migration must be atomic (partial migration leaves the database inconsistent), and all code changes are coupled with the migration (merging code without migration references a nonexistent column; merging migration without code breaks existing joins). All changes must land together via a feature branch.

## Repository: trustify-backend

### migration/
| File | Change | Task |
|---|---|---|
| `migration/src/lib.rs` | Modify — register new migration module | Task 2 |
| `migration/src/m0002_advisory_status_enum/mod.rs` | Create — enum migration (create type, add column, backfill, drop FK, drop table) | Task 2 |
| `migration/Cargo.toml` | Modify — add dependencies if needed | Task 2 |

### entity/
| File | Change | Task |
|---|---|---|
| `entity/src/advisory.rs` | Modify — replace `status_id` FK with `status` enum field; remove relation to advisory_status | Task 3 |
| `entity/src/advisory_status_enum.rs` | Create — `AdvisoryStatusEnum` with SeaORM `DeriveActiveEnum` | Task 3 |
| `entity/src/lib.rs` | Modify — remove advisory_status module, add advisory_status_enum module | Task 3 |

### modules/fundamental/ (advisory)
| File | Change | Task |
|---|---|---|
| `modules/fundamental/src/advisory/service/advisory.rs` | Modify — remove advisory_status join from all queries; filter on enum column | Task 4 |
| `modules/fundamental/src/advisory/model/summary.rs` | Modify — source status from enum field | Task 4 |
| `modules/fundamental/src/advisory/model/details.rs` | Modify — source status from enum field | Task 4 |
| `modules/fundamental/src/advisory/model/mod.rs` | Modify — update re-exports if needed | Task 4 |
| `modules/fundamental/src/advisory/endpoints/list.rs` | Modify — update status filter to use enum comparison | Task 4 |
| `modules/fundamental/src/advisory/endpoints/get.rs` | Modify — update if it references status join | Task 4 |

### modules/ingestor/
| File | Change | Task |
|---|---|---|
| `modules/ingestor/src/graph/advisory/mod.rs` | Modify — write enum value directly instead of lookup table insert | Task 5 |
| `modules/ingestor/src/service/mod.rs` | Modify — remove advisory_status entity references | Task 5 |

### tests/
| File | Change | Task |
|---|---|---|
| `tests/api/advisory.rs` | Modify — update fixtures to use enum status; add enum filtering test | Task 6 |
