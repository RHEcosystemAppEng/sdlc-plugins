# Jira create_issue Call (simulated, not executed)

Step 3.5: The CLAUDE.md has no `### Jira Field Defaults` subsection, so the skill used the defaults (prompt for priority: true, prompt for fixVersion: true, no default priority). The user skipped both, so `priority` and `fixVersions` are left out.
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
| Create a new PR review for each eval run rather than editing a previous review | The GitHub REST API does support updating a submitted review's body (`PUT /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id}`), so creating a new review is a design choice, not an API limitation. Updating the existing review in place is a possible alternative. | Yes |
```

Simulated result: `TC-XXXX` was created (placeholder key).
