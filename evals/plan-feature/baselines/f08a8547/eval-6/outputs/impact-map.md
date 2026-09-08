# Repository Impact Map — TC-9006: Add vulnerability remediation tracking dashboard

## Repositories

### trustify-backend
Changes:
- Create new `modules/remediation/` module following the established model/service/endpoints pattern
- Implement `GET /api/v2/remediation/summary` endpoint returning aggregated vulnerability counts by severity (Critical/High/Medium/Low) and status (Open/In Progress/Resolved)
- Implement `GET /api/v2/remediation/by-product` endpoint returning paginated per-product remediation breakdown with total, open, and resolved counts
- Add remediation module to workspace `Cargo.toml` and mount routes in `server/src/main.rs`
- Add integration tests for both remediation endpoints in `tests/api/`
- All aggregations computed from existing entity data (`advisory`, `sbom_advisory`, `sbom`) — no new database tables

### trustify-ui
Changes:
- Add TypeScript interfaces for remediation API response types in `src/api/models.ts`
- Add API client functions (`fetchRemediationSummary`, `fetchRemediationByProduct`) in `src/api/rest.ts`
- Add React Query hooks (`useRemediationSummary`, `useRemediationByProduct`) in `src/hooks/`
- Create `RemediationDashboardPage` at `/remediation` with summary cards (Open, In Progress, Resolved) and progress chart (30-day trend)
- Add filterable vulnerability table component with severity, product, and status filters using existing `FilterToolbar` and `SeverityBadge` components
- Register `/remediation` route with lazy loading in `src/routes.tsx`
- Add documentation for the remediation dashboard and API endpoints (New Content — per Documentation Considerations)

## Excluded Requirements
- **CSV export of remediation report** (non-MVP): Explicitly marked as non-MVP in the feature requirements table. Can be planned in a future iteration — no missing inputs prevent decomposition. The export would require a new backend endpoint for CSV generation and an export button on the frontend dashboard.

## Workflow Mode

**Mode: direct-to-main**

Rationale — atomicity analysis:
1. **Coordinated schema migrations**: None — no new database tables; all aggregations are computed from existing vulnerability and SBOM relationship data.
2. **Breaking API changes**: None — both remediation endpoints are new additions at new paths (`/api/v2/remediation/summary` and `/api/v2/remediation/by-product`). No existing endpoints are modified.
3. **Cross-cutting refactors**: None — the backend adds a new module and the frontend adds a new page without restructuring existing code.
4. **Tightly coupled feature components**: Not blocking — the backend endpoints are independently deployable (additive, no existing functionality depends on them). The frontend page is at a new route (`/remediation`) that does not affect existing pages. With dependency ordering (backend tasks complete before frontend tasks), each PR merges cleanly to main without leaving the codebase in a broken state.

No atomicity indicators were identified. All tasks target `main`.

## Epic Hierarchy

**Grouping strategy: by-repository** (from CLAUDE.md Hierarchy Configuration)

### Epic: TC-9006: trustify-backend
- Issue type: Epic (level 1)
- Parent: TC-9006
- Description: Backend remediation module providing aggregation API endpoints for vulnerability remediation tracking. Includes the summary endpoint (severity-by-status matrix) and per-product breakdown endpoint with pagination.
- additional_fields: `{ "labels": ["ai-generated-jira"], "priority": {"name": "High"}, "fixVersions": [{"name": "RHTPA 1.5.0"}] }`
- Tasks:
  - Task 1 — Create remediation module with summary aggregation endpoint
  - Task 2 — Add per-product remediation breakdown endpoint

### Epic: TC-9006: trustify-ui
- Issue type: Epic (level 1)
- Parent: TC-9006
- Description: Frontend remediation dashboard page with summary cards, progress chart, and filterable vulnerability table. Includes API data layer (types, client functions, React Query hooks) and documentation.
- additional_fields: `{ "labels": ["ai-generated-jira"], "priority": {"name": "High"}, "fixVersions": [{"name": "RHTPA 1.5.0"}] }`
- Tasks:
  - Task 3 — Add remediation API types, client functions, and React Query hooks
  - Task 4 — Create remediation dashboard page with summary cards and progress chart
  - Task 5 — Add filterable vulnerability table to remediation dashboard
  - Task 6 — Add remediation dashboard and API documentation

## Issue Links

### Incorporates (Feature to Epics)
- TC-9006 **incorporates** Epic "TC-9006: trustify-backend"
- TC-9006 **incorporates** Epic "TC-9006: trustify-ui"

Note: Incorporates links go from Feature to Epics only, not from Feature to individual Tasks. Tasks inherit hierarchy through their Epic parent.

### Depends (Task dependencies)
- Task 2 **depends on** Task 1
- Task 3 **depends on** Task 1, Task 2
- Task 4 **depends on** Task 3
- Task 5 **depends on** Task 4
- Task 6 **depends on** Tasks 1, 2, 3, 4, 5

## Field Inheritance

- **Priority**: "High" — inherited from Feature TC-9006 and propagated to all Epics and Tasks via `additional_fields.priority`.
- **fixVersions**: ["RHTPA 1.5.0"] — inherited from Feature TC-9006 and propagated to all Epics and Tasks via `additional_fields.fixVersions`. The `fixVersion scope` setting is not present in CLAUDE.md Jira Field Defaults, defaulting to "both" (propagate to tasks).
- **Labels**: All created issues include the `ai-generated-jira` label.

## Task Creation Log — additional_fields

All tasks and Epics are created with the following `additional_fields`:
```json
{
  "labels": ["ai-generated-jira"],
  "priority": {"name": "High"},
  "fixVersions": [{"name": "RHTPA 1.5.0"}]
}
```

---

*This comment was AI-generated by [sdlc-workflow/plan-feature](https://github.com/RHEcosystemAppEng/sdlc-plugins) v0.13.9.*
