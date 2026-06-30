## Repository
sdlc-plugins

## Target Branch
main

## Description
Fix eval-3 assertion failures related to convention upgrade eligibility evaluation and sub-task creation for review comment 30002. Two assertions fail because the verify-pr skill does not evaluate convention upgrade eligibility for suggestion-classified review comments and consequently does not create sub-tasks for comments that should be elevated to code change requests via convention analysis.

## Target PR
https://github.com/mrizzi/sdlc-plugins/pull/747

## Review Context

From the eval-3 CI review (posted by github-actions[bot]):

**Failing Assertion 1:**
- **Assertion:** "Convention upgrade eligibility is evaluated for review comment 30002 (index suggestion) — the review classification output (review-30002.md) or the report's Style/Conventions analysis explains whether the suggestion matches a documented or demonstrated project convention"
- **Evidence:** "The output file review-30002.md classifies the comment as a suggestion but does not evaluate convention upgrade eligibility — no CONVENTIONS.md lookup or codebase pattern analysis is documented in the classification reasoning"

**Failing Assertion 2:**
- **Assertion:** "Review comment 30002 (index suggestion) results in a sub-task regardless of classification path — whether classified directly as code change request based on reviewer language, or upgraded from suggestion via convention analysis"
- **Evidence:** "No sub-task was created for review comment 30002 — it was classified as suggestion and no convention upgrade was attempted, so the suggestion was not elevated to a code change request"

## Files to Modify
- `plugins/sdlc-workflow/skills/verify-pr/style-conventions.md` — ensure Check 1 (Convention Upgrade) documents the convention upgrade eligibility evaluation in classification output, including CONVENTIONS.md lookup and codebase pattern analysis reasoning
- `plugins/sdlc-workflow/skills/verify-pr/SKILL.md` — ensure Step 4c classification and Step 6b convention upgrade flow produces sub-tasks for suggestions that match documented or demonstrated conventions

## Implementation Notes
- The root issue is that suggestion-classified comments are not having their convention upgrade eligibility evaluated. The Style/Conventions sub-agent's Check 1 (Convention Upgrade) must explicitly document in its output whether each suggestion was checked against CONVENTIONS.md and codebase patterns.
- When a suggestion matches a convention (documented in CONVENTIONS.md or demonstrated by codebase usage), it must be upgraded to a code change request, which then triggers sub-task creation in Step 6d.
- The classification reasoning output (review-N.md) must include evidence of the convention upgrade eligibility check — either confirming a match was found (and upgrade applied) or confirming no match exists (and the suggestion remains as-is).

## Acceptance Criteria
- [ ] Convention upgrade eligibility is evaluated and documented for all suggestion-classified review comments
- [ ] CONVENTIONS.md lookup is performed and its result recorded in classification reasoning
- [ ] Codebase pattern analysis is performed and its result recorded in classification reasoning
- [ ] Suggestions matching documented or demonstrated conventions are upgraded to code change requests
- [ ] Upgraded suggestions result in sub-task creation

## Test Requirements
- [ ] Verify eval-3 assertions pass after the fix
- [ ] Verify convention upgrade eligibility reasoning appears in review classification output
- [ ] Verify sub-tasks are created for convention-backed suggestions
