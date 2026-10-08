## Repository
sdlc-plugins

## Target Branch
main

## Description
Add Markdown-specific documentation coverage rule to Check 6 in the verify-pr style-conventions sub-agent. The current implementation skips Markdown files entirely ("Markdown: not applicable -- skip Markdown files"), but this repository heavily uses Markdown for skill definitions. The check should verify that new Markdown sections (headings) have introductory explanatory text.

## Files to Modify
- `plugins/sdlc-workflow/skills/verify-pr/style-conventions.md` -- update Check 6 step 6b to replace the Markdown skip rule with a Markdown-specific documentation check for new headings

## Implementation Notes
- Replace the current Markdown entry ("Markdown: not applicable -- skip Markdown files") in step 6b with a Markdown-specific rule
- The Markdown rule should check whether new `###` (or lower-level) headings have at least one paragraph of explanatory text before any sub-sections or code blocks
- Follow the same pattern as other language-specific checks in step 6b
- A new heading without any introductory text before sub-sections or code blocks should be flagged as undocumented

## Review Context
**Reviewer:** reviewer-b
**Comment ID:** 50001
**File:** plugins/sdlc-workflow/skills/verify-pr/style-conventions.md, line 310
**Comment:** "The Check 6 description says 'Markdown: not applicable -- skip Markdown files' but this is a documentation-heavy repository where skills are defined in Markdown. The check should still verify that new Markdown sections have introductory text explaining their purpose, even if traditional doc comments don't apply. Consider adding a Markdown-specific rule that checks whether new `###` headings have at least one paragraph of explanatory text before any sub-sections or code blocks."

## Target PR
https://github.com/RHEcosystemAppEng/sdlc-plugins/pull/747

## Acceptance Criteria
- [ ] Check 6 step 6b includes a Markdown-specific documentation rule instead of skipping Markdown files
- [ ] The Markdown rule checks that new headings have at least one paragraph of explanatory text before sub-sections or code blocks
- [ ] New Markdown headings without introductory text are flagged as undocumented symbols
