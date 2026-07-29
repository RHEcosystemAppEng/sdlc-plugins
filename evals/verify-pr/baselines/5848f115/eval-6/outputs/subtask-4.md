## Repository
sdlc-plugins

## Target Branch
main

## Description
Root-cause: Improve convention upgrade eligibility evaluation in the verify-pr skill execution to ensure every suggestion receives explicit CONVENTIONS.md lookup and codebase pattern analysis. The eval-3 regression failures show that the verify-pr skill classified a suggestion (review comment 30002, an index suggestion) without evaluating convention upgrade eligibility -- no CONVENTIONS.md lookup or codebase pattern analysis was documented in the classification reasoning. This caused the suggestion to remain unupgraded when it should have been elevated to a code change request based on convention evidence.

The root cause is a skill gap in the implement-task phase: the verify-pr skill's convention upgrade logic (Check 1 in style-conventions.md) is defined correctly but was not consistently executed during PR verification. The classification reasoning output must include explicit evidence of the CONVENTIONS.md and codebase pattern checks performed for each suggestion, regardless of whether the check finds a match.

## Files to Modify
- `plugins/sdlc-workflow/skills/verify-pr/style-conventions.md` -- strengthen Check 1 (Convention Upgrade) instructions to require explicit documentation of the CONVENTIONS.md lookup and codebase pattern analysis in the output for EVERY suggestion, even when no match is found
- `plugins/sdlc-workflow/skills/verify-pr/SKILL.md` -- ensure Step 6b convention upgrade processing documentation aligns with the strengthened Check 1 requirements

## Implementation Notes
- Check 1 already defines the correct procedure (steps 1a through 1d), but the instructions do not explicitly require that the classification reasoning OUTPUT documents each step's result
- Add explicit output requirements to Check 1: for each suggestion, the finding must document (1) whether CONVENTIONS.md was checked and what was found (or "no match"), (2) whether codebase patterns were searched and what counts were found (or "no matching pattern"), (3) the upgrade decision and evidence
- This ensures eval assertions can verify that convention upgrade eligibility was actually evaluated by inspecting the output, not just that the instructions exist
- The existing Check 1 verdict logic (PASS = no upgrades, WARN = upgrades performed, N/A = no suggestions) remains unchanged
- Follow the pattern of Check 6 evidence documentation: "Evidence: list of undocumented symbols with file path and line number" -- similarly, Check 1 should list each suggestion examined with its CONVENTIONS.md and codebase pattern results

## Acceptance Criteria
- [ ] Check 1 instructions require explicit documentation of CONVENTIONS.md lookup results in the output for each suggestion
- [ ] Check 1 instructions require explicit documentation of codebase pattern analysis results in the output for each suggestion
- [ ] The convention upgrade evidence is recorded even when no match is found (negative evidence)
- [ ] eval-3 assertions about convention upgrade eligibility evaluation pass after the fix
