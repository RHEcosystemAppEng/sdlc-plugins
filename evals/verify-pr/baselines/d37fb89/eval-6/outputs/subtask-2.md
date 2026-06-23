## Repository
sdlc-plugins

## Target Branch
main

## Description
Fix eval-3 assertion failures related to convention upgrade eligibility and sub-task creation for review comment 30002. The eval expects that (1) convention upgrade eligibility is evaluated for suggestion-type review comments, with documented reasoning about CONVENTIONS.md lookup or codebase pattern analysis, and (2) review comment 30002 results in a sub-task regardless of classification path -- either directly as a code change request or via convention upgrade from suggestion. The current implementation classifies the comment as a suggestion without attempting convention upgrade, and does not create a sub-task.

## Files to Modify
- `plugins/sdlc-workflow/skills/verify-pr/style-conventions.md` -- ensure Check 1 (Convention Upgrade) explicitly documents the convention eligibility evaluation reasoning in the output for each suggestion examined
- `plugins/sdlc-workflow/skills/verify-pr/SKILL.md` -- ensure the classification and convention upgrade pipeline produces sub-tasks for suggestions that match conventions, and that the reasoning is captured in output files

## Implementation Notes
- The eval-3 failures indicate that suggestion-classified review comments are not being evaluated for convention upgrade eligibility -- the classification reasoning output must document whether a CONVENTIONS.md lookup or codebase pattern analysis was performed
- When a suggestion is examined for convention upgrade, the review classification output (review-N.md) or the report's Style/Conventions analysis must explain whether the suggestion matches a documented or demonstrated project convention
- If convention upgrade elevates a suggestion to a code change request, a sub-task must be created for it
- Review the Convention Upgrade check (Check 1 in style-conventions.md) to ensure it produces explicit output about the eligibility evaluation for each suggestion

## Acceptance Criteria
- [ ] Convention upgrade eligibility is evaluated for suggestion-type review comments with documented reasoning
- [ ] The review classification output or Style/Conventions analysis explains whether each suggestion matches a documented or demonstrated project convention
- [ ] Suggestions that match conventions are upgraded to code change requests and result in sub-task creation
- [ ] eval-3 assertions pass after the fix

## Test Requirements
- [ ] Verify that convention upgrade eligibility reasoning appears in review classification output
- [ ] Verify that suggestions matching conventions are upgraded and produce sub-tasks

## Review Context
**Eval-3 failing assertions (2 failures at 85% pass rate):**

- **Assertion:** "Convention upgrade eligibility is evaluated for review comment 30002 (index suggestion) -- the review classification output (review-30002.md) or the report's Style/Conventions analysis explains whether the suggestion matches a documented or demonstrated project convention"
  **Evidence:** "The output file review-30002.md classifies the comment as a suggestion but does not evaluate convention upgrade eligibility -- no CONVENTIONS.md lookup or codebase pattern analysis is documented in the classification reasoning"

- **Assertion:** "Review comment 30002 (index suggestion) results in a sub-task regardless of classification path -- whether classified directly as code change request based on reviewer language, or upgraded from suggestion via convention analysis"
  **Evidence:** "No sub-task was created for review comment 30002 -- it was classified as suggestion and no convention upgrade was attempted, so the suggestion was not elevated to a code change request"

## Target PR
https://github.com/mrizzi/sdlc-plugins/pull/747
