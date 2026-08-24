## Repository
sdlc-plugins

## Target Branch
main

## Description
Fix eval-3 assertion failures in verify-pr related to convention upgrade eligibility evaluation and sub-task creation for review comments classified as suggestions. Two assertions fail at 85% pass rate:

1. Convention upgrade eligibility is not evaluated for suggestion-classified review comments -- the classification output does not document whether CONVENTIONS.md lookup or codebase pattern analysis was performed.
2. Suggestion-classified review comments that should result in sub-tasks (either via direct classification as code change request or via convention upgrade) do not produce sub-tasks when convention upgrade is not attempted.

The root cause is that the implementation skips convention upgrade evaluation for suggestions, leaving them as suggestions without checking whether project conventions support upgrading them to code change requests.

## Files to Modify
- `plugins/sdlc-workflow/skills/verify-pr/style-conventions.md` -- ensure Check 1 (Convention Upgrade) evaluation is documented in the classification output for every suggestion-classified comment, including the CONVENTIONS.md lookup and codebase pattern analysis results
- `evals/verify-pr/evals.json` -- update eval assertions if needed to align with the corrected behavior

## Implementation Notes
- The Style/Conventions sub-agent's Check 1 (Convention Upgrade) must evaluate every comment classified as "suggestion" in the Classified Review Comments
- For each suggestion, the output must document: (1) whether CONVENTIONS.md was checked, (2) whether codebase pattern analysis was performed, (3) the upgrade decision and evidence
- If a suggestion matches a documented or demonstrated convention, it must be upgraded to a code change request, which then triggers sub-task creation in Step 6d
- Follow the existing Check 1 structure in style-conventions.md (steps 1a through 1d) -- the logic is already defined but the implementation must ensure it runs for all suggestions and documents its findings

## Acceptance Criteria
- [ ] Convention upgrade eligibility is evaluated for every suggestion-classified review comment
- [ ] The classification output documents CONVENTIONS.md lookup results for each suggestion
- [ ] The classification output documents codebase pattern analysis results for each suggestion
- [ ] Suggestions matching documented or demonstrated conventions are upgraded to code change requests
- [ ] Upgraded suggestions result in sub-task creation
- [ ] eval-3 assertions pass after the fix

## Test Requirements
- [ ] Verify convention upgrade evaluation runs for suggestion-classified comments
- [ ] Verify the classification output includes convention lookup documentation
- [ ] Verify upgraded suggestions produce sub-tasks
- [ ] Run eval-3 and confirm all assertions pass

## Review Context
**Eval-3 failing assertion 1:**
- **Assertion:** "Convention upgrade eligibility is evaluated for review comment 30002 (index suggestion) -- the review classification output (review-30002.md) or the report's Style/Conventions analysis explains whether the suggestion matches a documented or demonstrated project convention"
- **Evidence:** "The output file review-30002.md classifies the comment as a suggestion but does not evaluate convention upgrade eligibility -- no CONVENTIONS.md lookup or codebase pattern analysis is documented in the classification reasoning"

**Eval-3 failing assertion 2:**
- **Assertion:** "Review comment 30002 (index suggestion) results in a sub-task regardless of classification path -- whether classified directly as code change request based on reviewer language, or upgraded from suggestion via convention analysis"
- **Evidence:** "No sub-task was created for review comment 30002 -- it was classified as suggestion and no convention upgrade was attempted, so the suggestion was not elevated to a code change request"

## Target PR
https://github.com/mrizzi/sdlc-plugins/pull/747
