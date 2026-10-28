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
| contentFormat | `markdown` |
| labels | `["ai-generated-jira"]` |
| assignee | Self-assigned (current user's accountId) |
| priority | `Major` |
| fixVersions | `[{"name": "1.5.0"}]` |

## Description

The `description` field contains the full composed Feature description with all 9 sections in markdown format (as shown in preview.md).

## Sections Included

1. Feature Overview (Required) -- provided
2. Background and Strategic Fit (Recommended) -- provided
3. Goals (Recommended) -- provided
4. Requirements (Required) -- provided
5. Non-Functional Requirements (Recommended) -- provided
6. Use Cases (Recommended) -- provided
7. Customer Considerations (Optional) -- provided
8. Customer Information/Supportability (Optional) -- provided
9. Documentation Considerations (Optional) -- provided
