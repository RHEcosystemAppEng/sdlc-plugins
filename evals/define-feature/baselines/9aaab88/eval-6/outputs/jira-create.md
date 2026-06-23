# Jira Create Parameters

**API Call**: `mcp__jira__create_issue`

## Parameters

```json
{
  "project_key": "TC",
  "issue_type_id": "10142",
  "summary": "Add automated PR review posting for eval results",
  "description": "## Feature Overview\n\nAdd a CI workflow step that posts eval results as a PR review comment on pull requests that modify skill definitions. When a PR changes a SKILL.md file, the CI pipeline should run the corresponding eval suite and post a summary of pass/fail assertions as a PR review. This gives reviewers immediate visibility into whether skill behavior changes break existing eval expectations.\n\n## Requirements\n\n| Requirement | Notes | Is MVP? |\n|---|---|---|\n| Post eval results as a GitHub PR review when SKILL.md files change | Use the GitHub REST API to create a review with pass/fail summary | Yes |\n| Include per-assertion results in the review body | Format as a Markdown checklist | Yes |\n| Handle the case where no evals exist for the modified skill | Post an informational comment instead of a review | Yes |\n| PR reviews cannot be updated after initial submission so always create a new review | The GitHub API does not support modifying a submitted review | Yes |\n\n> **Note**: The requirement \"PR reviews cannot be updated after initial submission so always create a new review\" contains an external API claim that could not be verified (web tools unavailable). The original wording has been retained as-is.",
  "assignee": null
}
```

## Derived From

- **Cloud ID**: 2b9e35e3-6bd3-4cec-b838-f4249ee02432
- **CLAUDE.md**: /home/runner/work/sdlc-plugins/sdlc-plugins/evals/define-feature/files/claude-md-configured.md
