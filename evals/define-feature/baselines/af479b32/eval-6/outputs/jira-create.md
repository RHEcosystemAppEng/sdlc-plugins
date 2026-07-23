# Jira Issue Creation Parameters

## createJiraIssue Call

```
createJiraIssue(
  cloudId = "2b9e35e3-6bd3-4cec-b838-f4249ee02432",
  projectKey = "TC",
  issueTypeId = "10142",
  summary = "Add automated PR review posting for eval results",
  description = <composed description from preview.md>,
  contentFormat = "markdown",
  additional_fields = {
    "labels": ["ai-generated-jira"]
  }
)
```

## Parameters

| Parameter | Value |
|---|---|
| Cloud ID | `2b9e35e3-6bd3-4cec-b838-f4249ee02432` |
| Project Key | `TC` |
| Issue Type ID | `10142` |
| Summary | Add automated PR review posting for eval results |
| Content Format | markdown |
| Labels | `ai-generated-jira` |
| Assignee | Unassigned (not included in additional_fields) |
| Priority | Not set (omitted from additional_fields) |
| Fix Version | Not set (omitted from additional_fields) |

## Description Content

The description includes the following sections:

- **Feature Overview** -- included
- **Requirements** -- included (4 rows, all MVP)

Skipped sections (omitted from description):

- Background and Strategic Fit
- Goals
- Non-Functional Requirements
- Use Cases
- Customer Considerations
- Customer Information/Supportability
- Documentation Considerations
