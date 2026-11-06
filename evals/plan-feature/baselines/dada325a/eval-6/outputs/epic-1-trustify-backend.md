<!-- Jira creation metadata (simulated): Issue type: Epic (hierarchyLevel 1) | Summary: TC-9006: trustify-backend | Parent: TC-9006 | Simulated key: TC-9101 | Labels: ai-generated-jira | Priority: Major | fixVersions: RHTPA 1.5.0 | Incorporated by: TC-9006 -->

# TC-9006: trustify-backend

Backend work for the vulnerability remediation tracking dashboard (TC-9006). Adds a new remediation module in trustify-backend that computes remediation aggregations from existing SBOM and advisory relationship data (no new tables) and exposes three read-only endpoints: a severity-by-status summary with a 30-day trend (GET /api/v2/remediation/summary), a paginated per-product breakdown (GET /api/v2/remediation/by-product), and a filterable, paginated list of tracked vulnerabilities (GET /api/v2/remediation/vulnerabilities).

Tasks:
- TC-9103 — Task 1: Add remediation module with summary aggregation endpoint
- TC-9104 — Task 2: Add per-product remediation breakdown endpoint
- TC-9105 — Task 3: Add filterable remediation vulnerability list endpoint
