# Jira create_issue call (simulated)

Step 6.1: the issue type name would be resolved via `getJiraProjectIssueTypesMetadata(cloudId="2b9e35e3-6bd3-4cec-b838-f4249ee02432", projectKey="TC")`, matching ID `10142` (Feature).

Step 6.2:

```
createJiraIssue(
  cloudId="2b9e35e3-6bd3-4cec-b838-f4249ee02432",
  projectKey="TC",
  issueTypeId="10142",
  summary="Add automated PR review posting for eval results",
  contentFormat="markdown",
  description=<see below>,
  additional_fields={ "labels": ["ai-generated-jira"] }
)
```

- `assignee`: omitted (the user left the Feature unassigned)
- `priority`: omitted (not selected)
- `fixVersions`: omitted (not selected)

## description

```markdown
## Feature Overview

Add a CI workflow step that posts eval results as a PR review comment on pull requests that modify skill definitions. When a PR changes a SKILL.md file, the CI pipeline should run the corresponding eval suite and post a summary of pass/fail assertions as a PR review. This gives reviewers immediate visibility into whether skill behavior changes break existing eval expectations.

## Requirements

| Requirement | Notes | Is MVP? |
|---|---|---|
| Post eval results as a GitHub PR review when SKILL.md files change | Use the GitHub REST API to create a review with pass/fail summary | Yes |
| Include per-assertion results in the review body | Format as a Markdown checklist | Yes |
| Handle the case where no evals exist for the modified skill | Post an informational comment instead of a review | Yes |
| Update the existing eval-results PR review on subsequent CI runs rather than creating a new review each time | The GitHub REST API supports updating a submitted review's body via `PUT /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id}` ([docs](https://docs.github.com/en/rest/pulls/reviews#update-a-review-for-a-pull-request)) | Yes |
```

Simulated result: created issue key `TC-XXXX` (placeholder).
