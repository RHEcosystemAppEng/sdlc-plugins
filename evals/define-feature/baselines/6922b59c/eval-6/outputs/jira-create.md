# Jira Issue Creation

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

**Note:** No `assignee` field is included because the user chose to leave the Feature unassigned. No `priority` or `fixVersions` fields are included because these were not set.

## Description (Markdown)

```markdown
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
| PR reviews cannot be updated after initial submission so always create a new review | The GitHub API does not support modifying a submitted review | Yes |
```

## Configuration Source

| Field | Value | Source |
|---|---|---|
| Cloud ID | `2b9e35e3-6bd3-4cec-b838-f4249ee02432` | CLAUDE.md > Jira Configuration |
| Project Key | `TC` | CLAUDE.md > Jira Configuration |
| Issue Type ID | `10142` | CLAUDE.md > Jira Configuration (Feature issue type ID) |
| Labels | `ai-generated-jira` | Skill default |
| Assignee | _(unassigned)_ | User chose to leave unassigned |
| Priority | _(not set)_ | Skipped |
| Fix Version | _(not set)_ | Skipped |
