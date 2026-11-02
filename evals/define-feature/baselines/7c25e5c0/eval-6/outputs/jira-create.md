# Jira Issue Creation

## MCP Call

```
createJiraIssue(
  cloudId="2b9e35e3-6bd3-4cec-b838-f4249ee02432",
  projectKey="TC",
  issueTypeId="10142",
  summary="Add automated PR review posting for eval results",
  description="## Feature Overview\n\nAdd a CI workflow step that posts eval results as a PR review comment on pull requests that modify skill definitions. When a PR changes a SKILL.md file, the CI pipeline should run the corresponding eval suite and post a summary of pass/fail assertions as a PR review. This gives reviewers immediate visibility into whether skill behavior changes break existing eval expectations.\n\n## Requirements\n\n| Requirement | Notes | Is MVP? |\n|---|---|---|\n| Post eval results as a GitHub PR review when SKILL.md files change | Use the GitHub REST API to create a review with pass/fail summary | Yes |\n| Include per-assertion results in the review body | Format as a Markdown checklist | Yes |\n| Handle the case where no evals exist for the modified skill | Post an informational comment instead of a review | Yes |\n| PR reviews cannot be updated after initial submission so always create a new review | The GitHub API does not support modifying a submitted review | Yes |",
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

## Simulated Response

```json
{
  "id": "10001",
  "key": "TC-101",
  "self": "https://jira.atlassian.com/rest/api/3/issue/10001"
}
```
