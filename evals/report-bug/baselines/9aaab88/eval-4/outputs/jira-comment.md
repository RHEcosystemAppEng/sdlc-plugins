# Jira Comment

Bug report created from programmatic input with the following sections:

- **Issue Description**: Describes the DELETE endpoint returning 200 without actually removing the SBOM record from the database
- **Steps to Reproduce**: 6-step reproduction sequence using the SBOM REST API
- **Expected Result**: DELETE should remove the record; subsequent GET should return 404
- **Actual Result**: DELETE returns 200 but record persists; GET still returns data
- **Attachments**: API request/response logs from verify-pr test run
- **Suggested Fix**: Check `rows_affected` return value in the delete handler and return 404 when zero rows are deleted

---

*Created with [sdlc-workflow/report-bug](https://github.com/mrizzi/sdlc-plugins) v0.11.0*
