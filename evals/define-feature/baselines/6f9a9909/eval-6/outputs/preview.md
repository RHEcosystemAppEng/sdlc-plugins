# Feature Preview

## Summary (Title)

Add automated PR review posting for eval results

## Description

### Feature Overview

Add a CI workflow step that posts eval results as a PR review comment on
pull requests that modify skill definitions. When a PR changes a SKILL.md
file, the CI pipeline should run the corresponding eval suite and post a
summary of pass/fail assertions as a PR review. This gives reviewers
immediate visibility into whether skill behavior changes break existing
eval expectations.

### Requirements

| Requirement | Notes | Is MVP? |
|---|---|---|
| Post eval results as a GitHub PR review when SKILL.md files change | Use the GitHub REST API to create a review with pass/fail summary | Yes |
| Include per-assertion results in the review body | Format as a Markdown checklist | Yes |
| Handle the case where no evals exist for the modified skill | Post an informational comment instead of a review | Yes |
| PR reviews cannot be updated after initial submission so always create a new review | The GitHub API does not support modifying a submitted review -- **UNVERIFIED: web tools unavailable; flagged for manual verification** | Yes |

## Metadata

- **Priority:** Not set
- **Fix Version:** Not set
- **Assignee:** Unassigned
- **Labels:** `ai-generated-jira`

## Sections Included

1. Feature Overview (Required)
4. Requirements (Required)

## Sections Skipped

2. Background and Strategic Fit (Recommended)
3. Goals (Recommended)
5. Non-Functional Requirements (Recommended)
6. Use Cases (Recommended)
7. Customer Considerations (Optional)
8. Customer Information/Supportability (Optional)
9. Documentation Considerations (Optional)

## API Claim Notice

The Requirements section contains an unverified claim about the GitHub REST
API: "The GitHub API does not support modifying a submitted review." This
claim could not be verified because web tools (WebSearch, WebFetch) are
unavailable. The claim is flagged in the requirements table and should be
verified manually before implementation.
