## Repository
sdlc-plugins

## Target Branch
main

## Description
Fix eval-3 regression failures related to convention upgrade eligibility evaluation and sub-task creation for review comments. Two assertions that previously passed at baseline (eval-3: 15/15, 100%) now fail (eval-3: 11/13, 85%), indicating a regression introduced by the PR changes.

The failures indicate that when a review comment is classified as a suggestion (e.g., comment 30002 with an index suggestion), the verify-pr skill must (1) evaluate convention upgrade eligibility by performing a CONVENTIONS.md lookup and codebase pattern analysis, and (2) create a sub-task if the suggestion is upgraded to a code change request or if the comment warrants a sub-task through direct classification.

## Files to Modify
- `plugins/sdlc-workflow/skills/verify-pr/style-conventions.md` -- ensure Check 1 (Convention Upgrade) properly evaluates eligibility for all suggestion-classified comments, including documenting the convention lookup and pattern analysis in the classification reasoning output
- `plugins/sdlc-workflow/skills/verify-pr/SKILL.md` -- verify that Step 6b (Apply Convention Upgrades) and Step 6d (Create Sub-Tasks) correctly process upgraded suggestions through the full pipeline

## Implementation Notes
- The eval-3 assertions test that convention upgrade eligibility is evaluated for review comments classified as suggestions, and that the evaluation reasoning is documented in the output
- The first failing assertion checks that `review-30002.md` or the report's Style/Conventions analysis explains whether the suggestion matches a documented or demonstrated project convention -- this requires the classification output to include CONVENTIONS.md lookup results and codebase pattern analysis
- The second failing assertion checks that review comment 30002 results in a sub-task regardless of classification path -- either through direct classification as code change request, or through convention upgrade from suggestion
- Review the Convention Upgrade check (Check 1) in style-conventions.md to ensure steps 1a-1d are thorough: CONVENTIONS.md lookup, codebase pattern search, and upgrade decision must all produce documented evidence in the output
- Ensure that when a suggestion is evaluated for convention upgrade, the reasoning is recorded even when no upgrade occurs (to satisfy the first assertion about documenting the evaluation)

## Acceptance Criteria
- [ ] Convention upgrade eligibility is evaluated for all suggestion-classified review comments with documented reasoning in the output
- [ ] The convention upgrade evaluation includes CONVENTIONS.md lookup results and codebase pattern analysis
- [ ] Review comments that match a convention are properly upgraded to code change requests and result in sub-task creation
- [ ] eval-3 passes with 13/13 assertions (restoring baseline 100% pass rate)

## Review Context
The following eval-3 assertions regressed from baseline (baseline: 15/15 100%, PR: 11/13 85%):

**Assertion 1:**
> "Convention upgrade eligibility is evaluated for review comment 30002 (index suggestion) -- the review classification output (review-30002.md) or the report's Style/Conventions analysis explains whether the suggestion matches a documented or demonstrated project convention"

**Evidence:**
> "The output file review-30002.md classifies the comment as a suggestion but does not evaluate convention upgrade eligibility -- no CONVENTIONS.md lookup or codebase pattern analysis is documented in the classification reasoning"

**Assertion 2:**
> "Review comment 30002 (index suggestion) results in a sub-task regardless of classification path -- whether classified directly as code change request based on reviewer language, or upgraded from suggestion via convention analysis"

**Evidence:**
> "No sub-task was created for review comment 30002 -- it was classified as suggestion and no convention upgrade was attempted, so the suggestion was not elevated to a code change request"

## Target PR
https://github.com/RHEcosystemAppEng/sdlc-plugins/pull/747
