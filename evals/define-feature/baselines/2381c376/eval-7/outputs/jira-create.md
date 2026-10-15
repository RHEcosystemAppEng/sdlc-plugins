# Jira Create Issue Parameters

```
createJiraIssue(
  cloudId="2b9e35e3-6bd3-4cec-b838-f4249ee02432",
  projectKey="TC",
  issueTypeId="10142",
  summary="Add bulk SBOM delete endpoint",
  description="## Feature Overview\n\nAdd a bulk delete endpoint for SBOMs that allows users to delete multiple\nSBOMs in a single API call. Currently users must delete SBOMs one at a\ntime, which is impractical when cleaning up hundreds of test or outdated\nSBOMs. The endpoint should accept a list of SBOM IDs and return a summary\nof which deletions succeeded and which failed.\n\n## Requirements\n\n| Requirement | Notes | Is MVP? |\n|---|---|---|\n| `DELETE /api/v2/sboms/bulk` accepts a JSON array of SBOM IDs | Maximum 100 IDs per request | Yes |\n| Return a response with per-ID success/failure status | Include error reason for each failed deletion | Yes |\n| Require the same permissions as single SBOM delete | Reuse existing authorization checks | Yes |\n| Validate all IDs before starting deletions | Return 400 if any ID is malformed | Yes |",
  contentFormat="markdown",
  additional_fields={
    "labels": ["ai-generated-jira"],
    "priority": {"name": "Normal"}
  }
)
```

## Notes

- **Priority** is set to `Normal` — applied silently from the `### Jira Field Defaults` configuration (`Default priority: Normal`, `Prompt for priority: false`).
- **fixVersions** is omitted from `additional_fields` — no default fixVersion is configured and `Prompt for fixVersion: false` suppresses the prompt, so the field is left unset.
- **Assignee** is omitted — the user chose to leave the Feature unassigned.
- **Skipped sections** (Background and Strategic Fit, Goals, Non-Functional Requirements, Use Cases, Customer Considerations, Customer Information/Supportability, Documentation Considerations) are excluded from the description entirely.
