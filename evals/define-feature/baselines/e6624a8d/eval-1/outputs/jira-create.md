# Jira Create Issue Parameters

## MCP Call: `createJiraIssue`

```
createJiraIssue(
  cloudId = "2b9e35e3-6bd3-4cec-b838-f4249ee02432",
  projectKey = "TC",
  issueTypeId = "10142",
  summary = "Add SBOM dependency graph visualization",
  description = <composed description - see preview.md>,
  contentFormat = "markdown",
  additional_fields = {
    "labels": ["ai-generated-jira"],
    "assignee": { "accountId": "<current-user-account-id>" },
    "priority": {"name": "Major"},
    "fixVersions": [{"name": "1.5.0"}]
  }
)
```

## Parameter Details

| Parameter | Value |
|---|---|
| Cloud ID | `2b9e35e3-6bd3-4cec-b838-f4249ee02432` |
| Project Key | `TC` |
| Issue Type ID | `10142` |
| Summary | `Add SBOM dependency graph visualization` |
| Content Format | `markdown` |
| Labels | `["ai-generated-jira"]` |
| Assignee | Self-assigned (current user's accountId via `atlassianUserInfo()`) |
| Priority | `Major` |
| Fix Versions | `["1.5.0"]` |

## Notes

- The assignee `accountId` is obtained from `atlassianUserInfo()` in Step 4. The user chose self-assignment.
- Priority `Major` was selected by the user in Step 3.5.3.
- Fix version `1.5.0` was selected by the user in Step 3.5.4.
- The description field contains the full composed Markdown from all 9 template sections (none were skipped).
