# Jira Create Call (simulated — not executed)

## Step 6.1 — Resolve issue type name

```
getJiraProjectIssueTypesMetadata(
  cloudId="2b9e35e3-6bd3-4cec-b838-f4249ee02432",
  projectKey="TC"
)
```
Look up the issue type with ID `10142` (Feature).

## Step 6.2 — Create the Feature

```
createJiraIssue(
  cloudId="2b9e35e3-6bd3-4cec-b838-f4249ee02432",
  projectKey="TC",
  issueTypeId="10142",
  summary="Add automated PR review posting for eval results",
  contentFormat="markdown",
  additional_fields={
    "labels": ["ai-generated-jira"]
  },
  description=<see below>
)
```

- `assignee`: omitted (user left the Feature unassigned)
- `priority`: omitted (not selected)
- `fixVersions`: omitted (not selected)

### description

```markdown
## Feature Overview

Add a CI workflow step that posts eval results as a PR review comment on pull requests that modify skill definitions. When a PR changes a SKILL.md file, the CI pipeline should run the corresponding eval suite and post a summary of pass/fail assertions as a PR review. This gives reviewers immediate visibility into whether skill behavior changes break existing eval expectations.

## Requirements

| Requirement | Notes | Is MVP? |
|---|---|---|
| Post eval results as a GitHub PR review when SKILL.md files change | Use the GitHub REST API to create a review with pass/fail summary | Yes |
| Include per-assertion results in the review body | Format as a Markdown checklist | Yes |
| Handle the case where no evals exist for the modified skill | Post an informational comment instead of a review | Yes |
| PR reviews cannot be updated after initial submission so always create a new review | The GitHub API does not support modifying a submitted review | Yes |
```

**Simulated result:** issue key `TC-XXXX` (placeholder, since no real issue was created).
