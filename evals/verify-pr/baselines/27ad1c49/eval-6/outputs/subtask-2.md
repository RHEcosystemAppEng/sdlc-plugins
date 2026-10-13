## Repository
sdlc-plugins

## Target Branch
main

## Target PR
https://github.com/mrizzi/sdlc-plugins/pull/747

## Description
Fix two regression assertion failures in eval-3 of the verify-pr eval suite. The failures relate to convention upgrade eligibility evaluation for review comment 30002 (an index suggestion). The verify-pr skill is not documenting its convention upgrade analysis in the classification reasoning, and a sub-task is not being created when the convention analysis would support an upgrade. Both assertions pass at baseline (9401c868, 100% pass rate for eval-3) but fail on this PR branch, indicating a regression.

## Files to Modify
- `plugins/sdlc-workflow/skills/verify-pr/style-conventions.md` -- ensure Check 1 (Convention Upgrade) behavior is not disrupted by the addition of Check 6 (Documentation Coverage); verify the output format change from 5 to 6 rows does not affect convention upgrade evaluation
- `plugins/sdlc-workflow/skills/verify-pr/SKILL.md` -- ensure the new Documentation Coverage verdict mapping does not interfere with convention upgrade processing in Step 6b

## Implementation Notes
- The two failing assertions are:
  1. "Convention upgrade eligibility is evaluated for review comment 30002 (index suggestion)" -- the classification output must document whether the suggestion matches a documented or demonstrated project convention (CONVENTIONS.md lookup or codebase pattern analysis)
  2. "Review comment 30002 (index suggestion) results in a sub-task regardless of classification path" -- the suggestion should either be classified directly as a code change request or upgraded via convention analysis, and in either case result in a sub-task
- The baseline (9401c868) shows eval-3 at 15/15 (100%). The convention upgrade eligibility assertion (equivalent to baseline assertion 12) passes at baseline, confirming this is a regression
- Investigate whether the output format change (5 rows to 6 rows in style-conventions.md) causes the sub-agent to truncate or skip convention upgrade analysis
- Investigate whether the new verdict mapping row in SKILL.md affects how the orchestrator processes convention upgrade actions in Step 6b
- The existing convention upgrade logic (Check 1 in style-conventions.md) was not directly modified by this PR, so the regression may be an indirect side effect of the output format change

## Review Context
CI eval run posted by github-actions[bot] reported eval-3 at 85% (11/13):

> **Assertion:** "Convention upgrade eligibility is evaluated for review comment 30002 (index suggestion) -- the review classification output (review-30002.md) or the report's Style/Conventions analysis explains whether the suggestion matches a documented or demonstrated project convention"
> **Evidence:** "The output file review-30002.md classifies the comment as a suggestion but does not evaluate convention upgrade eligibility -- no CONVENTIONS.md lookup or codebase pattern analysis is documented in the classification reasoning"

> **Assertion:** "Review comment 30002 (index suggestion) results in a sub-task regardless of classification path -- whether classified directly as code change request based on reviewer language, or upgraded from suggestion via convention analysis"
> **Evidence:** "No sub-task was created for review comment 30002 -- it was classified as suggestion and no convention upgrade was attempted, so the suggestion was not elevated to a code change request"

## Acceptance Criteria
- [ ] eval-3 passes at 100% (or matches baseline pass rate) after the fix
- [ ] Convention upgrade eligibility is documented in the classification output when a suggestion is evaluated
- [ ] The output format change (5 to 6 rows) does not affect convention upgrade evaluation behavior
- [ ] The verify-pr skill properly evaluates CONVENTIONS.md lookup and codebase pattern analysis for suggestions

## Test Requirements
- [ ] Run the verify-pr eval suite and confirm eval-3 achieves at least the baseline pass rate (15/15 or 100%)
- [ ] Verify that convention upgrade analysis is present in classification output for suggestion-classified comments

## Verification Commands
- `python3 -m pytest plugins/sdlc-workflow/scripts/ -q` -- all existing unit tests pass
