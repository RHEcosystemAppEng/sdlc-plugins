# Feature Preview

**Summary (title):** Add automated PR review posting for eval results

**Priority:** Not set
**Fix Version:** Not set
**Assignee:** Unassigned
**Labels:** `ai-generated-jira`

> Note: The priority and fixVersion prompts were enabled. The claude-md-configured.md file has no `### Jira Field Defaults` subsection, so the defaults apply and both prompts are shown. The available values could not be fetched because Jira access was simulated. Both fields were skipped, so they are left unset.

> **Unverified API claim:** Requirement row 4 contains a claim about the GitHub REST API: "PR reviews cannot be updated after initial submission". It could not be verified because web tools were unavailable. See api-claim-verification.md. Verify it manually before planning.

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
| PR reviews cannot be updated after initial submission so always create a new review | The GitHub API does not support modifying a submitted review | Yes |

---

**Sections included:** Feature Overview, Requirements
**Sections skipped (omitted):** Background and Strategic Fit, Goals, Non-Functional Requirements, Use Cases (User Experience & Workflow), Customer Considerations, Customer Information/Supportability, Documentation Considerations

> "Ready to create this Feature in Jira? You can also request changes to any section before I create it."
