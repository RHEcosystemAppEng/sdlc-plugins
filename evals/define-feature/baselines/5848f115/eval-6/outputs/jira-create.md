# Jira Issue Creation Request

This file represents the Jira issue that would be created via MCP or REST API.

## API Call Details

**Method:** createJiraIssue (MCP) or `POST /rest/api/3/issue` (REST API)

**Parameters:**

- **cloudId:** 2b9e35e3-6bd3-4cec-b838-f4249ee02432
- **projectKey:** TC
- **issueTypeId:** 10142
- **summary:** Add automated PR review posting for eval results
- **contentFormat:** markdown
- **additional_fields:**
  ```json
  {
    "labels": ["ai-generated-jira"]
  }
  ```

**Note:** Priority, fixVersion, and assignee are omitted because the user skipped priority selection, fix version selection, and left the Feature unassigned.

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
| PR reviews cannot be updated after initial submission so always create a new review | The GitHub API does not support modifying a submitted review (UNVERIFIED) | Yes |
```

## Verification Warning

Requirement 4 contains an unverified claim about the GitHub REST API ("The GitHub API does not support modifying a submitted review"). Web tools were unavailable for verification. This claim is flagged as UNVERIFIED in the description. Manual verification is recommended.
