# Feature Preview

## Step 0 — Project Configuration Validation

- Repository Registry: present (trustify-backend)
- Jira Configuration: present — Project key `TC`, Cloud ID `2b9e35e3-6bd3-4cec-b838-f4249ee02432`, Feature issue type ID `10142`
- Code Intelligence: present
- Jira Field Defaults: absent, so the defaults apply (Default priority: none; Prompt for priority: true; Prompt for fixVersion: true)

## Metadata

- **Summary (title):** Add automated PR review posting for eval results
- **Priority:** Not set (the priority/fixVersion lookup via `getJiraIssueTypeMetaWithFields` was not run in this eval, and the user made no selection)
- **Fix Version:** Not set
- **Assignee:** Unassigned
- **Labels:** `ai-generated-jira`

> **Unverified external API claim:** Requirement row 4 says GitHub PR reviews cannot be updated after submission. Web tools were unavailable, so this could not be checked against the GitHub REST API documentation. The original wording is kept below. Verify it manually before planning (see api-claim-verification.md).

## Description

---

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

## Sections

- **Included:** Feature Overview, Requirements
- **Skipped (omitted):** Background and Strategic Fit, Goals, Non-Functional Requirements, Use Cases (User Experience & Workflow), Customer Considerations, Customer Information/Supportability, Documentation Considerations

> "Ready to create this Feature in Jira? You can also request changes to any section before I create it."
