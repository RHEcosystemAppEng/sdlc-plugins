## Repository
sdlc-plugins

## Target Branch
main

## Description
Fix eval-3 assertion failures related to convention upgrade eligibility evaluation and sub-task creation for review comments classified as suggestions. Two assertions fail because verify-pr does not evaluate convention upgrade eligibility for suggestion-classified review comments and consequently does not create sub-tasks when convention upgrade would elevate the suggestion to a code change request.

The first failing assertion requires that convention upgrade eligibility is evaluated for suggestion-classified review comments -- the classification output must document whether a CONVENTIONS.md lookup or codebase pattern analysis was performed. The second failing assertion requires that the review comment results in a sub-task regardless of classification path -- whether classified directly as a code change request or upgraded from suggestion via convention analysis.

## Files to Modify
- `plugins/sdlc-workflow/skills/verify-pr/style-conventions.md` -- ensure Check 1 (Convention Upgrade) instructions explicitly require documenting the convention lookup process and its outcome for every suggestion, even when no matching convention is found
- `plugins/sdlc-workflow/skills/verify-pr/SKILL.md` -- ensure Step 6b convention upgrade processing and Step 6d sub-task creation handle the case where convention analysis elevates a suggestion to a code change request

## Implementation Notes
- The eval-3 failures indicate that when a review comment is classified as a suggestion, the convention upgrade check (Check 1 in style-conventions.md) either does not run or does not document its reasoning in the output
- The convention upgrade check must always produce visible evidence of its analysis: what conventions were searched, whether any matched, and the upgrade decision -- even when the result is "no matching convention found, suggestion remains as-is"
- When convention analysis does find a match, the suggestion must be upgraded to a code change request, which then triggers sub-task creation in Step 6d
- Review the existing Check 1 instructions (1a through 1d) to ensure they mandate documentation of the lookup process in the classification output file

## Acceptance Criteria
- [ ] Convention upgrade eligibility is evaluated and documented for every suggestion-classified review comment
- [ ] The classification output (review-N.md or equivalent) includes evidence of CONVENTIONS.md lookup and/or codebase pattern analysis for suggestions
- [ ] When convention upgrade elevates a suggestion to code change request, a sub-task is created
- [ ] eval-3 assertions pass after the fix

## Test Requirements
- [ ] Verify that a suggestion-classified comment triggers convention upgrade analysis with documented reasoning
- [ ] Verify that a suggestion matching a documented convention is upgraded and results in sub-task creation
- [ ] Verify that a suggestion with no matching convention remains a suggestion with documented reasoning

## Review Context
The following eval assertions failed in eval-3:

- **Assertion:** "Convention upgrade eligibility is evaluated for review comment 30002 (index suggestion) -- the review classification output (review-30002.md) or the report's Style/Conventions analysis explains whether the suggestion matches a documented or demonstrated project convention"
  **Evidence:** "The output file review-30002.md classifies the comment as a suggestion but does not evaluate convention upgrade eligibility -- no CONVENTIONS.md lookup or codebase pattern analysis is documented in the classification reasoning"

- **Assertion:** "Review comment 30002 (index suggestion) results in a sub-task regardless of classification path -- whether classified directly as code change request based on reviewer language, or upgraded from suggestion via convention analysis"
  **Evidence:** "No sub-task was created for review comment 30002 -- it was classified as suggestion and no convention upgrade was attempted, so the suggestion was not elevated to a code change request"

## Target PR
https://github.com/mrizzi/sdlc-plugins/pull/747
