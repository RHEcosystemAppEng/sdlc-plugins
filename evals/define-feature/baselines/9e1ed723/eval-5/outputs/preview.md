# Feature Preview

- **Summary (title):** Add automated PR review posting for eval results
- **Priority:** Not set
- **Fix Version:** Not set
- **Assignee:** Unassigned
- **Labels:** `ai-generated-jira`

> Priority and Fix Version: the project CLAUDE.md has no `### Jira Field Defaults` subsection, so both prompts would normally be shown. In this eval no Jira metadata could be fetched, so both are skipped and left unset.
>
> Requirements row 4: the user's original claim ("PR reviews cannot be updated after initial submission" / "The GitHub API does not support modifying a submitted review") was found to be incorrect during External API Claim Verification (see `api-claim-verification.md`). The row below uses the corrected wording the user confirmed.

---

## Description

## Feature Overview

Add a CI workflow step that posts eval results as a PR review comment on pull requests that modify skill definitions. When a PR changes a SKILL.md file, the CI pipeline should run the corresponding eval suite and post a summary of pass/fail assertions as a PR review. This gives reviewers immediate visibility into whether skill behavior changes break existing eval expectations.

## Requirements

| Requirement | Notes | Is MVP? |
|---|---|---|
| Post eval results as a GitHub PR review when SKILL.md files change | Use the GitHub REST API to create a review with pass/fail summary | Yes |
| Include per-assertion results in the review body | Format as a Markdown checklist | Yes |
| Handle the case where no evals exist for the modified skill | Post an informational comment instead of a review | Yes |
| On later eval runs for the same PR, update the review posted earlier instead of creating a new one | The GitHub REST API supports updating a submitted review's body via `PUT /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id}` ([docs](https://docs.github.com/en/rest/pulls/reviews#update-a-review-for-a-pull-request)). Only the body can be changed, not the review state. | Yes |

---

**Sections included:** Feature Overview, Requirements
**Sections skipped:** Background and Strategic Fit, Goals, Non-Functional Requirements, Use Cases (User Experience & Workflow), Customer Considerations, Customer Information/Supportability, Documentation Considerations

> "Ready to create this Feature in Jira? You can also request changes to any section before I create it."

**Simulated user response:** Approved.
