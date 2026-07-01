# Jira Create Issue Parameters

## API Call: `create_issue`

**Parameters:**

- **project_key:** TC
- **issue_type_id:** 10142
- **summary:** Add automated PR review posting for eval results
- **description:**

```
## Feature Overview

Add a CI workflow step that posts eval results as a PR review comment on
pull requests that modify skill definitions. When a PR changes a SKILL.md
file, the CI pipeline should run the corresponding eval suite and post a
summary of pass/fail assertions as a PR review. This gives reviewers
immediate visibility into whether skill behavior changes break existing
eval expectations.

## Requirements

| Requirement | Notes | Is MVP? |
|---|---|---|
| Post eval results as a GitHub PR review when SKILL.md files change | Use the GitHub REST API to create a review with pass/fail summary | Yes |
| Include per-assertion results in the review body | Format as a Markdown checklist | Yes |
| Handle the case where no evals exist for the modified skill | Post an informational comment instead of a review | Yes |
| PR reviews can be updated after submission using the GitHub REST API (PUT /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id}); prefer updating an existing review over creating a new one to reduce notification noise | Update the existing review when re-running evals on the same PR | Yes |
```

- **assignee:** Unassigned
