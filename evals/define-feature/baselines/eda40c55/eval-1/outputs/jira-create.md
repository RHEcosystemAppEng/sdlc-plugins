## Jira Create Issue Call

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
    "priority": {"name": "Major"},
    "fixVersions": [{"name": "1.5.0"}]
  }
)
```

### Parameters

| Parameter | Value |
|---|---|
| cloudId | 2b9e35e3-6bd3-4cec-b838-f4249ee02432 |
| projectKey | TC |
| issueTypeId | 10142 |
| summary | Add SBOM dependency graph visualization |
| contentFormat | markdown |
| labels | ai-generated-jira |
| assignee | Self-assigned (accountId from atlassianUserInfo) |
| priority | Major |
| fixVersions | 1.5.0 |
