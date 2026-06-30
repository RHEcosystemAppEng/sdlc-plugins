# Sub-Task: Root-cause: strengthen convention upgrade eligibility documentation in verify-pr

## Type: root-cause

## Repository
sdlc-plugins

## Target Branch
main

## Description
The eval-3 failures reveal that the verify-pr skill's convention upgrade pipeline does not consistently document its analysis for suggestion-classified review comments. When a review comment is classified as a suggestion, the Style/Conventions sub-agent's Check 1 (Convention Upgrade) should evaluate whether the suggestion matches a documented or demonstrated project convention, and the evaluation reasoning must be recorded in the output regardless of whether the suggestion is upgraded.

This is an implement-task skill gap. The knowledge required to prevent this defect is universal (method-based): "every classification decision must document its reasoning" is a general analysis technique that applies to any repository. The implement-task skill should ensure that convention upgrade eligibility analysis is always performed and documented for suggestion-classified comments, including cases where no convention match is found.

## Files to Modify
- `plugins/sdlc-workflow/skills/verify-pr/style-conventions.md` -- strengthen Check 1 (Convention Upgrade) to explicitly require that the convention analysis (CONVENTIONS.md lookup and codebase pattern search) is documented in the output for every suggestion, not just for upgraded ones

## Implementation Notes
- Check 1 currently documents convention upgrade analysis only when a match is found and a suggestion is upgraded. When no match is found, the suggestion is left as-is without recording what was checked.
- Add explicit language to Check 1 requiring that for every suggestion-classified comment, the output includes: (1) whether CONVENTIONS.md was checked and what was found (or that it was absent), (2) whether codebase patterns were searched and what was found, (3) the conclusion (upgraded or not upgraded, with evidence)
- This aligns with the existing "Evidence:" requirement in Check 1's verdict section but makes it explicit that evidence must be recorded per-comment, not just in the aggregate verdict

## Acceptance Criteria
- [ ] Check 1 in style-conventions.md explicitly requires documenting convention upgrade eligibility analysis for every suggestion-classified comment
- [ ] The documentation requirement covers both positive (convention found, upgrade) and negative (no convention, no upgrade) cases
- [ ] The output evidence for each suggestion includes what was checked (CONVENTIONS.md, codebase patterns) and what was concluded
