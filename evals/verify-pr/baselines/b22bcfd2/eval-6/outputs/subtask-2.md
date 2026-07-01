## Repository
sdlc-plugins

## Target Branch
main

## Description
Fix eval-3 assertion failures related to convention upgrade eligibility evaluation and sub-task creation for review comment 30002. The eval expects that when a review comment is classified as a suggestion (e.g., an index suggestion), the verify-pr skill evaluates whether the suggestion matches a documented or demonstrated project convention and, if so, upgrades it to a code change request and creates a sub-task. Currently, the suggestion is classified but no convention upgrade eligibility is evaluated -- no CONVENTIONS.md lookup or codebase pattern analysis is documented in the classification reasoning, and no sub-task is created.

## Files to Modify
- `plugins/sdlc-workflow/skills/verify-pr/style-conventions.md` -- ensure Check 1 (Convention Upgrade) documentation and logic clearly require evaluating every suggestion for convention upgrade eligibility with documented reasoning
- `plugins/sdlc-workflow/skills/verify-pr/SKILL.md` -- ensure Step 6b (Apply Convention Upgrades) processes all upgrade-comment actions and that the classification reply in Step 6e includes convention upgrade eligibility reasoning for suggestions

## Implementation Notes
- The two failing assertions both relate to review comment 30002 being classified as a suggestion without attempting convention upgrade analysis
- The first assertion requires that convention upgrade eligibility is evaluated and the reasoning is documented in the classification output (review-30002.md) or the report's Style/Conventions analysis
- The second assertion requires that the comment results in a sub-task regardless of classification path -- either classified directly as a code change request, or upgraded from suggestion via convention analysis
- The fix should ensure the Style/Conventions sub-agent's Check 1 (Convention Upgrade) explicitly evaluates every suggestion for CONVENTIONS.md matches and codebase pattern matches, and documents the evaluation reasoning even when no match is found
- The classification reply (Step 6e) should include convention upgrade eligibility reasoning for suggestions that were evaluated but not upgraded

## Acceptance Criteria
- [ ] Convention upgrade eligibility is evaluated for all suggestions, with documented reasoning in the classification output
- [ ] When a suggestion matches a documented or demonstrated convention, it is upgraded to a code change request and a sub-task is created
- [ ] The classification reasoning explicitly states whether CONVENTIONS.md was checked and whether codebase patterns were analyzed
- [ ] eval-3 assertions pass after the fix

## Review Context
**Source:** Eval result review from CI (github-actions[bot], review ID 40001)
**Eval ID:** eval-3
**Pass Rate:** 85% (11/13 passed, 2 failed)

**Failing Assertion 1:**
- **Assertion:** "Convention upgrade eligibility is evaluated for review comment 30002 (index suggestion) -- the review classification output (review-30002.md) or the report's Style/Conventions analysis explains whether the suggestion matches a documented or demonstrated project convention"
- **Evidence:** "The output file review-30002.md classifies the comment as a suggestion but does not evaluate convention upgrade eligibility -- no CONVENTIONS.md lookup or codebase pattern analysis is documented in the classification reasoning"

**Failing Assertion 2:**
- **Assertion:** "Review comment 30002 (index suggestion) results in a sub-task regardless of classification path -- whether classified directly as code change request based on reviewer language, or upgraded from suggestion via convention analysis"
- **Evidence:** "No sub-task was created for review comment 30002 -- it was classified as suggestion and no convention upgrade was attempted, so the suggestion was not elevated to a code change request"

## Target PR
https://github.com/mrizzi/sdlc-plugins/pull/747
