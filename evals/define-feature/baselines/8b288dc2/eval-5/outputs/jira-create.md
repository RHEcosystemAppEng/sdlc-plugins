# Jira Create Issue Parameters

```json
{
  "projectKey": "TC",
  "issueTypeId": "10142",
  "summary": "Add automated PR review posting for eval results",
  "labels": ["ai-generated-jira"],
  "description": "## Feature Overview\n\nAdd a CI workflow step that posts eval results as a PR review comment on pull requests that modify skill definitions. When a PR changes a SKILL.md file, the CI pipeline should run the corresponding eval suite and post a summary of pass/fail assertions as a PR review. This gives reviewers immediate visibility into whether skill behavior changes break existing eval expectations.\n\n## Requirements\n\n| Requirement | Notes | Is MVP? |\n|---|---|---|\n| Post eval results as a GitHub PR review when SKILL.md files change | Use the GitHub REST API to create a review with pass/fail summary | Yes |\n| Include per-assertion results in the review body | Format as a Markdown checklist | Yes |\n| Handle the case where no evals exist for the modified skill | Post an informational comment instead of a review | Yes |\n| Update the existing PR review when re-running evals on the same PR; create a new review only if no prior eval review exists | Use `PUT /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id}` to update an existing review, or `POST` to create a new one if none exists | Yes |"
}
```

**Notes**:
- No assignee specified (user left the Feature unassigned)
- Labels include `ai-generated-jira` as required
- Description contains the corrected requirement language (original incorrect API claim has been fixed)
