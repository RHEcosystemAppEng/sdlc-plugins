# Jira Issue Creation

## API Call

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

## Parameters

- **Cloud ID:** 2b9e35e3-6bd3-4cec-b838-f4249ee02432
- **Project Key:** TC
- **Issue Type ID:** 10142
- **Summary:** Add automated PR review posting for eval results
- **Labels:** ai-generated-jira
- **Assignee:** (none -- left unassigned per user choice)

## Description Content

The description includes the following sections:

- **Feature Overview** (Required) -- included
- **Background and Strategic Fit** (Recommended) -- SKIPPED
- **Goals** (Recommended) -- SKIPPED
- **Requirements** (Required) -- included
- **Non-Functional Requirements** (Recommended) -- SKIPPED
- **Use Cases** (Recommended) -- SKIPPED
- **Customer Considerations** (Optional) -- SKIPPED
- **Customer Information/Supportability** (Optional) -- SKIPPED
- **Documentation Considerations** (Optional) -- SKIPPED

Skipped sections are omitted from the description (no empty headings).
