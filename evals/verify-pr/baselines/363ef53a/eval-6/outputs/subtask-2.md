## Repository
sdlc-plugins

## Target Branch
main

## Description
Fix eval-3 assertion failures related to convention upgrade eligibility evaluation and sub-task creation for review comment 30002 (index suggestion). Two assertions fail: (1) convention upgrade eligibility is not evaluated for the comment -- no CONVENTIONS.md lookup or codebase pattern analysis is documented in the classification reasoning, and (2) no sub-task is created for the comment because it was classified as a suggestion without attempting convention upgrade.

## Files to Modify
- `plugins/sdlc-workflow/skills/verify-pr/style-conventions.md` -- ensure Check 1 (Convention Upgrade) logic is applied to all suggestion-classified comments, including those that should be elevated to code change requests when backed by project conventions
- `plugins/sdlc-workflow/skills/verify-pr/SKILL.md` -- verify that Step 6b convention upgrade processing correctly feeds into Step 6d sub-task creation for upgraded suggestions

## Implementation Notes
- The root cause appears to be that review comment 30002 (an index suggestion) was classified as a suggestion but the convention upgrade check (Check 1 in style-conventions.md) did not evaluate it for upgrade eligibility
- The convention upgrade check should perform a CONVENTIONS.md lookup and/or codebase pattern analysis for every suggestion-classified comment, and document the analysis in the classification reasoning output
- When a suggestion matches a documented or demonstrated convention, it must be upgraded to a code change request, which then triggers sub-task creation in Step 6d
- Review the Check 1 steps (1a through 1d) to ensure the upgrade pipeline runs for all suggestion-classified comments without short-circuiting

## Acceptance Criteria
- [ ] Convention upgrade eligibility is evaluated for all suggestion-classified review comments
- [ ] The classification output (review-N.md) documents whether a CONVENTIONS.md lookup or codebase pattern analysis was performed
- [ ] Suggestions that match a documented or demonstrated convention are upgraded to code change requests
- [ ] Upgraded suggestions result in sub-task creation via Step 6d

## Review Context
**Eval ID:** eval-3
**Failing assertions (2):**

1. **Assertion:** "Convention upgrade eligibility is evaluated for review comment 30002 (index suggestion) -- the review classification output (review-30002.md) or the report's Style/Conventions analysis explains whether the suggestion matches a documented or demonstrated project convention"
   **Evidence:** "The output file review-30002.md classifies the comment as a suggestion but does not evaluate convention upgrade eligibility -- no CONVENTIONS.md lookup or codebase pattern analysis is documented in the classification reasoning"

2. **Assertion:** "Review comment 30002 (index suggestion) results in a sub-task regardless of classification path -- whether classified directly as code change request based on reviewer language, or upgraded from suggestion via convention analysis"
   **Evidence:** "No sub-task was created for review comment 30002 -- it was classified as suggestion and no convention upgrade was attempted, so the suggestion was not elevated to a code change request"

## Target PR
https://github.com/RHEcosystemAppEng/sdlc-plugins/pull/747
