## Repository
sdlc-plugins

## Target Branch
main

## Description
Add a Markdown-specific documentation rule to Check 6 (Documentation Coverage) in the Style/Conventions sub-agent. Currently, Check 6 skips Markdown files entirely with "Markdown: not applicable -- skip Markdown files." However, since sdlc-plugins is a documentation-heavy repository where skills are defined in Markdown (SKILL.md files), the check should verify that new Markdown sections have introductory text explaining their purpose.

## Files to Modify
- `plugins/sdlc-workflow/skills/verify-pr/style-conventions.md` -- update Check 6's step 6b to replace the Markdown exclusion with a Markdown-specific rule that checks whether new `###` headings have at least one paragraph of explanatory text before any sub-sections or code blocks

## Implementation Notes
- Replace the current "Markdown: not applicable -- skip Markdown files" entry in step 6b with a Markdown-specific documentation rule
- The rule should check that new `###` (or deeper) headings introduced in the PR diff have at least one paragraph of explanatory text before any sub-sections or code blocks
- This is consistent with the repository's documentation-first nature where skills are authored in Markdown
- Follow the same pattern as other language entries in step 6b (language name, doc comment convention description)

## Acceptance Criteria
- [ ] Check 6 step 6b includes a Markdown-specific rule instead of skipping Markdown files
- [ ] The Markdown rule checks whether new headings have introductory explanatory text
- [ ] The rule applies to `###` and deeper headings
- [ ] The rule checks for at least one paragraph of text before sub-sections or code blocks

## Review Context
> The Check 6 description says 'Markdown: not applicable -- skip Markdown files' but this is a documentation-heavy repository where skills are defined in Markdown. The check should still verify that new Markdown sections have introductory text explaining their purpose, even if traditional doc comments don't apply. Consider adding a Markdown-specific rule that checks whether new `###` headings have at least one paragraph of explanatory text before any sub-sections or code blocks.

- **Reviewer:** reviewer-b
- **File:** `plugins/sdlc-workflow/skills/verify-pr/style-conventions.md`, line 310
- **Comment ID:** 50001

## Target PR
https://github.com/mrizzi/sdlc-plugins/pull/747
