## Repository
sdlc-plugins

## Target PR
https://github.com/RHEcosystemAppEng/sdlc-plugins/pull/747

## Description
Fix verify-pr eval-3 assertion failures related to convention upgrade eligibility evaluation and sub-task creation for suggestion-classified review comments. The eval results show that when a review comment is classified as a suggestion (e.g., comment 30002 about adding an index), the verify-pr skill does not evaluate convention upgrade eligibility — no CONVENTIONS.md lookup or codebase pattern analysis is performed in the classification reasoning.

## Files to Modify
- `plugins/sdlc-workflow/skills/verify-pr/style-conventions.md` — ensure the Convention Upgrade check (Check 1) evaluates every suggestion comment against CONVENTIONS.md and codebase patterns, documenting the analysis in the classification output
- `plugins/sdlc-workflow/skills/verify-pr/SKILL.md` — verify that the orchestrator's Step 4c classification pipeline feeds all suggestions to the Style/Conventions sub-agent for convention upgrade evaluation

## Implementation Notes
- The Convention Upgrade check (Check 1 in style-conventions.md) must evaluate every comment classified as "suggestion" for convention upgrade eligibility
- The evaluation must include: CONVENTIONS.md lookup (Check 1a), codebase pattern search (Check 1b), and performance-related scrutiny if applicable (Check 1c)
- The classification output (review-N.md) must document the convention upgrade analysis, even when the suggestion is NOT upgraded — explicitly state what was checked and why no match was found
- Follow the existing Check 1d decision logic for upgrade/no-upgrade determination

## Acceptance Criteria
- [ ] Every suggestion-classified comment has documented convention upgrade eligibility evaluation in its classification output
- [ ] CONVENTIONS.md is checked for matching conventions when available
- [ ] Codebase patterns are searched for established practices matching the suggestion
- [ ] The classification reasoning explicitly explains whether a convention match was found and the upgrade decision

## Review Context
**Source:** Eval result review from github-actions[bot] (review 40001)

**Failing assertions from eval-3:**

1. **Assertion:** "Convention upgrade eligibility is evaluated for review comment 30002 (index suggestion) — the review classification output (review-30002.md) or the report's Style/Conventions analysis explains whether the suggestion matches a documented or demonstrated project convention"
   **Evidence:** "The output file review-30002.md classifies the comment as a suggestion but does not evaluate convention upgrade eligibility — no CONVENTIONS.md lookup or codebase pattern analysis is documented in the classification reasoning"

2. **Assertion:** "Review comment 30002 (index suggestion) results in a sub-task regardless of classification path — whether classified directly as code change request based on reviewer language, or upgraded from suggestion via convention analysis"
   **Evidence:** "No sub-task was created for review comment 30002 — it was classified as suggestion and no convention upgrade was attempted, so the suggestion was not elevated to a code change request"
