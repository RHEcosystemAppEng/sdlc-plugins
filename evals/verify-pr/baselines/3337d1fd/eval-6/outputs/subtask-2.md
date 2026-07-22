## Repository
sdlc-plugins

## Target Branch
main

## Description
Add a Markdown-specific documentation rule to Check 6 (Documentation Coverage) in the style-conventions sub-agent. The current implementation blanket-skips all Markdown files ("Markdown: not applicable -- skip Markdown files"), but in documentation-heavy repositories where skills and workflows are defined in Markdown, new sections should still be verified for adequate explanatory content.

## Files to Modify
- `plugins/sdlc-workflow/skills/verify-pr/style-conventions.md` -- modify Check 6 step 6b to replace the blanket Markdown exclusion with a Markdown-specific rule that checks whether new `###` headings have at least one paragraph of explanatory text before any sub-sections or code blocks

## Review Context
Reviewer reviewer-b commented on `plugins/sdlc-workflow/skills/verify-pr/style-conventions.md` line 310:

> The Check 6 description says 'Markdown: not applicable -- skip Markdown files' but this is a documentation-heavy repository where skills are defined in Markdown. The check should still verify that new Markdown sections have introductory text explaining their purpose, even if traditional doc comments don't apply. Consider adding a Markdown-specific rule that checks whether new `###` headings have at least one paragraph of explanatory text before any sub-sections or code blocks.

## Target PR
https://github.com/RHEcosystemAppEng/sdlc-plugins/pull/747

## Implementation Notes
- Replace the "Markdown: not applicable -- skip Markdown files" entry in step 6b's language convention list with a Markdown-specific rule
- The rule should check whether newly added `###` (or deeper) headings in Markdown files have at least one paragraph of explanatory text before the next sub-heading or code block
- This aligns with the repository's practice of using Markdown for skill definitions, where each section heading should have introductory context
- The PASS/WARN/N/A verdict logic in step 6c remains unchanged -- Markdown sections missing explanatory text count as undocumented symbols

## Acceptance Criteria
- [ ] Check 6 no longer blanket-skips Markdown files
- [ ] A Markdown-specific rule checks whether new headings have explanatory text
- [ ] New `###` headings without introductory paragraphs produce a WARN verdict
- [ ] Markdown files with properly documented sections produce a PASS verdict

## Test Requirements
- [ ] Verify the Markdown rule detects new headings without explanatory text
- [ ] Verify the Markdown rule passes for headings with introductory paragraphs
- [ ] Verify non-Markdown files are unaffected by the new rule
