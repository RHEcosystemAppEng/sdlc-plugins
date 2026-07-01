# Jira create_issue Call Parameters

```
createJiraIssue(
  cloudId="2b9e35e3-6bd3-4cec-b838-f4249ee02432",
  projectKey="TC",
  issueTypeId="10142",
  summary="Add SBOM dependency graph visualization",
  description=<composed Feature description — see preview.md>,
  contentFormat="markdown",
  additional_fields={
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
| cloudId | `2b9e35e3-6bd3-4cec-b838-f4249ee02432` |
| projectKey | `TC` |
| issueTypeId | `10142` |
| summary | `Add SBOM dependency graph visualization` |
| description | Full composed description (all 9 sections) |
| contentFormat | `markdown` |
| labels | `["ai-generated-jira"]` |
| assignee | `{ "accountId": "<current-user-account-id>" }` (self-assigned) |
| priority | `{"name": "Major"}` |
| fixVersions | `[{"name": "1.5.0"}]` |
