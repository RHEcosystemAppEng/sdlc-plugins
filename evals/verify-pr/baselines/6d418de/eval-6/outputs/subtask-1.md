## Repository
sdlc-plugins

## Target Branch
main

## Description
Add a Markdown-specific documentation rule to Check 6 (Documentation Coverage) in the Style/Conventions sub-agent. The current implementation blanket-skips Markdown files, but in documentation-heavy repositories where skills and workflows are defined in Markdown, new sections should be verified for introductory explanatory text. This rule should check whether new `###` headings have at least one paragraph of explanatory text before any sub-sections or code blocks.

## Files to Modify
- `plugins/sdlc-workflow/skills/verify-pr/style-conventions.md` -- update the Check 6 section to replace the blanket Markdown exclusion with a Markdown-specific documentation rule that verifies new headings have explanatory text

## Implementation Notes
- In the "6b -- Check Documentation Comments" section, replace the current "Markdown: not applicable -- skip Markdown files" bullet with a Markdown-specific rule
- The new Markdown rule should check whether new `###` (or deeper) headings introduced in the PR diff have at least one paragraph of explanatory text before any sub-sections or code blocks
- Follow the pattern of the other language-specific rules in step 6b (Rust, TypeScript/Java, Python, Go) -- each is a bullet describing what to look for
- The rule should be scoped to new headings only (lines with `+` prefix in the diff), consistent with step 6a's definition of "new"

## Review Context
Reviewer reviewer-b commented on `plugins/sdlc-workflow/skills/verify-pr/style-conventions.md` line 310:
> "The Check 6 description says 'Markdown: not applicable -- skip Markdown files' but this is a documentation-heavy repository where skills are defined in Markdown. The check should still verify that new Markdown sections have introductory text explaining their purpose, even if traditional doc comments don't apply. Consider adding a Markdown-specific rule that checks whether new `###` headings have at least one paragraph of explanatory text before any sub-sections or code blocks."

## Target PR
https://github.com/mrizzi/sdlc-plugins/pull/747

## Acceptance Criteria
- [ ] The Markdown exclusion ("not applicable -- skip Markdown files") is replaced with a Markdown-specific documentation rule
- [ ] The Markdown rule checks whether new `###` headings have at least one paragraph of explanatory text before sub-sections or code blocks
- [ ] The rule only applies to newly introduced headings (consistent with step 6a's "new" definition)
- [ ] The Documentation Coverage verdict correctly reflects missing explanatory text in Markdown files (WARN when missing, PASS when present)
