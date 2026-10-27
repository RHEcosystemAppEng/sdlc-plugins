## Repository
sdlc-plugins

## Target Branch
main

## Description
Fix eval-3 assertion failures in the verify-pr eval suite. Two assertions in eval-3 fail because the verify-pr skill does not evaluate convention upgrade eligibility for suggestion-classified review comments and does not create sub-tasks when convention analysis indicates the suggestion should be upgraded. The convention upgrade pathway (Style/Conventions sub-agent Check 1) must always document its evaluation reasoning in the classification output, and suggestions that match demonstrated project conventions must be elevated to code change requests with sub-task creation.

## Files to Modify
- `plugins/sdlc-workflow/skills/verify-pr/style-conventions.md` — update Check 1 (Convention Upgrade) to ensure convention upgrade eligibility is always evaluated and documented for every suggestion, even when no CONVENTIONS.md exists; ensure codebase pattern analysis is performed and recorded in classification output
- `plugins/sdlc-workflow/skills/verify-pr/SKILL.md` — update Step 4c or Step 6b to ensure upgraded suggestions always trigger sub-task creation

## Implementation Notes
- Check 1a–1d in style-conventions.md defines the convention upgrade pathway. The current implementation may skip evaluation when CONVENTIONS.md is absent. Ensure Check 1b (codebase pattern analysis) always runs and its results are documented in the review classification output (review-N.md)
- When codebase patterns demonstrate the suggested practice is widely used (e.g., multiple occurrences of the same pattern in similar files), the suggestion must be upgraded to a code change request per Check 1d
- The classification output file (review-30002.md in the eval fixture) must contain explicit convention upgrade eligibility analysis regardless of the final classification outcome

## Acceptance Criteria
- [ ] Convention upgrade eligibility is evaluated for every suggestion-classified review comment, with reasoning documented in the classification output
- [ ] When no CONVENTIONS.md exists, codebase pattern analysis (Check 1b) still runs and its results are recorded
- [ ] Suggestions matching demonstrated project conventions are upgraded to code change requests and trigger sub-task creation
- [ ] eval-3 assertion about convention upgrade eligibility evaluation passes
- [ ] eval-3 assertion about sub-task creation for review comment 30002 passes

## Test Requirements
- [ ] Verify convention upgrade evaluation reasoning appears in review classification output for all suggestion comments
- [ ] Verify sub-task creation occurs when convention analysis upgrades a suggestion

## Review Context
The following eval assertions failed in eval-3 (85% pass rate, 11/13 passed):

**Assertion 1:** "Convention upgrade eligibility is evaluated for review comment 30002 (index suggestion) — the review classification output (review-30002.md) or the report's Style/Conventions analysis explains whether the suggestion matches a documented or demonstrated project convention"
**Evidence:** "The output file review-30002.md classifies the comment as a suggestion but does not evaluate convention upgrade eligibility — no CONVENTIONS.md lookup or codebase pattern analysis is documented in the classification reasoning"

**Assertion 2:** "Review comment 30002 (index suggestion) results in a sub-task regardless of classification path — whether classified directly as code change request based on reviewer language, or upgraded from suggestion via convention analysis"
**Evidence:** "No sub-task was created for review comment 30002 — it was classified as suggestion and no convention upgrade was attempted, so the suggestion was not elevated to a code change request"

## Target PR
https://github.com/mrizzi/sdlc-plugins/pull/747
