## Planning Summary: TC-9003 SBOM Comparison View

### Tasks Created

| # | Summary | Repository | Dependencies |
|---|---|---|---|
| 1 | SBOM comparison model and diff service | trustify-backend | -- |
| 2 | SBOM comparison REST endpoint and integration tests | trustify-backend | Task 1 |
| 3 | SBOM comparison API types, client function, and React Query hook | trustify-ui | Task 2 |
| 4 | SBOM comparison page and routing | trustify-ui | Task 3 |
| 5 | SBOM list page comparison selection UI | trustify-ui | Task 4 |

### Cross-Repo Dependency Chain

```
trustify-backend          trustify-ui
  Task 1 (model+service)
    |
  Task 2 (endpoint) -----> Task 3 (types+hook)
                              |
                            Task 4 (comparison page)
                              |
                            Task 5 (list page selection)
```

### Inherited Field Propagation

- **Priority**: Critical -- propagated from TC-9003 to all 5 tasks
- **fixVersions**: RHTPA 1.5.0 -- propagated from TC-9003 to all 5 tasks

### Design Context

Frontend tasks 4 and 5 reference the Figma design specifications for PatternFly component mapping, layout structure, badge colors, empty/loading states, and table column definitions. Task 3 (API types and hook) is exempt from Figma requirements as it is an API-layer task.

### Key Decisions

- **No database migrations**: Comparison is computed on-the-fly from existing package, advisory, and license data, satisfying the non-functional requirement of no new database tables.
- **Backend-first ordering**: Backend tasks (1-2) are numbered before frontend tasks (3-5) to reflect the dependency chain where the API contract must be defined before the frontend can be built.
- **Virtualized tables**: Frontend uses virtualized rendering for diff sections with >100 rows, addressing the non-functional requirement to prevent browser freezing on large diffs.
- **URL-shareable comparisons**: The comparison page reads and writes `left` and `right` query parameters, enabling bookmarkable and shareable comparison URLs.
