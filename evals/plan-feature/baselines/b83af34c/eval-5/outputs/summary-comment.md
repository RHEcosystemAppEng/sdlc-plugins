## Planning Summary — TC-9005: Drop status table and migrate to enum column

### Workflow Mode
**Feature-branch** — atomicity constraints require all changes to land together. The `workflow:feature-branch` label will be applied to TC-9005.

### Inherited Fields
- **Priority:** High (propagated from TC-9005 to all 7 created tasks)
- **Fix Versions:** RHTPA 2.0.0 (propagated from TC-9005 to all 7 created tasks)

### Tasks Created

| # | Summary | Type | Target Branch |
|---|---|---|---|
| 1 | Create feature branch TC-9005 from main | Bookend (create-branch) | main |
| 2 | Create database migration for advisory status enum | Implementation | TC-9005 |
| 3 | Update SeaORM entity definitions for advisory status enum | Implementation | TC-9005 |
| 4 | Update advisory service, model, and endpoints to use enum column | Implementation | TC-9005 |
| 5 | Update advisory ingestion pipeline to write enum values directly | Implementation | TC-9005 |
| 6 | Update internal architecture documentation for schema change | Documentation | TC-9005 |
| 7 | Merge feature branch TC-9005 to main | Bookend (merge-branch) | main |

### Dependency Chain
```
Task 1 (create-branch)
  +-- Task 2 (migration)
       +-- Task 3 (entity update)
            +-- Task 4 (service/endpoints)
            +-- Task 5 (ingestion pipeline)
                 +-- Task 6 (documentation) [depends on Tasks 2-5]
                 +-- Task 7 (merge-branch) [depends on Tasks 2-5]
```

### Coverage
- **Migration**: Atomic enum type creation, column addition, data backfill, FK drop, and table drop
- **Entities**: SeaORM entity definitions updated to use `AdvisoryStatus` enum
- **Service layer**: All advisory queries updated to eliminate `advisory_status` join
- **Ingestion**: Pipeline writes enum values directly instead of lookup table inserts
- **Documentation**: Internal architecture docs updated (minor impact)
- **API**: No external API changes — response shape remains unchanged
