# Feature Preview

**Summary (title):** Add automated PR review posting for eval results

**Priority:** Not set

**Fix Version:** Not set

**Assignee:** Unassigned

**Labels:** `ai-generated-jira`

---

## Feature Overview

Add a CI workflow step that posts eval results as a PR review comment on pull requests that modify skill definitions. When a PR changes a SKILL.md file, the CI pipeline should run the corresponding eval suite and post a summary of pass/fail assertions as a PR review. This gives reviewers immediate visibility into whether skill behavior changes break existing eval expectations.

## Requirements

| Requirement | Notes | Is MVP? |
|---|---|---|
| Post eval results as a GitHub PR review when SKILL.md files change | Use the GitHub REST API to create a review with pass/fail summary | Yes |
| Include per-assertion results in the review body | Format as a Markdown checklist | Yes |
| Handle the case where no evals exist for the modified skill | Post an informational comment instead of a review | Yes |
| Update the existing eval review if one was previously posted, or create a new review if none exists | Use `PUT /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id}` to update an existing review | Yes |

> **Note:** Requirement 4 was revised after API claim verification. The original stated that "PR reviews cannot be updated after initial submission" and that "The GitHub API does not support modifying a submitted review." Verification confirmed this claim is incorrect — the GitHub REST API supports `PUT /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id}` to update a submitted review. The requirement was corrected to leverage this capability.
