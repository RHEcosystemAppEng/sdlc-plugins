# Jira Create Issue Parameters

```
createJiraIssue(
  cloudId="2b9e35e3-6bd3-4cec-b838-f4249ee02432",
  projectKey="TC",
  issueTypeId="10142",
  summary="Add automated PR review posting for eval results",
  description=<composed description from preview>,
  contentFormat="markdown",
  additional_fields={
    "labels": ["ai-generated-jira"]
  }
)
```

## Parameters

- **projectKey:** TC
- **issueTypeId:** 10142
- **summary:** Add automated PR review posting for eval results
- **labels:** ["ai-generated-jira"]
- **assignee:** unassigned (no assignee field included)
- **contentFormat:** markdown

## Notes

- The assignee field is omitted because the user chose to leave the Feature unassigned.
- The description contains only the non-skipped sections: Feature Overview and Requirements.
- The Requirements section reflects the corrected language after External API Claim Verification (the incorrect claim about GitHub PR reviews not being updatable was replaced with accurate information about the update review endpoint).
