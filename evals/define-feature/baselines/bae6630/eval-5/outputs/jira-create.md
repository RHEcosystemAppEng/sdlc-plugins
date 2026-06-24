# Jira Create Issue Call Parameters

## MCP Call: createJiraIssue

```
createJiraIssue(
  cloudId="2b9e35e3-6bd3-4cec-b838-f4249ee02432",
  projectKey="TC",
  issueTypeId="10142",
  summary="Add automated PR review posting for eval results",
  description="## Feature Overview\n\nAdd a CI workflow step that posts eval results as a PR review comment on pull requests that modify skill definitions. When a PR changes a SKILL.md file, the CI pipeline should run the corresponding eval suite and post a summary of pass/fail assertions as a PR review. This gives reviewers immediate visibility into whether skill behavior changes break existing eval expectations.\n\n## Requirements\n\n| Requirement | Notes | Is MVP? |\n|---|---|---|\n| Post eval results as a GitHub PR review when SKILL.md files change | Use the GitHub REST API to create a review with pass/fail summary | Yes |\n| Include per-assertion results in the review body | Format as a Markdown checklist | Yes |\n| Handle the case where no evals exist for the modified skill | Post an informational comment instead of a review | Yes |\n| Update existing PR reviews when re-running evals on the same PR, rather than creating duplicate reviews | Use the GitHub REST API `PUT /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id}` endpoint to update the review body with the latest eval results | Yes |",
  contentFormat="markdown",
  additional_fields={
    "labels": ["ai-generated-jira"]
  }
)
```

### Parameters Breakdown

| Parameter | Value |
|---|---|
| cloudId | `2b9e35e3-6bd3-4cec-b838-f4249ee02432` |
| projectKey | `TC` |
| issueTypeId | `10142` |
| summary | `Add automated PR review posting for eval results` |
| contentFormat | `markdown` |
| labels | `["ai-generated-jira"]` |
| assignee | _(omitted — unassigned)_ |
| priority | _(omitted — skipped)_ |
| fixVersions | _(omitted — skipped)_ |

### Notes

- The assignee field is omitted because the user chose to leave the Feature unassigned.
- The priority field is omitted because the user skipped priority selection.
- The fixVersions field is omitted because the user skipped fixVersion selection.
- The description contains the corrected requirement about updating PR reviews (the original incorrect claim that "PR reviews cannot be updated after initial submission" was replaced with the correct approach using the GitHub REST API update endpoint).
