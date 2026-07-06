# Jira Create Issue Parameters

```
createJiraIssue(
  cloudId="2b9e35e3-6bd3-4cec-b838-f4249ee02432",
  projectKey="TC",
  issueTypeId="10142",
  summary="Add automated PR review posting for eval results",
  description=<composed-description>,
  contentFormat="markdown",
  additional_fields={
    "labels": ["ai-generated-jira"]
  }
)
```

## Parameter Details

| Parameter | Value |
|---|---|
| Cloud ID | `2b9e35e3-6bd3-4cec-b838-f4249ee02432` |
| Project Key | `TC` |
| Issue Type ID | `10142` |
| Summary | Add automated PR review posting for eval results |
| Content Format | markdown |
| Labels | `ai-generated-jira` |
| Assignee | Unassigned |
| Priority | Not set (skipped) |
| Fix Version | Not set (skipped) |

## Notes

- The Feature is left **unassigned** per the user's choice, so no `assignee` field is included in `additional_fields`.
- Priority and fixVersion were not selected, so they are omitted from `additional_fields`.
- The description contains only the two required sections (Feature Overview and Requirements); all other sections were skipped and omitted.
