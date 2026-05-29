# Jira create_issue Call Parameters

## MCP Call

```
createJiraIssue(
  cloudId = "2b9e35e3-6bd3-4cec-b838-f4249ee02432",
  projectKey = "TC",
  issueTypeId = "10142",
  summary = "Add SBOM dependency graph visualization",
  description = <composed-description-below>,
  contentFormat = "markdown",
  additional_fields = {
    "labels": ["ai-generated-jira"],
    "assignee": { "accountId": "<current-user-account-id>" }
  }
)
```

## Parameters Detail

| Parameter | Value |
|---|---|
| **Cloud ID** | `2b9e35e3-6bd3-4cec-b838-f4249ee02432` |
| **Project Key** | `TC` |
| **Issue Type ID** | `10142` |
| **Summary** | `Add SBOM dependency graph visualization` |
| **Content Format** | `markdown` |
| **Labels** | `["ai-generated-jira"]` |
| **Assignee** | Self-assigned (current user's `accountId` from `atlassianUserInfo()`) |

## Description (Markdown)

The `description` field contains the full composed Feature description with all 9 sections as rendered in `preview.md`:

- ## Feature Overview
- ## Background and Strategic Fit
- ## Goals
- ## Requirements
- ## Non-Functional Requirements
- ## Use Cases (User Experience & Workflow)
- ## Customer Considerations
- ## Customer Information/Supportability
- ## Documentation Considerations

All sections are included (none were skipped).
