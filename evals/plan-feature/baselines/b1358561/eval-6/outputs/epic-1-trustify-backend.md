**Issue type:** Epic (level-1 type, discovered in Step 2.5)
**Summary:** TC-9006: trustify-backend
**Parent:** TC-9006
**Placeholder key:** TC-9101
**additional_fields:** labels `["ai-generated-jira"]`, priority `{"name": "Major"}`, fixVersions `[{"name": "RHTPA 1.5.0"}]`

**Description (plain text):**

Backend work for TC-9006 (vulnerability remediation tracking dashboard) in trustify-backend. Adds a remediation domain module that aggregates vulnerability remediation status from existing SBOM and advisory data without new tables, and exposes it through the summary, by-product, vulnerability list and 30-day trend endpoints under /api/v2/remediation, with integration tests. Also includes the New Content documentation task for the dashboard and endpoints.

Tasks: TC-9103 (Task 1), TC-9104 (Task 2), TC-9105 (Task 3), TC-9109 (Task 7, documentation).
