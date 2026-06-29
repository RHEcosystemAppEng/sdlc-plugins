# Feature Preview

| Field | Value |
|---|---|
| **Summary** | Add automated PR review posting for eval results |
| **Project** | TC |
| **Issue Type** | Feature (10142) |
| **Assignee** | Unassigned |
| **Labels** | ai-generated-jira |

---

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
| Update existing eval review on subsequent runs rather than always creating a new review | The GitHub REST API supports updating a submitted review via `PUT /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id}`, so the implementation should update an existing eval review in place when one already exists on the PR, and only create a new review if none exists yet. | Yes |

> **Note — API claim corrected:** The original input stated that "PR reviews cannot be updated after initial submission" and that "The GitHub API does not support modifying a submitted review." This is incorrect. The GitHub REST API supports `PUT /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id}` to update a submitted review. The requirement has been revised accordingly.
