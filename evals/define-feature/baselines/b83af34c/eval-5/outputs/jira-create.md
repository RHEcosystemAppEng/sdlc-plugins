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

| Parameter | Value | Source |
|---|---|---|
| cloudId | 2b9e35e3-6bd3-4cec-b838-f4249ee02432 | CLAUDE.md Jira Configuration |
| projectKey | TC | CLAUDE.md Jira Configuration |
| issueTypeId | 10142 | CLAUDE.md Feature issue type ID |
| summary | Add automated PR review posting for eval results | User input |
| contentFormat | markdown | Skill default |
| labels | ai-generated-jira | Skill default |
| assignee | _(not set -- user left unassigned)_ | User choice |
| priority | _(not set -- skipped)_ | No Jira Field Defaults configured; step skipped |
| fixVersions | _(not set -- skipped)_ | No Jira Field Defaults configured; step skipped |

## Description Content

The description field contains the composed Feature description with only the non-skipped sections:

1. **Feature Overview** -- included
2. **Background and Strategic Fit** -- skipped
3. **Goals** -- skipped
4. **Requirements** -- included (with corrected API claim language)
5. **Non-Functional Requirements** -- skipped
6. **Use Cases** -- skipped
7. **Customer Considerations** -- skipped
8. **Customer Information/Supportability** -- skipped
9. **Documentation Considerations** -- skipped
