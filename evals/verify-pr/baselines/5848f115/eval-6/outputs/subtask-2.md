## Repository
sdlc-plugins

## Target Branch
main

## Description
Fix eval-3 assertion failures related to convention upgrade eligibility evaluation. The eval results show 2 failing assertions in eval-3 (85% pass rate, 11/13 passed). Both failures indicate that the verify-pr skill does not evaluate convention upgrade eligibility for review comments classified as suggestions, and does not create sub-tasks when convention upgrade should have elevated a suggestion to a code change request.

## Files to Modify
- `plugins/sdlc-workflow/skills/verify-pr/style-conventions.md` -- ensure Check 1 (Convention Upgrade) evaluation logic properly handles all classified suggestions, including those that should be upgraded based on CONVENTIONS.md or codebase pattern analysis
- `plugins/sdlc-workflow/skills/verify-pr/SKILL.md` -- verify Step 6b convention upgrade processing correctly applies upgrade decisions and feeds upgraded suggestions into the sub-task creation pipeline

## Implementation Notes
- The failing assertions indicate that for review comment 30002 (an index suggestion), the convention upgrade eligibility analysis was not performed: "no CONVENTIONS.md lookup or codebase pattern analysis is documented in the classification reasoning"
- The second failing assertion confirms the downstream consequence: no sub-task was created for the suggestion because it was never upgraded to a code change request
- Check 1 in style-conventions.md should be reviewed to ensure that EVERY suggestion in the Classified Review Comments is examined for convention upgrade, including:
  1. CONVENTIONS.md lookup (step 1a)
  2. Codebase pattern search (step 1b)
  3. Performance-related scrutiny when applicable (step 1c)
  4. Explicit upgrade decision with evidence (step 1d)
- The convention upgrade evidence must be recorded in the classification reasoning output (review-N.md files) so that eval assertions can verify the analysis was performed

## Acceptance Criteria
- [ ] Convention upgrade eligibility is evaluated for every suggestion in the Classified Review Comments
- [ ] CONVENTIONS.md lookup is documented in the classification reasoning for each suggestion
- [ ] Codebase pattern analysis is documented in the classification reasoning for each suggestion
- [ ] Suggestions matching documented or demonstrated conventions are upgraded to code change requests
- [ ] Upgraded suggestions result in sub-task creation via the standard pipeline
- [ ] eval-3 assertions pass after the fix

## Review Context
**Eval review source:** github-actions[bot] eval result review (review ID 40001)

**Failing assertions:**
1. "Convention upgrade eligibility is evaluated for review comment 30002 (index suggestion) -- the review classification output (review-30002.md) or the report's Style/Conventions analysis explains whether the suggestion matches a documented or demonstrated project convention"
   Evidence: "The output file review-30002.md classifies the comment as a suggestion but does not evaluate convention upgrade eligibility -- no CONVENTIONS.md lookup or codebase pattern analysis is documented in the classification reasoning"

2. "Review comment 30002 (index suggestion) results in a sub-task regardless of classification path -- whether classified directly as code change request based on reviewer language, or upgraded from suggestion via convention analysis"
   Evidence: "No sub-task was created for review comment 30002 -- it was classified as suggestion and no convention upgrade was attempted, so the suggestion was not elevated to a code change request"

## Target PR
https://github.com/mrizzi/sdlc-plugins/pull/747
