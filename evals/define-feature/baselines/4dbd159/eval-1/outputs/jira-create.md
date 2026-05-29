# Jira create_issue Call Parameters

## Parameters

- **cloudId**: `2b9e35e3-6bd3-4cec-b838-f4249ee02432`
- **projectKey**: `TC`
- **issueTypeId**: `10142`
- **summary**: `Add SBOM dependency graph visualization`
- **contentFormat**: `markdown`
- **description**: *(full composed description as shown in preview.md)*

## additional_fields

```json
{
  "labels": ["ai-generated-jira"],
  "assignee": {
    "accountId": "<current-user-account-id>"
  }
}
```

## Full MCP Call

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
    "assignee": { "accountId": "<current-user-account-id>" }
  }
)
```

## Notes

- **Assignee**: Self-assigned (the current user's accountId would be retrieved via `atlassianUserInfo()` at runtime)
- **Labels**: `ai-generated-jira` applied as required by the skill
- **Issue type ID**: `10142` (Feature) as configured in CLAUDE.md Jira Configuration
- **Project key**: `TC` as configured in CLAUDE.md Jira Configuration
