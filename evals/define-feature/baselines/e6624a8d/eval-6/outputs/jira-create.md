# Jira Issue Creation

## API Call (Simulated)

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
- **Content Format:** markdown
- **Labels:** ai-generated-jira
- **Assignee:** Unassigned (omitted from additional_fields)
- **Priority:** Not set (omitted from additional_fields)
- **Fix Version:** Not set (omitted from additional_fields)

## Description Content

The description includes the following sections:

1. **Feature Overview** -- provided by user
2. **Requirements** -- provided by user (contains 4 requirements, all marked MVP)

Skipped sections (omitted from description):
- Background and Strategic Fit
- Goals
- Non-Functional Requirements
- Use Cases
- Customer Considerations
- Customer Information/Supportability
- Documentation Considerations

## Simulated Response

```json
{
  "id": "10001",
  "key": "TC-101",
  "self": "https://jira.example.com/rest/api/3/issue/10001"
}
```

**Note:** This is a simulated response. No actual Jira API call was made.
