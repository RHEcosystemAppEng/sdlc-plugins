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

- **Project key:** TC
- **Cloud ID:** 2b9e35e3-6bd3-4cec-b838-f4249ee02432
- **Issue type ID:** 10142
- **Summary:** Add automated PR review posting for eval results
- **Labels:** ["ai-generated-jira"]
- **Assignee:** (none -- left unassigned)
- **Priority:** (not set -- skipped)
- **Fix Version:** (not set -- skipped)

## Description Content

The description includes the following sections:
- Feature Overview
- Requirements

Skipped sections (omitted from description):
- Background and Strategic Fit
- Goals
- Non-Functional Requirements
- Use Cases
- Customer Considerations
- Customer Information/Supportability
- Documentation Considerations
