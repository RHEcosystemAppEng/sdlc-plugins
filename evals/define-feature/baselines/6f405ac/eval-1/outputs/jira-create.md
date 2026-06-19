# Jira Create Issue Parameters

## MCP Call

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
    "assignee": { "accountId": "<user-account-id>" }
  }
)
```

## Parameters

- **Project key**: TC
- **Summary**: Add SBOM dependency graph visualization
- **Issue type ID**: 10142
- **Description**: The full composed Feature description (all 9 sections as shown in preview.md)
- **Content format**: markdown
- **Labels**: `["ai-generated-jira"]`
- **Assignee**: Self-assigned (user chose self-assignment, so the `assignee` field is included with `{ "accountId": "<user-account-id>" }` obtained from `atlassianUserInfo()`)
