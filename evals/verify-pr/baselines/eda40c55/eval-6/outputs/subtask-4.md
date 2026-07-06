## Repository
sdlc-plugins

## Target Branch
main

## Description
Root-cause: Improve the implement-task skill's convention upgrade pipeline execution to ensure that convention upgrade eligibility is evaluated and documented for every review comment classified as a suggestion. The eval-3 assertion failures in TC-9106 verification reveal that the implementation skipped convention upgrade evaluation entirely for a suggestion-classified comment -- no CONVENTIONS.md lookup or codebase pattern analysis was performed, and consequently no sub-task was created when the convention match should have triggered an upgrade.

The gap is in the implement-task skill's execution of the Style/Conventions sub-agent's Check 1 (Convention Upgrade). The method -- "for every suggestion, evaluate convention upgrade eligibility by performing CONVENTIONS.md lookup and codebase pattern analysis, and document the result" -- is universal and language-agnostic, making this a skill gap rather than a convention gap.

## Files to Modify
- `plugins/sdlc-workflow/skills/verify-pr/style-conventions.md` -- strengthen the Convention Upgrade check instructions to explicitly require that every suggestion-classified comment undergoes documented convention evaluation, even when no match is found (the negative result should be recorded as evidence)
- `plugins/sdlc-workflow/skills/verify-pr/SKILL.md` -- reinforce in Step 6b that convention upgrade evaluation is mandatory for all suggestions and that the evaluation reasoning must be traceable in the classification output

## Implementation Notes
- The current Convention Upgrade check (Check 1 in style-conventions.md) describes the upgrade process but does not explicitly mandate that every suggestion must undergo evaluation. The implementation may have interpreted the check as optional when no obvious convention match was apparent.
- Add explicit language requiring that for each suggestion: (1) CONVENTIONS.md is checked for matching patterns, (2) codebase patterns are searched, (3) the result (match or no-match) is documented in the classification reasoning.
- The "no match found" case should still produce evidence: "Checked CONVENTIONS.md (no matching section found) and codebase patterns (0 occurrences of similar pattern). Suggestion remains as-is."
- This ensures the convention upgrade evaluation is auditable and prevents silent skipping.

## Acceptance Criteria
- [ ] The Convention Upgrade check explicitly requires evaluation of every suggestion-classified comment
- [ ] The check requires documenting the evaluation result (match or no-match) in the classification output
- [ ] CONVENTIONS.md lookup is mandatory for every suggestion, not just those with obvious convention matches
- [ ] Codebase pattern analysis is mandatory for every suggestion
- [ ] The no-match case produces documented evidence that evaluation was performed

## Test Requirements
- [ ] Verify that convention upgrade evaluation is performed for all suggestion-classified comments
- [ ] Verify that the evaluation result is documented in the review classification output
- [ ] Verify that no-match cases produce evidence of evaluation
