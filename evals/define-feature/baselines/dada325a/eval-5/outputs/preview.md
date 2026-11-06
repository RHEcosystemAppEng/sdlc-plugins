# Feature Preview

- **Summary (title):** Add automated PR review posting for eval results
- **Priority:** Not set
- **Fix Version:** Not set
- **Assignee:** Unassigned
- **Labels:** `ai-generated-jira`

## Description

## Feature Overview

Add a CI workflow step that posts eval results as a PR review comment on pull requests that modify skill definitions. When a PR changes a SKILL.md file, the CI pipeline should run the corresponding eval suite and post a summary of pass/fail assertions as a PR review. This gives reviewers immediate visibility into whether skill behavior changes break existing eval expectations.

## Requirements

| Requirement | Notes | Is MVP? |
|---|---|---|
| Post eval results as a GitHub PR review when SKILL.md files change | Use the GitHub REST API to create a review with pass/fail summary | Yes |
| Include per-assertion results in the review body | Format as a Markdown checklist | Yes |
| Handle the case where no evals exist for the modified skill | Post an informational comment instead of a review | Yes |
| Create a new PR review for each eval run rather than editing a previous review | The GitHub REST API does support updating a submitted review's body (`PUT /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id}`), so creating a new review is a design choice, not an API limitation. Updating the existing review in place is a possible alternative. | Yes |

---

Sections skipped (omitted): Background and Strategic Fit, Goals, Non-Functional Requirements, Use Cases, Customer Considerations, Customer Information/Supportability, Documentation Considerations.

Note: The original Requirements row 4 said that submitted GitHub PR reviews cannot be updated. External API Claim Verification found this to be incorrect (see api-claim-verification.md), and the corrected wording above was confirmed by the user (simulated).

> Ready to create this Feature in Jira? You can also request changes to any section before I create it.

**Simulated user response:** Approved.
