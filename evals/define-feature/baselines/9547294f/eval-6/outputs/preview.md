# Feature Preview: Add automated PR review posting for eval results

**Project**: TC
**Issue Type**: Feature (10142)
**Assignee**: Unassigned

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
| PR reviews cannot be updated after initial submission so always create a new review | The GitHub API does not support modifying a submitted review | Yes |

> **Note**: The requirement "PR reviews cannot be updated after initial submission so always create a new review" contains an unverified claim about the GitHub API. See api-claim-verification.md for details.

---

### Sections Skipped

The following optional/recommended sections were marked SKIP by the user and are omitted:

- Section 2 — Background and Strategic Fit
- Section 3 — Goals
- Section 5 — Non-Functional Requirements
- Section 6 — Use Cases
- Section 7 — Customer Considerations
- Section 8 — Customer Information/Supportability
- Section 9 — Documentation Considerations
