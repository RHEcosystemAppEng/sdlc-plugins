# Jira create_issue Call Parameters

## MCP Call

```
createJiraIssue(
  cloudId="2b9e35e3-6bd3-4cec-b838-f4249ee02432",
  projectKey="TC",
  issueTypeId="10142",
  summary="Add SBOM dependency graph visualization",
  description=<composed description from all 9 sections — see preview.md>,
  contentFormat="markdown",
  additional_fields={
    "labels": ["ai-generated-jira"],
    "assignee": { "accountId": "<current-user-account-id>" },
    "priority": { "name": "Major" },
    "fixVersions": [{ "name": "1.5.0" }]
  }
)
```

## Parameters Summary

| Parameter | Value |
|---|---|
| Project Key | TC |
| Summary | Add SBOM dependency graph visualization |
| Issue Type ID | 10142 |
| Content Format | markdown |
| Labels | `ai-generated-jira` |
| Assignee | Self (current user's accountId) |
| Priority | Major |
| Fix Versions | 1.5.0 |

## Notes

- The `cloudId` is read from CLAUDE.md Jira Configuration: `2b9e35e3-6bd3-4cec-b838-f4249ee02432`
- The `issueTypeId` is read from CLAUDE.md Jira Configuration (Feature issue type ID): `10142`
- The `projectKey` is read from CLAUDE.md Jira Configuration: `TC`
- The user chose self-assignment, so the `assignee` field is included with the current user's `accountId` (retrieved via `atlassianUserInfo()`)
- Priority is set to "Major" as selected by the user in Step 3.5
- Fix Version is set to "1.5.0" as selected by the user in Step 3.5
- The `ai-generated-jira` label is always included per skill specification
- The description includes all 9 template sections (none were skipped)
