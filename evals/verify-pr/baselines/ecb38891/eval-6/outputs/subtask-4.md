## Repository
sdlc-plugins

## Target Branch
main

## Description
Root-cause: Strengthen the implement-task skill's convention upgrade evaluation to ensure every suggestion is evaluated for convention upgrade eligibility and the evaluation reasoning is documented. The eval-3 failures in TC-9106 verification revealed that when the verify-pr skill classifies a review comment as a suggestion, the convention upgrade pipeline (Style/Conventions sub-agent Check 1) does not consistently evaluate whether the suggestion matches a documented or demonstrated project convention. This results in suggestions that should be upgraded to code change requests (and trigger sub-task creation) being left as suggestions with no action taken.

This is a method-based skill gap in the implement-task phase: the implement-task skill should ensure that the convention upgrade check always runs on every suggestion and documents its reasoning, regardless of the suggestion's content. The method is: "For every suggestion, perform CONVENTIONS.md lookup and codebase pattern analysis, and document the evaluation result in the classification output."

## Files to Modify
- `plugins/sdlc-workflow/skills/verify-pr/style-conventions.md` -- strengthen Check 1 (Convention Upgrade) instructions to require explicit evaluation and documentation for every suggestion, even when no convention match is found
- `plugins/sdlc-workflow/skills/verify-pr/SKILL.md` -- add a constraint or rule ensuring convention upgrade evaluation is always performed and documented for classified suggestions

## Implementation Notes
- The current Check 1 instructions describe the convention upgrade flow but do not mandate that the evaluation reasoning be documented in the output when no match is found
- The fix should require that for every suggestion, the classification output includes: (1) whether CONVENTIONS.md was checked, (2) whether codebase patterns were searched, (3) the result of each check (match found or no match)
- This ensures that eval assertions can verify the evaluation was performed, not just the final classification
- Follow the existing convention upgrade structure: 1a (CONVENTIONS.md), 1b (codebase patterns), 1c (performance scrutiny), 1d (upgrade decision)

## Acceptance Criteria
- [ ] Every classified suggestion has documented convention upgrade evaluation reasoning in the output
- [ ] CONVENTIONS.md lookup result is explicitly stated (match found with section reference, or no match)
- [ ] Codebase pattern analysis result is explicitly stated (N occurrences found, or no pattern match)
- [ ] Suggestions matching conventions are upgraded to code change requests with documented evidence
- [ ] Suggestions not matching conventions remain as suggestions with documented "no match" reasoning

## Test Requirements
- [ ] Verify that classification output for a suggestion includes CONVENTIONS.md lookup reasoning
- [ ] Verify that classification output for a suggestion includes codebase pattern analysis reasoning
- [ ] Verify that a suggestion matching a convention is upgraded and documents the match evidence
- [ ] Verify that a suggestion not matching any convention documents the "no match" result
