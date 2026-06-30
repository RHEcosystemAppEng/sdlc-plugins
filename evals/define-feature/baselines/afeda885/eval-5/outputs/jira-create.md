# Jira Create Issue Call Parameters

## MCP Call

```
createJiraIssue(
  cloudId="2b9e35e3-6bd3-4cec-b838-f4249ee02432",
  projectKey="TC",
  issueTypeId="10142",
  summary="Add automated PR review posting for eval results",
  description=<see description below>,
  contentFormat="markdown",
  additional_fields={
    "labels": ["ai-generated-jira"]
  }
)
```

**Notes:**
- Project key: **TC** (from Jira Configuration)
- Cloud ID: **2b9e35e3-6bd3-4cec-b838-f4249ee02432** (from Jira Configuration)
- Feature issue type ID: **10142** (from Jira Configuration)
- Assignee is omitted because the user left the Feature unassigned
- Priority is omitted because it was not set
- fixVersions is omitted because it was not set

## Description (Markdown)

```markdown
## Feature Overview

Add a CI workflow step that posts eval results as a PR review comment on pull requests that modify skill definitions. When a PR changes a SKILL.md file, the CI pipeline should run the corresponding eval suite and post a summary of pass/fail assertions as a PR review. This gives reviewers immediate visibility into whether skill behavior changes break existing eval expectations.

## Requirements

| Requirement | Notes | Is MVP? |
|---|---|---|
| Post eval results as a GitHub PR review when SKILL.md files change | Use the GitHub REST API to create a review with pass/fail summary | Yes |
| Include per-assertion results in the review body | Format as a Markdown checklist | Yes |
| Handle the case where no evals exist for the modified skill | Post an informational comment instead of a review | Yes |
| Update existing eval review on subsequent runs instead of creating duplicate reviews | Use PUT /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id} to update a previously submitted review | Yes |
```
