# Feature Preview

- **Summary (title):** Add automated PR review posting for eval results
- **Priority:** Not set
- **Fix Version:** Not set
- **Assignee:** Unassigned
- **Labels:** `ai-generated-jira`

Note: The project CLAUDE.md has no `### Jira Field Defaults` subsection, so priority and fixVersion prompts default to enabled; in this simulated run no selections were made (both skipped).

## Description

## Feature Overview

Add a CI workflow step that posts eval results as a PR review comment on pull requests that modify skill definitions. When a PR changes a SKILL.md file, the CI pipeline should run the corresponding eval suite and post a summary of pass/fail assertions as a PR review. This gives reviewers immediate visibility into whether skill behavior changes break existing eval expectations.

## Requirements

| Requirement | Notes | Is MVP? |
|---|---|---|
| Post eval results as a GitHub PR review when SKILL.md files change | Use the GitHub REST API to create a review with pass/fail summary | Yes |
| Include per-assertion results in the review body | Format as a Markdown checklist | Yes |
| Handle the case where no evals exist for the modified skill | Post an informational comment instead of a review | Yes |
| On subsequent CI runs, update the existing eval-results PR review instead of creating a new one | Use `PUT /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id}` to update the body of the previously posted review ([GitHub docs](https://docs.github.com/en/rest/pulls/reviews#update-a-review-for-a-pull-request)) | Yes |

---

Sections skipped (omitted): Background and Strategic Fit, Goals, Non-Functional Requirements, Use Cases, Customer Considerations, Customer Information/Supportability, Documentation Considerations.

> Ready to create this Feature in Jira? You can also request changes to any section before I create it.
