# Jira create_issue Parameters

```json
{
  "project": "TC",
  "issuetype": "10142",
  "summary": "Add automated PR review posting for eval results",
  "description": "## Feature Overview\n\nAdd a CI workflow step that posts eval results as a PR review comment on pull requests that modify skill definitions. When a PR changes a SKILL.md file, the CI pipeline should run the corresponding eval suite and post a summary of pass/fail assertions as a PR review. This gives reviewers immediate visibility into whether skill behavior changes break existing eval expectations.\n\n## Requirements\n\n| Requirement | Notes | Is MVP? |\n|---|---|---|\n| Post eval results as a GitHub PR review when SKILL.md files change | Use the GitHub REST API to create a review with pass/fail summary | Yes |\n| Include per-assertion results in the review body | Format as a Markdown checklist | Yes |\n| Handle the case where no evals exist for the modified skill | Post an informational comment instead of a review | Yes |\n| Update the existing eval review when re-running, or create a new review if none exists | Use PUT /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id} to update a previously submitted review; create a new review only on the first run | Yes |",
  "labels": ["ai-generated-jira"]
}
```

**Notes:**
- No assignee set (user left unassigned)
- No priority set (user skipped)
- No fixVersions set (user skipped)
