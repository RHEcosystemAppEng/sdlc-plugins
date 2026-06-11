## Repository
sdlc-plugins

## Target Branch
main

## Description
Fix eval-3 assertion failures related to convention upgrade eligibility and sub-task creation for review comment 30002 (index suggestion). Two assertions fail: (1) convention upgrade eligibility is not evaluated for comment 30002, and (2) no sub-task is created for comment 30002. The root cause is that the verify-pr skill classifies comment 30002 as a suggestion but does not attempt convention upgrade analysis (no CONVENTIONS.md lookup or codebase pattern analysis), so the suggestion is never elevated to a code change request and no sub-task is created.

## Files to Modify
- `plugins/sdlc-workflow/skills/verify-pr/style-conventions.md` -- ensure Check 1 (Convention Upgrade) properly evaluates all suggestions for convention upgrade eligibility, including documenting the analysis in the classification reasoning output
- `plugins/sdlc-workflow/skills/verify-pr/SKILL.md` -- if needed, clarify that convention upgrade eligibility must be evaluated and documented for every suggestion, not just those that match

## Implementation Notes
- The eval-3 assertions expect that convention upgrade eligibility is evaluated for comment 30002 and that the classification output (review-30002.md) documents whether the suggestion matches a documented or demonstrated project convention
- The Style/Conventions sub-agent's Check 1 (Convention Upgrade) should already handle this, but the eval evidence shows that no CONVENTIONS.md lookup or codebase pattern analysis was performed
- Ensure that Check 1 explicitly requires documenting the convention analysis for every suggestion, even when no match is found, so the reasoning is transparent and auditable
- The second assertion expects a sub-task to be created regardless of classification path -- either directly as a code change request or via convention upgrade. This implies the convention analysis should result in an upgrade for comment 30002 in the eval scenario

## Review Context
Eval-3 failing assertions from CI eval review:
- **Assertion:** "Convention upgrade eligibility is evaluated for review comment 30002 (index suggestion) -- the review classification output (review-30002.md) or the report's Style/Conventions analysis explains whether the suggestion matches a documented or demonstrated project convention"
  **Evidence:** "The output file review-30002.md classifies the comment as a suggestion but does not evaluate convention upgrade eligibility -- no CONVENTIONS.md lookup or codebase pattern analysis is documented in the classification reasoning"
- **Assertion:** "Review comment 30002 (index suggestion) results in a sub-task regardless of classification path -- whether classified directly as code change request based on reviewer language, or upgraded from suggestion via convention analysis"
  **Evidence:** "No sub-task was created for review comment 30002 -- it was classified as suggestion and no convention upgrade was attempted, so the suggestion was not elevated to a code change request"

## Target PR
https://github.com/mrizzi/sdlc-plugins/pull/747

## Acceptance Criteria
- [ ] Convention upgrade eligibility is evaluated and documented for all suggestions in the Style/Conventions sub-agent output
- [ ] The convention analysis reasoning is transparent in classification output files (e.g., review-30002.md)
- [ ] When a suggestion matches a documented or demonstrated convention, it is upgraded to a code change request and a sub-task is created
- [ ] Eval-3 assertions pass after the fix
