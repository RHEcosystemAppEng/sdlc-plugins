# Feature Preview

- **Summary (title):** Add automated PR review posting for eval results
- **Priority:** Not set
- **Fix Version:** Not set
- **Assignee:** Unassigned
- **Labels:** `ai-generated-jira`

Note: The project CLAUDE.md has no `### Jira Field Defaults` subsection, so both the
priority and fixVersion prompts were shown (defaults: no default priority, prompt both).
The user skipped both.

## Description

## Feature Overview

Add a CI workflow step that posts eval results as a PR review comment on pull requests that modify skill definitions. When a PR changes a SKILL.md file, the CI pipeline should run the corresponding eval suite and post a summary of pass/fail assertions as a PR review. This gives reviewers immediate visibility into whether skill behavior changes break existing eval expectations.

## Requirements

| Requirement | Notes | Is MVP? |
|---|---|---|
| Post eval results as a GitHub PR review when SKILL.md files change | Use the GitHub REST API to create a review with pass/fail summary | Yes |
| Include per-assertion results in the review body | Format as a Markdown checklist | Yes |
| Handle the case where no evals exist for the modified skill | Post an informational comment instead of a review | Yes |
| Always create a new review for each eval run | Design choice, not an API limitation — the GitHub REST API supports updating a submitted review body via `PUT /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id}` ([docs](https://docs.github.com/en/rest/pulls/reviews#update-a-review-for-a-pull-request)); updating the existing review is an available alternative | Yes |

---

Sections included: Feature Overview, Requirements
Sections skipped (omitted): Background and Strategic Fit, Goals, Non-Functional Requirements, Use Cases (User Experience & Workflow), Customer Considerations, Customer Information/Supportability, Documentation Considerations

> Ready to create this Feature in Jira? You can also request changes to any section before I create it.

**Simulated user response:** Approved.
