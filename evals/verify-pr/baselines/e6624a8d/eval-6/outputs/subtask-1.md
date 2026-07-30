## Repository
sdlc-plugins

## Target Branch
main

## Description
Fix eval-3 assertion failures related to convention upgrade eligibility evaluation and sub-task creation for review comments classified as suggestions. Two assertions in eval-3 fail at 85% pass rate, both concerning review comment 30002 (an index suggestion): the convention upgrade eligibility is not evaluated, and no sub-task is created for the comment.

The verify-pr skill must ensure that all comments classified as suggestions go through the convention upgrade evaluation pipeline (Check 1 in style-conventions.md), and that the classification reasoning documents whether a CONVENTIONS.md lookup or codebase pattern analysis was performed. When convention upgrade analysis determines a suggestion matches a documented or demonstrated convention, the suggestion must be elevated to a code change request and a sub-task must be created.

## Files to Modify
- `plugins/sdlc-workflow/skills/verify-pr/style-conventions.md` -- ensure Check 1 (Convention Upgrade) instructions clearly require evaluating every suggestion and documenting the evaluation result, including when no match is found
- `plugins/sdlc-workflow/skills/verify-pr/SKILL.md` -- ensure Step 6b (Apply Convention Upgrades) and Step 6d (Create Sub-Tasks) handle upgraded suggestions correctly

## Implementation Notes
- The convention upgrade pipeline (Check 1 in style-conventions.md) must evaluate every comment classified as "suggestion" -- not just those that obviously match a convention
- The classification output (review-N.md or equivalent) must document the convention upgrade evaluation: whether CONVENTIONS.md was checked, whether codebase patterns were searched, and what the result was (match found or no match)
- When a suggestion is upgraded to a code change request via convention analysis, a sub-task must be created following the same pipeline as directly-classified code change requests
- Follow the existing Check 1 structure (steps 1a through 1d) in style-conventions.md

## Review Context
The following eval-3 assertions failed:

**Assertion 1:** "Convention upgrade eligibility is evaluated for review comment 30002 (index suggestion) -- the review classification output (review-30002.md) or the report's Style/Conventions analysis explains whether the suggestion matches a documented or demonstrated project convention"
**Evidence:** "The output file review-30002.md classifies the comment as a suggestion but does not evaluate convention upgrade eligibility -- no CONVENTIONS.md lookup or codebase pattern analysis is documented in the classification reasoning"

**Assertion 2:** "Review comment 30002 (index suggestion) results in a sub-task regardless of classification path -- whether classified directly as code change request based on reviewer language, or upgraded from suggestion via convention analysis"
**Evidence:** "No sub-task was created for review comment 30002 -- it was classified as suggestion and no convention upgrade was attempted, so the suggestion was not elevated to a code change request"

## Target PR
https://github.com/RHEcosystemAppEng/sdlc-plugins/pull/747

## Acceptance Criteria
- [ ] Every comment classified as "suggestion" is evaluated for convention upgrade eligibility
- [ ] The classification reasoning documents whether CONVENTIONS.md was checked and whether codebase patterns were analyzed
- [ ] When a suggestion matches a documented or demonstrated convention, it is upgraded to a code change request
- [ ] Upgraded suggestions result in sub-task creation following the standard pipeline
- [ ] eval-3 assertions pass after the fix

## Test Requirements
- [ ] Verify that a suggestion comment with a matching convention is upgraded and produces a sub-task
- [ ] Verify that a suggestion comment without a matching convention remains a suggestion with documented evaluation reasoning
- [ ] Verify that the convention upgrade evaluation is always documented in the classification output
