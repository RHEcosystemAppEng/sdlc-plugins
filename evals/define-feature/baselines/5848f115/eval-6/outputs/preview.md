# Feature Preview

## Summary (Title)

Add automated PR review posting for eval results

## Description

### Feature Overview

Add a CI workflow step that posts eval results as a PR review comment on pull requests that modify skill definitions. When a PR changes a SKILL.md file, the CI pipeline should run the corresponding eval suite and post a summary of pass/fail assertions as a PR review. This gives reviewers immediate visibility into whether skill behavior changes break existing eval expectations.

### Requirements

| Requirement | Notes | Is MVP? |
|---|---|---|
| Post eval results as a GitHub PR review when SKILL.md files change | Use the GitHub REST API to create a review with pass/fail summary | Yes |
| Include per-assertion results in the review body | Format as a Markdown checklist | Yes |
| Handle the case where no evals exist for the modified skill | Post an informational comment instead of a review | Yes |
| PR reviews cannot be updated after initial submission so always create a new review | The GitHub API does not support modifying a submitted review (**UNVERIFIED -- see api-claim-verification.md**) | Yes |

## Metadata

- **Project:** TC
- **Issue Type:** Feature (10142)
- **Priority:** Not set
- **Fix Version:** Not set
- **Assignee:** Unassigned
- **Labels:** ai-generated-jira

## Sections Included

1. Feature Overview (Required) -- provided
2. Requirements (Required) -- provided

## Sections Skipped

- Background and Strategic Fit (Recommended) -- skipped
- Goals (Recommended) -- skipped
- Non-Functional Requirements (Recommended) -- skipped
- Use Cases (Recommended) -- skipped
- Customer Considerations (Optional) -- skipped
- Customer Information/Supportability (Optional) -- skipped
- Documentation Considerations (Optional) -- skipped

## Verification Warnings

- **Unverified API claim** in Requirements section: "The GitHub API does not support modifying a submitted review." Web tools were unavailable; manual verification is recommended before finalizing this Feature.
