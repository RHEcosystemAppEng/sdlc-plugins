## Repository
sdlc-plugins

## Target Branch
TC-9106

## Description
Fix eval-3 assertion failures related to convention upgrade eligibility evaluation and sub-task creation for review comments classified as suggestions. Two assertions fail because the verify-pr skill does not evaluate convention upgrade eligibility when classifying a suggestion, and consequently does not create a sub-task when the suggestion matches a project convention.

The root cause is that when a review comment is classified as a suggestion, the convention upgrade pipeline (Check 1 in the Style/Conventions sub-agent) must evaluate whether the suggestion matches a documented or demonstrated project convention. If it does, the suggestion should be upgraded to a code change request, which then triggers sub-task creation. Currently, this upgrade evaluation is not being performed or documented in the classification reasoning.

## Files to Modify
- `plugins/sdlc-workflow/skills/verify-pr/style-conventions.md` -- ensure Check 1 (Convention Upgrade) instructions clearly require evaluating every suggestion against CONVENTIONS.md and codebase patterns, and documenting the evaluation reasoning in the output
- `plugins/sdlc-workflow/skills/verify-pr/SKILL.md` -- verify Step 6b (Apply Convention Upgrades) correctly processes upgrade-comment actions and triggers sub-task creation for upgraded suggestions

## Implementation Notes
- The convention upgrade check (Check 1 in style-conventions.md) must evaluate every classified suggestion, not skip evaluation
- The classification output (review-N.md files) must document whether convention upgrade eligibility was assessed, including the CONVENTIONS.md lookup result and any codebase pattern analysis
- When a suggestion matches a documented convention or demonstrated codebase pattern, it must be upgraded to a code change request via an upgrade-comment action
- Upgraded suggestions must flow through the sub-task creation pipeline in Step 6d
- Follow the existing convention upgrade flow: Check 1a (CONVENTIONS.md check) -> Check 1b (codebase patterns) -> Check 1c (performance scrutiny) -> Check 1d (upgrade decision)

## Acceptance Criteria
- [ ] Convention upgrade eligibility is evaluated for every review comment classified as a suggestion
- [ ] The classification reasoning output documents CONVENTIONS.md lookup and codebase pattern analysis for suggestions
- [ ] Suggestions matching documented or demonstrated conventions are upgraded to code change requests
- [ ] Upgraded suggestions result in sub-task creation through the standard pipeline
- [ ] eval-3 assertions pass: convention upgrade eligibility is evaluated and sub-task is created when appropriate

## Test Requirements
- [ ] Verify that a suggestion matching a CONVENTIONS.md pattern is upgraded and produces a sub-task
- [ ] Verify that a suggestion not matching any convention remains classified as suggestion with no sub-task
- [ ] Verify that the classification output includes convention upgrade evaluation reasoning

## Review Context
The following eval-3 assertions failed (classified as regression -- no baseline exists):

**Assertion 1:** "Convention upgrade eligibility is evaluated for review comment 30002 (index suggestion) -- the review classification output (review-30002.md) or the report's Style/Conventions analysis explains whether the suggestion matches a documented or demonstrated project convention"
**Evidence:** "The output file review-30002.md classifies the comment as a suggestion but does not evaluate convention upgrade eligibility -- no CONVENTIONS.md lookup or codebase pattern analysis is documented in the classification reasoning"

**Assertion 2:** "Review comment 30002 (index suggestion) results in a sub-task regardless of classification path -- whether classified directly as code change request based on reviewer language, or upgraded from suggestion via convention analysis"
**Evidence:** "No sub-task was created for review comment 30002 -- it was classified as suggestion and no convention upgrade was attempted, so the suggestion was not elevated to a code change request"

## Target PR
https://github.com/RHEcosystemAppEng/sdlc-plugins/pull/747
