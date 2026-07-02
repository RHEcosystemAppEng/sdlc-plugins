## Repository
sdlc-plugins

## Target Branch
main

## Description
Add a Markdown-specific documentation coverage rule to Check 6 in the style-conventions sub-agent. The current implementation skips Markdown files entirely ("Markdown: not applicable -- skip Markdown files"), but this repository defines skills in Markdown files, so new Markdown sections should still be checked for introductory explanatory text.

## Files to Modify
- `plugins/sdlc-workflow/skills/verify-pr/style-conventions.md` -- update Check 6, sub-step 6b to replace the Markdown exclusion with a Markdown-specific rule that checks whether new `###` headings have at least one paragraph of explanatory text before any sub-sections or code blocks

## Implementation Notes
- The current Markdown rule in Check 6 sub-step 6b reads: "Markdown: not applicable -- skip Markdown files"
- Replace this with a Markdown-specific check: for new `###` (or deeper) headings introduced in the diff, verify that at least one paragraph of explanatory text exists between the heading and the next sub-section heading or code block
- This aligns with the repository's documentation-heavy nature where skills are defined in Markdown
- Follow the same structure as the other language-specific rules in sub-step 6b

## Acceptance Criteria
- [ ] Check 6 no longer skips Markdown files entirely
- [ ] Check 6 includes a Markdown-specific rule that verifies new headings have introductory explanatory text
- [ ] The Markdown rule checks for at least one paragraph of text before sub-sections or code blocks under new headings
- [ ] Existing language-specific rules (Rust, TypeScript/Java, Python, Go) are unchanged

## Test Requirements
- [ ] Verify that a new Markdown heading with explanatory text produces PASS
- [ ] Verify that a new Markdown heading without explanatory text (immediately followed by a sub-heading or code block) produces WARN
- [ ] Verify that Markdown files with no new headings produce N/A for the Markdown-specific check

## Review Context
Reviewer reviewer-b commented on `plugins/sdlc-workflow/skills/verify-pr/style-conventions.md` line 310:

> The Check 6 description says 'Markdown: not applicable -- skip Markdown files' but this is a documentation-heavy repository where skills are defined in Markdown. The check should still verify that new Markdown sections have introductory text explaining their purpose, even if traditional doc comments don't apply. Consider adding a Markdown-specific rule that checks whether new `###` headings have at least one paragraph of explanatory text before any sub-sections or code blocks.

## Target PR
https://github.com/mrizzi/sdlc-plugins/pull/747
