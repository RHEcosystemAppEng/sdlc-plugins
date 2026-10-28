## Repository
sdlc-plugins

## Target Branch
TC-9106

## Description
Fix eval-3 assertion failures in verify-pr related to convention upgrade eligibility evaluation and sub-task creation for review comment 30002. The eval-3 run shows two failing assertions (85% pass rate, 11/13): the convention upgrade eligibility is not being evaluated for suggestions, and no sub-task is created for a suggestion that should be elevated to a code change request via convention upgrade. The verify-pr skill must evaluate whether suggestions match documented or demonstrated project conventions and, when they do, upgrade them to code change requests that trigger sub-task creation.

## Files to Modify
- `plugins/sdlc-workflow/skills/verify-pr/style-conventions.md` -- ensure convention upgrade logic properly evaluates all comments classified as suggestions for upgrade eligibility, documenting the CONVENTIONS.md lookup and/or codebase pattern analysis in the classification reasoning
- `plugins/sdlc-workflow/skills/verify-pr/SKILL.md` -- verify that the sub-task creation flow handles suggestions upgraded via convention analysis the same as directly classified code change requests

## Implementation Notes
- The failing assertions indicate that review comment 30002 (an index suggestion) is classified as a suggestion but the convention upgrade eligibility check is never performed -- the classification output (review-30002.md) contains no evidence of a CONVENTIONS.md lookup or codebase pattern analysis
- The convention upgrade check should examine every suggestion against CONVENTIONS.md entries and demonstrated codebase patterns, and document the analysis in the classification reasoning even when no match is found
- If a suggestion matches a documented convention, it should be upgraded to a code change request, which triggers sub-task creation via the standard code-change-request path
- Review the baseline grading at `evals/verify-pr/baselines/latest/eval-3/grading.json` to understand the expected behavior

## Acceptance Criteria
- [ ] Convention upgrade eligibility is evaluated for all comments classified as suggestions
- [ ] The classification output documents the convention upgrade analysis (CONVENTIONS.md lookup and/or codebase pattern analysis) even when no match is found
- [ ] When a suggestion matches a documented convention, it is upgraded to a code change request
- [ ] Upgraded suggestions trigger sub-task creation through the standard code-change-request flow
- [ ] eval-3 passes with 13/13 assertions (0 failures)

## Test Requirements
- [ ] Verify eval-3 passes with 0 failures after the fix
- [ ] Verify convention upgrade analysis is documented in classification output for all suggestions
- [ ] Verify sub-task is created for suggestions that match documented conventions

## Review Context
**Source:** CI eval results (review ID 40001, eval-3)
**Failing assertions:**

1. **Assertion:** "Convention upgrade eligibility is evaluated for review comment 30002 (index suggestion) -- the review classification output (review-30002.md) or the report's Style/Conventions analysis explains whether the suggestion matches a documented or demonstrated project convention"
   **Evidence:** "The output file review-30002.md classifies the comment as a suggestion but does not evaluate convention upgrade eligibility -- no CONVENTIONS.md lookup or codebase pattern analysis is documented in the classification reasoning"

2. **Assertion:** "Review comment 30002 (index suggestion) results in a sub-task regardless of classification path -- whether classified directly as code change request based on reviewer language, or upgraded from suggestion via convention analysis"
   **Evidence:** "No sub-task was created for review comment 30002 -- it was classified as suggestion and no convention upgrade was attempted, so the suggestion was not elevated to a code change request"

## Target PR
https://github.com/RHEcosystemAppEng/sdlc-plugins/pull/747
