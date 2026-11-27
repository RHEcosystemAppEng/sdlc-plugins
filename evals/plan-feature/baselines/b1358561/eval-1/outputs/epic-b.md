Summary: TC-9001: Advisory summary cache invalidation
Issue type: Epic (level 1)
Parent: TC-9001
additional_fields: {"labels": ["ai-generated-jira"], "priority": {"name": "Major"}, "fixVersions": [{"name": "RHTPA 1.5.0"}]}

Description:
Groups the work that keeps cached advisory severity summaries fresh: invalidating the cached summary for an SBOM whenever advisory ingestion/correlation or SBOM (re-)ingestion changes the SBOM-advisory links in trustify-backend (Task 3).
