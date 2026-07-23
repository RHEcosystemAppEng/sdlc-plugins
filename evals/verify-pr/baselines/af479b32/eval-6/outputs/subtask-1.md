## Repository
sdlc-plugins

## Target Branch
main

## Description
Fix eval-3 assertion failures in the verify-pr eval suite. Two assertions are failing at 85% pass rate (11/13 passed). Both failures relate to convention upgrade eligibility evaluation and sub-task creation for suggestion-classified review comments. The verify-pr skill must properly evaluate convention upgrade eligibility for suggestions and ensure that convention-backed suggestions result in sub-task creation.

## Files to Modify
- `plugins/sdlc-workflow/skills/verify-pr/style-conventions.md` -- ensure Check 1 (Convention Upgrade) properly evaluates all suggestion-classified comments for upgrade eligibility, including CONVENTIONS.md lookup and codebase pattern analysis
- `plugins/sdlc-workflow/skills/verify-pr/SKILL.md` -- ensure Step 6b (Apply Convention Upgrades) and Step 6d (Create Sub-Tasks) correctly process upgraded suggestions into sub-tasks

## Implementation Notes
- The eval-3 scenario involves a review comment (id 30002) classified as a suggestion that proposes an index-related pattern
- The current implementation classifies the comment as a suggestion but does not evaluate convention upgrade eligibility -- no CONVENTIONS.md lookup or codebase pattern analysis is documented in the classification reasoning
- Convention upgrade evaluation must follow the existing Check 1 flow in style-conventions.md: Check CONVENTIONS.md (1a), Check Codebase Patterns (1b), Performance-Related Scrutiny (1c), Upgrade Decision (1d)
- When a suggestion is upgraded to a code change request, it must flow through Step 6d to create a sub-task
- Ensure the classification output (review-N.md files) documents the convention upgrade evaluation reasoning even when the suggestion is not upgraded

## Acceptance Criteria
- [ ] Convention upgrade eligibility is evaluated for all suggestion-classified review comments, with documented reasoning including CONVENTIONS.md lookup and/or codebase pattern analysis
- [ ] Suggestions that match documented or demonstrated conventions are upgraded to code change requests
- [ ] Upgraded suggestions result in sub-task creation through Step 6d
- [ ] Classification output files document the convention upgrade evaluation reasoning

## Test Requirements
- [ ] Verify eval-3 passes with all 13 assertions succeeding
- [ ] Verify that suggestion comments trigger convention upgrade evaluation
- [ ] Verify that convention-backed suggestions produce sub-tasks

## Review Context
The following eval-3 assertions are failing:

**Assertion 1:** "Convention upgrade eligibility is evaluated for review comment 30002 (index suggestion) -- the review classification output (review-30002.md) or the report's Style/Conventions analysis explains whether the suggestion matches a documented or demonstrated project convention"
**Evidence:** "The output file review-30002.md classifies the comment as a suggestion but does not evaluate convention upgrade eligibility -- no CONVENTIONS.md lookup or codebase pattern analysis is documented in the classification reasoning"

**Assertion 2:** "Review comment 30002 (index suggestion) results in a sub-task regardless of classification path -- whether classified directly as code change request based on reviewer language, or upgraded from suggestion via convention analysis"
**Evidence:** "No sub-task was created for review comment 30002 -- it was classified as suggestion and no convention upgrade was attempted, so the suggestion was not elevated to a code change request"

## Target PR
https://github.com/RHEcosystemAppEng/sdlc-plugins/pull/747
