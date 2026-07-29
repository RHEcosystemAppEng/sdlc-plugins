# Jira Create Issue Parameters

## MCP Call

```
createJiraIssue(
  cloudId="2b9e35e3-6bd3-4cec-b838-f4249ee02432",
  projectKey="TC",
  issueTypeId="10142",
  summary="Add automated PR review posting for eval results",
  description="## Feature Overview\n\nAdd a CI workflow step that posts eval results as a PR review comment on pull requests that modify skill definitions. When a PR changes a SKILL.md file, the CI pipeline should run the corresponding eval suite and post a summary of pass/fail assertions as a PR review. This gives reviewers immediate visibility into whether skill behavior changes break existing eval expectations.\n\n## Requirements\n\n| Requirement | Notes | Is MVP? |\n|---|---|---|\n| Post eval results as a GitHub PR review when SKILL.md files change | Use the GitHub REST API to create a review with pass/fail summary | Yes |\n| Include per-assertion results in the review body | Format as a Markdown checklist | Yes |\n| Handle the case where no evals exist for the modified skill | Post an informational comment instead of a review | Yes |\n| Update the existing PR review when re-running evals on the same PR | Use PUT /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id} to update the review body instead of creating duplicate reviews | Yes |",
  contentFormat="markdown",
  additional_fields={
    "labels": ["ai-generated-jira"]
  }
)
```

## Parameters Breakdown

| Parameter | Value |
|---|---|
| cloudId | `2b9e35e3-6bd3-4cec-b838-f4249ee02432` |
| projectKey | `TC` |
| issueTypeId | `10142` |
| summary | `Add automated PR review posting for eval results` |
| contentFormat | `markdown` |
| labels | `["ai-generated-jira"]` |
| assignee | _(not set -- user chose unassigned)_ |
| priority | _(not set -- skipped)_ |
| fixVersions | _(not set -- skipped)_ |

## Notes

- The Feature issue type ID (`10142`) and Project key (`TC`) were read from the Jira Configuration in CLAUDE.md.
- The Cloud ID (`2b9e35e3-6bd3-4cec-b838-f4249ee02432`) was read from the Jira Configuration in CLAUDE.md.
- No assignee is included because the user chose to leave the Feature unassigned.
- Priority and fixVersion are omitted from `additional_fields` because they were not selected.
- The description contains corrected language for the fourth requirement after External API Claim Verification found the original claim about GitHub API limitations to be incorrect.
