## Repository
sdlc-plugins

## Target Branch
main

## Description
Fix eval-3 assertion failures related to convention upgrade eligibility and sub-task creation for review comment 30002 (index suggestion). Two assertions failed:

1. Convention upgrade eligibility is not evaluated for review comment 30002 — the classification output does not document a CONVENTIONS.md lookup or codebase pattern analysis for the suggestion.
2. Review comment 30002 does not result in a sub-task — it was classified as a suggestion but no convention upgrade was attempted, so it was never elevated to a code change request.

The root cause is that the verify-pr skill classified comment 30002 as a suggestion and did not attempt convention upgrade analysis. The Style/Conventions sub-agent's Check 1 (Convention Upgrade) should evaluate whether the suggestion matches a documented or demonstrated project convention, and if so, upgrade it to a code change request that triggers sub-task creation.

## Files to Modify
- `plugins/sdlc-workflow/skills/verify-pr/style-conventions.md` — review Check 1 (Convention Upgrade) to ensure all suggestions are evaluated for convention upgrade eligibility, with documented reasoning in the output regardless of the upgrade decision

## Implementation Notes
- Check 1 (Convention Upgrade) in `style-conventions.md` defines the process for upgrading suggestions to code change requests based on CONVENTIONS.md matches or codebase patterns
- The eval assertions expect that for every suggestion, the classification output (review-N.md) documents whether convention upgrade eligibility was evaluated — even if the suggestion is not upgraded, the reasoning should be present
- The eval also expects that if a suggestion matches a convention, a sub-task is created (either via direct classification as code change request or via convention upgrade)
- Review the eval-3 test case to understand what review comment 30002 contains and what convention it should match, then ensure the upgrade pipeline processes it correctly

## Review Context
Eval result review from CI (github-actions[bot]):

eval-3: 2 failing assertions:

- **Assertion:** "Convention upgrade eligibility is evaluated for review comment 30002 (index suggestion) — the review classification output (review-30002.md) or the report's Style/Conventions analysis explains whether the suggestion matches a documented or demonstrated project convention"
  **Evidence:** "The output file review-30002.md classifies the comment as a suggestion but does not evaluate convention upgrade eligibility — no CONVENTIONS.md lookup or codebase pattern analysis is documented in the classification reasoning"

- **Assertion:** "Review comment 30002 (index suggestion) results in a sub-task regardless of classification path — whether classified directly as code change request based on reviewer language, or upgraded from suggestion via convention analysis"
  **Evidence:** "No sub-task was created for review comment 30002 — it was classified as suggestion and no convention upgrade was attempted, so the suggestion was not elevated to a code change request"

## Target PR
https://github.com/mrizzi/sdlc-plugins/pull/747

## Acceptance Criteria
- [ ] Convention upgrade eligibility is evaluated and documented for all suggestions, including review comment 30002
- [ ] When a suggestion matches a documented or demonstrated convention, it is upgraded to a code change request
- [ ] Upgraded suggestions result in sub-task creation
- [ ] The review classification output includes reasoning about convention lookup (CONVENTIONS.md check and/or codebase pattern analysis) for every suggestion
- [ ] eval-3 assertions pass after the fix
