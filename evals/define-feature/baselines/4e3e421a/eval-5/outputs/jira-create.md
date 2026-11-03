# Jira create_issue Call (simulated)

Step 6.1: issue type name resolved via `getJiraProjectIssueTypesMetadata(cloudId="2b9e35e3-6bd3-4cec-b838-f4249ee02432", projectKey="TC")`, matched against ID `10142` (Feature). This was simulated.

Step 3.5: The CLAUDE.md has no `### Jira Field Defaults` subsection, so both prompts were shown (the backward-compatible default). The user skipped priority and fixVersion, so both are left out of `additional_fields`.

Step 4: The user chose to leave the Feature unassigned, so `assignee` is left out.

```
createJiraIssue(
  cloudId="2b9e35e3-6bd3-4cec-b838-f4249ee02432",
  projectKey="TC",
  issueTypeId="10142",
  summary="Add automated PR review posting for eval results",
  contentFormat="markdown",
  additional_fields={ "labels": ["ai-generated-jira"] },
  description=<see below>
)
```

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
| On subsequent eval runs for the same PR, update the existing eval results review rather than always creating a new review | The GitHub REST API supports updating a submitted review's body via `PUT /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id}` ([docs](https://docs.github.com/en/rest/pulls/reviews#update-a-review-for-a-pull-request)) | Yes |
```

Simulated result: created issue `TC-XXXX` (placeholder key used in the comment below).
