## Repository
sdlc-plugins

## Target Branch
main

## Description
Fix eval-3 assertion failures related to convention upgrade eligibility evaluation and sub-task creation for review comments classified as suggestions. The eval-3 scenario (within the verify-pr eval suite) has 2 failing assertions at an 85% pass rate, indicating that the verify-pr skill does not properly evaluate convention upgrade eligibility for suggestion-classified comments and does not create sub-tasks when a suggestion should be elevated to a code change request via convention analysis.

## Files to Modify
- `plugins/sdlc-workflow/skills/verify-pr/style-conventions.md` -- update Check 1 (Convention Upgrade) to ensure convention upgrade eligibility is always evaluated and documented for suggestion-classified comments, even when no upgrade occurs
- `plugins/sdlc-workflow/skills/verify-pr/SKILL.md` -- update Step 6b (Apply Convention Upgrades) or Step 6d (Create Sub-Tasks) if the sub-task creation pipeline needs adjustment for upgraded suggestions

## Implementation Notes
- The two failing assertions indicate a gap in how convention upgrade eligibility is handled:
  1. The classification output (review-N.md) must document whether convention upgrade eligibility was evaluated, including CONVENTIONS.md lookup results and codebase pattern analysis, even when the result is "no matching convention found"
  2. When a suggestion matches a convention (or should be upgraded based on established codebase patterns), a sub-task must be created -- the current implementation appears to stop at classification without attempting the upgrade path
- Follow the existing Convention Upgrade check structure (Check 1 in style-conventions.md), specifically steps 1a-1d
- Ensure the upgrade-comment action is produced when a convention match is found, so the orchestrator can create the sub-task in Step 6d

## Acceptance Criteria
- [ ] Convention upgrade eligibility is evaluated for every suggestion-classified review comment, with reasoning documented in the classification output
- [ ] When a suggestion matches a documented convention (CONVENTIONS.md) or demonstrated codebase pattern, it is upgraded to a code change request
- [ ] Upgraded suggestions result in sub-task creation through the standard pipeline (Step 6b upgrade, Step 6d sub-task creation)
- [ ] The review classification output explains the convention lookup result (match or no match) with specific evidence

## Test Requirements
- [ ] Verify that a suggestion-classified comment triggers convention upgrade eligibility evaluation
- [ ] Verify that a suggestion matching a documented convention is upgraded and results in a sub-task
- [ ] Verify that a suggestion with no matching convention remains classified as suggestion with documented reasoning

## Review Context
The following eval assertions failed in eval-3 (from CI eval review on PR #747):

**Assertion 1:** "Convention upgrade eligibility is evaluated for review comment 30002 (index suggestion) -- the review classification output (review-30002.md) or the report's Style/Conventions analysis explains whether the suggestion matches a documented or demonstrated project convention"
**Evidence:** "The output file review-30002.md classifies the comment as a suggestion but does not evaluate convention upgrade eligibility -- no CONVENTIONS.md lookup or codebase pattern analysis is documented in the classification reasoning"

**Assertion 2:** "Review comment 30002 (index suggestion) results in a sub-task regardless of classification path -- whether classified directly as code change request based on reviewer language, or upgraded from suggestion via convention analysis"
**Evidence:** "No sub-task was created for review comment 30002 -- it was classified as suggestion and no convention upgrade was attempted, so the suggestion was not elevated to a code change request"

## Target PR
https://github.com/RHEcosystemAppEng/sdlc-plugins/pull/747
