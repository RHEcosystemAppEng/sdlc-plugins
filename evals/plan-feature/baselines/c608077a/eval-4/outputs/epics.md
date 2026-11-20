# Epics (Step 5 / 6a.0) — grouping strategy: by-sub-feature (from CLAUDE.md Hierarchy Configuration)

## Epic A
- **Summary:** TC-9004: License compliance report API
- **Issue type:** Epic (level 1, assumed discovered in Step 2.5)
- **Parent:** TC-9004
- **additional_fields:** `{"labels": ["ai-generated-jira"], "priority": {"name": "Major"}, "fixVersions": [{"name": "RHTPA 1.5.0"}]}`
- **Description:** Backend work for the license compliance report in trustify-backend: configurable JSON license policy with a fail-closed loader (Task 1), license report models and SBOM license aggregation service including transitive packages (Task 2), and the GET /api/v2/sbom/{id}/license-report endpoint with integration tests (Task 3).

## Epic B
- **Summary:** TC-9004: License compliance documentation
- **Issue type:** Epic
- **Parent:** TC-9004
- **additional_fields:** `{"labels": ["ai-generated-jira"], "priority": {"name": "Major"}, "fixVersions": [{"name": "RHTPA 1.5.0"}]}`
- **Description:** New content documenting the license report endpoint and the license policy configuration for compliance officers (Task 4).
