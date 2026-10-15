## Repository
sdlc-plugins

## Target Branch
main

## Description
Fix eval-3 assertion failures in the verify-pr skill related to convention upgrade eligibility evaluation and sub-task creation for suggestion-classified review comments. The eval-3 run (85% pass rate, 2 of 13 assertions failing) revealed that the verify-pr implementation does not evaluate convention upgrade eligibility for suggestions, and consequently does not create sub-tasks for suggestions that should be upgraded to code change requests via convention analysis.

## Files to Modify
- `plugins/sdlc-workflow/skills/verify-pr/style-conventions.md` -- ensure the Convention Upgrade check (Check 2) evaluates all suggestion-classified comments for convention upgrade eligibility, including CONVENTIONS.md lookup and codebase pattern analysis
- `plugins/sdlc-workflow/skills/verify-pr/SKILL.md` -- ensure Step 6b convention upgrade processing correctly elevates suggestions to code change requests when convention evidence is found, and that Step 6d creates sub-tasks for upgraded suggestions

## Implementation Notes
- The Convention Upgrade check in style-conventions.md must produce explicit reasoning for each suggestion-classified comment, documenting whether a CONVENTIONS.md lookup or codebase pattern analysis was performed
- The classification output (review-N.md) must include convention upgrade eligibility analysis even when the comment is initially classified as a suggestion
- When convention evidence is found (documented convention or demonstrated codebase pattern), the suggestion must be upgraded to a code change request and proceed through the sub-task creation pipeline in Step 6d
- Follow the existing convention upgrade flow defined in style-conventions.md Check 2 and SKILL.md Step 6b

## Review Context
The following eval-3 assertions failed:

**Assertion 1:** "Convention upgrade eligibility is evaluated for review comment 30002 (index suggestion) -- the review classification output (review-30002.md) or the report's Style/Conventions analysis explains whether the suggestion matches a documented or demonstrated project convention"
**Evidence:** "The output file review-30002.md classifies the comment as a suggestion but does not evaluate convention upgrade eligibility -- no CONVENTIONS.md lookup or codebase pattern analysis is documented in the classification reasoning"

**Assertion 2:** "Review comment 30002 (index suggestion) results in a sub-task regardless of classification path -- whether classified directly as code change request based on reviewer language, or upgraded from suggestion via convention analysis"
**Evidence:** "No sub-task was created for review comment 30002 -- it was classified as suggestion and no convention upgrade was attempted, so the suggestion was not elevated to a code change request"

## Target PR
https://github.com/RHEcosystemAppEng/sdlc-plugins/pull/747

## Acceptance Criteria
- [ ] Convention upgrade eligibility is evaluated for every suggestion-classified review comment, with explicit reasoning documented in the classification output
- [ ] When a suggestion matches a documented convention in CONVENTIONS.md or a demonstrated codebase pattern, it is upgraded to a code change request
- [ ] Upgraded suggestions proceed through the sub-task creation pipeline and result in a Jira sub-task
- [ ] The review classification output includes convention upgrade analysis (CONVENTIONS.md lookup and/or codebase pattern analysis) even when no upgrade occurs

## Test Requirements
- [ ] Verify that a suggestion-classified comment with matching convention evidence is upgraded to a code change request and produces a sub-task
- [ ] Verify that the classification output documents convention upgrade eligibility reasoning for suggestion-classified comments
- [ ] Verify that suggestions without convention evidence remain as suggestions with documented reasoning for non-upgrade
