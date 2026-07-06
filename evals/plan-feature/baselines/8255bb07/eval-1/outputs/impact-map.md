# Repository Impact Map

## Feature: TC-9001 — Add advisory severity aggregation endpoint

### trustify-backend

changes:
  - Add AdvisorySeveritySummary response model struct with fields for critical, high, medium, low, and total counts
  - Add severity aggregation service method to SbomService that queries the sbom_advisory join table grouped by severity
  - Add GET /api/v2/sbom/{id}/advisory-summary endpoint with 5-minute cache and optional ?threshold query parameter
  - Add cache invalidation for advisory summaries in the advisory ingestion pipeline when new advisories are linked to an SBOM
  - Add integration tests for the advisory-summary endpoint covering happy path, 404, and threshold filtering

### Excluded requirements

None. All MVP and non-MVP requirements from the feature description can be decomposed into actionable tasks within the trustify-backend repository.

---

## Workflow Mode

**Selected mode:** `direct-to-main`

**Rationale:** No atomicity indicators were identified:

1. **Coordinated schema migrations** — No new database tables or schema changes are required. The feature uses existing advisory-SBOM relationship tables.
2. **Breaking API changes** — The feature adds a new endpoint; no existing API contracts are modified.
3. **Cross-cutting refactors** — No structural changes, renames, or module reorganizations are needed.
4. **Tightly coupled feature components** — All changes are within a single backend repository. No frontend changes are in scope.

Each task PR can land independently on `main` without leaving the codebase in a broken state.

---

## Inherited Field Propagation

The following fields from Feature TC-9001 will be propagated to all created tasks:

| Field | Value | Action |
|---|---|---|
| `priority` | Major | Propagated to all tasks (not "Undefined") |
| `fixVersions` | RHTPA 1.5.0 | Propagated to all tasks (fixVersion scope defaults to "both" — no Jira Field Defaults section in CLAUDE.md) |
| `labels` | ai-generated-jira | Applied to all created issues |

### additional_fields for created issues

```json
{
  "labels": ["ai-generated-jira"],
  "priority": {"name": "Major"},
  "fixVersions": [{"name": "RHTPA 1.5.0"}]
}
```
