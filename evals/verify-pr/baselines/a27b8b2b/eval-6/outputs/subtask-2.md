## Repository
sdlc-plugins

## Target Branch
main

## Description
Fix eval-3 assertion failures related to convention upgrade eligibility evaluation and sub-task creation for review comment 30002 (index suggestion). Two assertions regressed from the baseline: (1) convention upgrade eligibility must be evaluated and documented in the classification output for suggestions, and (2) review comment 30002 must result in a sub-task through either direct classification or convention upgrade. The verify-pr skill must evaluate convention upgrade eligibility for all suggestions and document the analysis in the review classification output, including CONVENTIONS.md lookup and codebase pattern analysis.

## Files to Modify
- `plugins/sdlc-workflow/skills/verify-pr/style-conventions.md` -- ensure Check 1 (Convention Upgrade) logic properly evaluates and documents convention upgrade eligibility for all suggestions
- `plugins/sdlc-workflow/skills/verify-pr/SKILL.md` -- verify Step 4c classification and Step 6b convention upgrade flow produce documented eligibility analysis
- `evals/verify-pr/evals.json` -- update eval assertions to cover the convention upgrade eligibility behavior if assertion text needs alignment

## Implementation Notes
- The failing assertions indicate that the convention upgrade eligibility analysis is not being documented in the classification output (review-30002.md). The style-conventions sub-agent's Check 1 must produce explicit evidence of CONVENTIONS.md lookup and codebase pattern analysis for every suggestion.
- Review the Check 1 flow in style-conventions.md: steps 1a (Check CONVENTIONS.md), 1b (Check Codebase Patterns), 1c (Performance-Related Scrutiny), and 1d (Upgrade Decision) must all produce documented evidence in the output.
- The second assertion expects a sub-task for comment 30002 -- verify whether the eval fixture data supports a convention upgrade (check if CONVENTIONS.md or codebase patterns in the fixture would trigger an upgrade).
- Cross-reference the baseline grading at `evals/verify-pr/baselines/latest/eval-3/grading.json` to understand what the passing behavior looked like.

## Acceptance Criteria
- [ ] Convention upgrade eligibility is evaluated and documented for all review comments classified as suggestions
- [ ] The review classification output includes CONVENTIONS.md lookup results and codebase pattern analysis
- [ ] Eval-3 assertions pass: convention upgrade eligibility is documented for comment 30002
- [ ] Eval-3 assertions pass: comment 30002 results in a sub-task through the appropriate classification path

## Test Requirements
- [ ] Update eval assertions in `evals/verify-pr/evals.json` to cover the convention upgrade eligibility behavior changes introduced by this task, if assertion text needs alignment with the implementation
- [ ] Verify eval-3 pass rate returns to 100% (baseline level)

## Review Context
**Eval Review Source:** github-actions[bot] eval result review on PR #747
**Eval ID:** eval-3
**Failing Assertions (2 regressions):**

1. **Assertion:** "Convention upgrade eligibility is evaluated for review comment 30002 (index suggestion) -- the review classification output (review-30002.md) or the report's Style/Conventions analysis explains whether the suggestion matches a documented or demonstrated project convention"
   **Evidence:** "The output file review-30002.md classifies the comment as a suggestion but does not evaluate convention upgrade eligibility -- no CONVENTIONS.md lookup or codebase pattern analysis is documented in the classification reasoning"
   **Baseline Classification:** regression (passed at baseline with 15/15)

2. **Assertion:** "Review comment 30002 (index suggestion) results in a sub-task regardless of classification path -- whether classified directly as code change request based on reviewer language, or upgraded from suggestion via convention analysis"
   **Evidence:** "No sub-task was created for review comment 30002 -- it was classified as suggestion and no convention upgrade was attempted, so the suggestion was not elevated to a code change request"
   **Baseline Classification:** regression (new assertion not present at baseline; conservative default)

## Target PR
https://github.com/mrizzi/sdlc-plugins/pull/747
