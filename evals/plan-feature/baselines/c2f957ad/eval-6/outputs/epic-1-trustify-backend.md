Summary: TC-9006: trustify-backend
Issue type: Epic (level 1)
Parent: TC-9006
Labels: ai-generated-jira | Priority: Major | fixVersions: RHTPA 1.5.0
Simulated key: TC-9101

Description:
Backend work for the vulnerability remediation tracking dashboard (TC-9006). Adds a remediation module in trustify-backend that computes remediation aggregations from existing advisory and SBOM relationship data (no new tables). It exposes four endpoints: summary by severity and status, per-product breakdown, a filterable vulnerability list, and a 30-day trend. Tasks: (1) remediation aggregation model and service, (2) summary and by-product endpoints, (3) vulnerability list endpoint, (4) trend endpoint.
