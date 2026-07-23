# Repository Impact Map -- TC-9002: Improve search experience

## trustify-backend

**Changes:**
- Add database indexes on search-relevant columns (entity name fields, timestamps) to improve full-text search query performance
- Enhance SearchService with relevance-weighted ranking to return more meaningful search results
- Add filter query parameters (entity type, date range) to the GET /api/v2/search endpoint with validation and backward-compatible defaults
- Update search integration tests to cover filter combinations, relevance ordering, and edge cases

## Excluded Requirements

| Requirement | MVP? | Reason for Exclusion |
|---|---|---|
| **Better UI** -- "Make it look nicer" | No | No frontend repository in the Repository Registry. Cannot plan UI changes without a target repository and design mockups. Provide a frontend repo and Figma URL to enable planning. |
| **Performance SLA** -- "Search should be faster" / "Should be fast enough" | Yes (partial) | The requirement does not specify a current performance baseline or target latency. Tasks include performance improvements (database indexing) but acceptance criteria cannot reference a specific SLA. The team should define quantitative targets (e.g., "p95 search latency < 200ms") so that performance can be measured and verified. |
| **Relevance definition** -- "Results should be more relevant" | Yes (partial) | The requirement does not define what "relevant" means -- no field weighting rules, no ranking algorithm preference, no distinction between entity types. Tasks include standard PostgreSQL full-text search ranking as a reasonable default, but the team should provide domain-specific relevance rules if the defaults are insufficient (e.g., should advisories with critical severity rank higher than SBOMs?). |
| **Filter specification** -- "Add filters: some kind of filtering capability" | Yes (partial) | The requirement does not specify which filters to implement. Tasks include entity-type and date-range filters based on the existing data model as a minimum viable set. The team should confirm whether additional filters are needed (e.g., severity, license type, package name, SBOM format). |

## Workflow Mode

**Mode:** `direct-to-main`

**Rationale:** No atomicity indicators found:

1. **Coordinated schema migrations** -- Not present. Database index additions (Task 1) are additive DDL operations. They create new indexes without modifying existing columns or tables. Tasks 2 and 3 benefit from indexes for performance but function correctly without them.
2. **Breaking API changes** -- Not present. Task 3 adds new optional query parameters to GET /api/v2/search. Existing callers that omit the new parameters continue to receive unfiltered results. No request or response schema changes break backward compatibility.
3. **Cross-cutting refactors** -- Not present. No renames, module reorganizations, or shared type changes span multiple tasks.
4. **Tightly coupled feature components** -- Not present. All tasks modify the same backend service but each produces independently deployable and testable changes. No task requires another task's code to be present for `main` to remain functional.

Each task PR can merge to `main` independently without leaving the codebase in a broken state.

## Task-to-Jira Field Mapping

All created issues will include the following `additional_fields`:

| Field | Value | Rationale |
|---|---|---|
| `labels` | `["ai-generated-jira"]` | Required on all AI-generated issues (per Step 6a) |
| `priority` | `{"name": "Normal"}` | Inherited from Feature TC-9002 (priority is "Normal", not "Undefined") |
| `fixVersions` | `[{"name": "RHTPA 1.6.0"}]` | Inherited from Feature TC-9002 (fixVersions is non-empty; no `fixVersion scope` setting in Jira Field Defaults section of CLAUDE.md, so defaults to "both" -- propagate to tasks) |

## Issue Type Discovery

Issue types would be discovered dynamically via `jira.get_project_issue_types(cloudId="2b9e35e3-6bd3-4cec-b838-f4249ee02432", projectKey="TC")` per Step 2.5.

Since Jira is unavailable in this eval context:

- **Feature type**: ID 10142 (from Jira Configuration in CLAUDE.md), hierarchy level 2
- **Epic type (level-1)**: Not discoverable. If a level-1 type exists, the Hierarchy Configuration specifies `Default epic grouping strategy: by-sub-feature`, and tasks would be grouped into Epics by logical sub-feature (e.g., "Performance optimization", "Relevance scoring", "Search filters"). If no level-1 type is found, tasks are created directly under the Feature using Feature -> Task hierarchy (per constraint 1.64).
- **Task type (level-0)**: Would be discovered dynamically from the project metadata

## Documentation Task Generation

**Skipped.** The Feature description has no "Documentation Considerations" section. Per constraint 1.84, documentation task generation is skipped silently.

## Testing Task Generation

**Skipped.** No testing readiness template exists at `docs/testing-readiness.md` in the trustify-backend repository. Per constraint 1.86, testing task generation is skipped silently.

---

*This comment was AI-generated by [sdlc-workflow/plan-feature](https://github.com/RHEcosystemAppEng/sdlc-plugins) v0.13.3.*
