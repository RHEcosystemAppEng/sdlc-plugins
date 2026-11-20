# Feature Preview

**Summary (title):** Add automated PR review posting for eval results

**Priority:** Not set
**Fix Version:** Not set
**Assignee:** Unassigned
**Labels:** `ai-generated-jira`

> Note: No `### Jira Field Defaults` subsection exists in the project CLAUDE.md, so both the priority and fixVersion prompts were shown (defaults: no default priority, prompt for both). The user skipped both.

> **Unverified external API claim:** Requirement row 4 says GitHub PR reviews cannot be updated after submission. This could not be verified (web tools unavailable). The user chose to keep the wording as-is. Check it manually against the GitHub REST API documentation before planning.

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
**Sections skipped:** Background and Strategic Fit, Goals, Non-Functional Requirements, Use Cases, Customer Considerations, Customer Information/Supportability, Documentation Considerations

> "Ready to create this Feature in Jira? You can also request changes to any section before I create it."

**User response (simulated):** Approved.
