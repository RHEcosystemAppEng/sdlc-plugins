# Jira Issue Creation Parameters

```
createJiraIssue(
  cloudId = "2b9e35e3-6bd3-4cec-b838-f4249ee02432",
  projectKey = "TC",
  issueTypeId = "10142",
  summary = "Add automated PR review posting for eval results",
  description = <composed-description>,
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
| Labels | `ai-generated-jira` |
| Assignee | Unassigned |
| Content Format | markdown |

## Notes

- Assignee is left unassigned per user choice.
- The label `ai-generated-jira` is applied as required by the define-feature skill.
- The description contains only the two Required sections (Feature Overview and Requirements) since all other sections were skipped.
