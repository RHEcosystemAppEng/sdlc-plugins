## Repository
sdlc-plugins

## Target Branch
main

## Description
Add Markdown-specific documentation coverage logic to Check 6 in the style-conventions sub-agent. The current implementation blanket-skips Markdown files, but in documentation-heavy repositories where skills and workflows are defined in Markdown, new sections should be checked for introductory explanatory text. Add a Markdown-specific rule that verifies new `###` headings have at least one paragraph of explanatory text before any sub-sections or code blocks.

## Files to Modify
- `plugins/sdlc-workflow/skills/verify-pr/style-conventions.md` -- update Check 6 section 6b to replace the blanket Markdown exclusion with a Markdown-specific documentation coverage rule

## Implementation Notes
- Replace the current rule "Markdown: not applicable -- skip Markdown files" in step 6b with a Markdown-specific check
- The Markdown check should verify that new `###` (or deeper) headings have at least one paragraph of explanatory text before any sub-sections or code blocks
- This applies specifically to repositories where Markdown files are functional artifacts (skill definitions, workflow documentation) rather than pure prose documentation
- Keep the check lightweight: only verify presence of explanatory text, not its quality or completeness
- Follow the same documented/undocumented recording pattern used for other languages in step 6b

## Acceptance Criteria
- [ ] Check 6 no longer blanket-skips Markdown files
- [ ] Check 6 includes a Markdown-specific rule that checks whether new headings have explanatory introductory text
- [ ] The Markdown rule checks for at least one paragraph of text before sub-sections or code blocks under new headings
- [ ] Existing language-specific doc comment checks (Rust, TypeScript/Java, Python, Go) are unchanged

## Test Requirements
- [ ] Verify the Markdown rule flags new headings without explanatory text
- [ ] Verify the Markdown rule passes new headings that have introductory text
- [ ] Verify non-Markdown files are unaffected by the change

## Review Context
Reviewer reviewer-b commented on `plugins/sdlc-workflow/skills/verify-pr/style-conventions.md` line 310:

> The Check 6 description says 'Markdown: not applicable -- skip Markdown files' but this is a documentation-heavy repository where skills are defined in Markdown. The check should still verify that new Markdown sections have introductory text explaining their purpose, even if traditional doc comments don't apply. Consider adding a Markdown-specific rule that checks whether new `###` headings have at least one paragraph of explanatory text before any sub-sections or code blocks.

## Target PR
https://github.com/RHEcosystemAppEng/sdlc-plugins/pull/747
