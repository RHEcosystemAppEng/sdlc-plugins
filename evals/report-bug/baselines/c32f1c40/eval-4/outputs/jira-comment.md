# Jira Comment

**Tool**: `mcp__jira__add_comment`

**Comment body**:

Bug report filed with the following sections:

- **Issue Description** -- Overview of the DELETE endpoint returning 200 without removing the SBOM record
- **Steps to Reproduce** -- 6-step reproduction sequence using the SBOM create/delete/get API flow
- **Expected Result** -- DELETE should remove the record; subsequent GET should return 404
- **Actual Result** -- DELETE returns 200 but record persists; GET still returns data
- **Environment / Version** -- RHTPA 1.4.0 on OpenShift 4.14 with PostgreSQL 15.4
- **Attachments** -- API request/response logs from verify-pr test run
- **Suggested Fix** -- Check `rows_affected` return value in the delete handler

*Created with [sdlc-workflow/report-bug](https://github.com/RHEcosystemAppEng/sdlc-plugins) v0.13.10*
