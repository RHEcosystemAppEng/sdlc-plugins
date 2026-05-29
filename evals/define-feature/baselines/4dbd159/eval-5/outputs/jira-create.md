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

- **Cloud ID:** 2b9e35e3-6bd3-4cec-b838-f4249ee02432
- **Project key:** TC
- **Issue type ID:** 10142
- **Summary:** Add automated PR review posting for eval results
- **Content format:** markdown
- **Labels:** ["ai-generated-jira"]
- **Assignee:** Unassigned (no assignee field included)

## Description Content

The description contains the following non-skipped sections:

1. **Feature Overview** -- high-level description of the CI workflow step for posting eval results as PR reviews
2. **Requirements** -- four requirements with corrected language (the original incorrect claim about GitHub API limitations has been corrected based on API claim verification)

Skipped sections (omitted from description):
- Background and Strategic Fit
- Goals
- Non-Functional Requirements
- Use Cases
- Customer Considerations
- Customer Information/Supportability
- Documentation Considerations
