## Repository
sdlc-plugins

## Target Branch
main

## Description
Fix eval-3 assertion failures related to convention upgrade eligibility evaluation and sub-task creation for review comment 30002 (index suggestion). The verify-pr skill must evaluate convention upgrade eligibility for suggestions and create sub-tasks for convention-backed suggestions that are upgraded to code change requests.

Two eval-3 assertions are failing:
1. Convention upgrade eligibility is not being evaluated for suggestion-classified comments -- the classification output does not document CONVENTIONS.md lookup or codebase pattern analysis
2. Suggestion comments that should be upgraded via convention analysis are not resulting in sub-tasks because no convention upgrade is attempted

## Files to Modify
- `plugins/sdlc-workflow/skills/verify-pr/style-conventions.md` -- ensure Check 1 (Convention Upgrade) instructions clearly require convention eligibility evaluation for all suggestion-classified comments, with documented reasoning in the output
- `plugins/sdlc-workflow/skills/verify-pr/SKILL.md` -- verify Step 6b (Apply Convention Upgrades) correctly processes upgrade-comment actions and that Step 6d creates sub-tasks for upgraded suggestions

## Implementation Notes
- The Convention Upgrade check (Check 1 in style-conventions.md) must evaluate every suggestion-classified comment against CONVENTIONS.md and codebase patterns
- The classification output (review-NNNNN.md) must include a Convention Upgrade Evaluation section documenting the CONVENTIONS.md lookup, file-type applicability check, codebase pattern analysis, and upgrade decision
- When a suggestion matches a documented or demonstrated convention, it must be upgraded to a code change request and result in sub-task creation
- Follow the existing convention upgrade flow: Check 1a (CONVENTIONS.md check), 1b (Codebase Patterns), 1c (Performance-Related Scrutiny), 1d (Upgrade Decision)

## Acceptance Criteria
- [ ] Convention upgrade eligibility is evaluated for all suggestion-classified review comments
- [ ] The classification output includes a Convention Upgrade Evaluation section with CONVENTIONS.md lookup, file-type applicability, codebase pattern analysis, and upgrade decision
- [ ] Suggestions that match documented or demonstrated conventions are upgraded to code change requests
- [ ] Upgraded suggestions result in sub-task creation with Review Context and Target PR sections
- [ ] eval-3 assertions for convention upgrade eligibility and sub-task creation pass

## Review Context
> **Assertion:** "Convention upgrade eligibility is evaluated for review comment 30002 (index suggestion) -- the review classification output (review-30002.md) or the report's Style/Conventions analysis explains whether the suggestion matches a documented or demonstrated project convention"
> **Evidence:** "The output file review-30002.md classifies the comment as a suggestion but does not evaluate convention upgrade eligibility -- no CONVENTIONS.md lookup or codebase pattern analysis is documented in the classification reasoning"

> **Assertion:** "Review comment 30002 (index suggestion) results in a sub-task regardless of classification path -- whether classified directly as code change request based on reviewer language, or upgraded from suggestion via convention analysis"
> **Evidence:** "No sub-task was created for review comment 30002 -- it was classified as suggestion and no convention upgrade was attempted, so the suggestion was not elevated to a code change request"

## Target PR
https://github.com/mrizzi/sdlc-plugins/pull/747
