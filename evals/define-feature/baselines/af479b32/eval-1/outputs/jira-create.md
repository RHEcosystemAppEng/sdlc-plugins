# Jira create_issue Call Parameters

```
createJiraIssue(
  cloudId="2b9e35e3-6bd3-4cec-b838-f4249ee02432",
  projectKey="TC",
  issueTypeId="10142",
  summary="Add SBOM dependency graph visualization",
  description=<composed-description>,
  contentFormat="markdown",
  additional_fields={
    "labels": ["ai-generated-jira"],
    "assignee": { "accountId": "<user-account-id>" },
    "priority": { "name": "Major" },
    "fixVersions": [{ "name": "1.5.0" }]
  }
)
```

## Parameter Details

| Parameter | Value |
|---|---|
| cloudId | `2b9e35e3-6bd3-4cec-b838-f4249ee02432` |
| projectKey | `TC` |
| issueTypeId | `10142` |
| summary | `Add SBOM dependency graph visualization` |
| contentFormat | `markdown` |
| labels | `["ai-generated-jira"]` |
| assignee | `{ "accountId": "<user-account-id>" }` (self-assignment) |
| priority | `{ "name": "Major" }` |
| fixVersions | `[{ "name": "1.5.0" }]` |

## Description

The `description` field contains the full composed Feature description with all 9 sections in markdown format (as shown in preview.md), using `contentFormat="markdown"` for automatic conversion.

## Notes

- The assignee `accountId` would be retrieved from `atlassianUserInfo()` at runtime
- All 9 sections are included in the description (none were skipped)
- Priority "Major" is included in `additional_fields` as selected by the user
- fixVersion "1.5.0" is included in `additional_fields` as selected by the user
