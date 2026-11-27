# Feature Preview

- **Summary (title):** Add automated PR review posting for eval results
- **Priority:** Not set
- **Fix Version:** Not set
- **Assignee:** Unassigned
- **Labels:** `ai-generated-jira`

> Note: The CLAUDE.md has no `### Jira Field Defaults` subsection, so priority and fixVersion prompts default to enabled; the user input provided no selection for either, so both were skipped.

## Description

## Feature Overview

Add a CI workflow step that posts eval results as a PR review comment on pull requests that modify skill definitions. When a PR changes a SKILL.md file, the CI pipeline should run the corresponding eval suite and post a summary of pass/fail assertions as a PR review. This gives reviewers immediate visibility into whether skill behavior changes break existing eval expectations.

## Requirements

| Requirement | Notes | Is MVP? |
|---|---|---|
| Post eval results as a GitHub PR review when SKILL.md files change | Use the GitHub REST API to create a review with pass/fail summary | Yes |
| Include per-assertion results in the review body | Format as a Markdown checklist | Yes |
| Handle the case where no evals exist for the modified skill | Post an informational comment instead of a review | Yes |
| When re-running evals on a PR, update the existing eval-results review rather than always creating a new one | The GitHub REST API supports updating a submitted review's body via `PUT /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id}` | Yes |

---

Sections omitted (skipped by user): Background and Strategic Fit, Goals, Non-Functional Requirements, Use Cases (User Experience & Workflow), Customer Considerations, Customer Information/Supportability, Documentation Considerations.

> Ready to create this Feature in Jira? You can also request changes to any section before I create it.

**Simulated user response:** Approved.
