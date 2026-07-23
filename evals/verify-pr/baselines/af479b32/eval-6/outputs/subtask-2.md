## Repository
sdlc-plugins

## Target Branch
main

## Description
Add a Markdown-specific documentation coverage rule to Check 6 in the style-conventions sub-agent. The current implementation skips Markdown files entirely ("Markdown: not applicable -- skip Markdown files"), but this repository is documentation-heavy with skills defined in Markdown. The check should verify that new Markdown sections have introductory text explaining their purpose.

## Files to Modify
- `plugins/sdlc-workflow/skills/verify-pr/style-conventions.md` -- replace the Markdown "not applicable" rule in Check 6 step 6b with a Markdown-specific documentation coverage rule that checks whether new `###` headings have at least one paragraph of explanatory text before any sub-sections or code blocks

## Implementation Notes
- The current Check 6b lists language-specific doc comment patterns and has "Markdown: not applicable -- skip Markdown files" as the last entry
- Replace this with a Markdown-specific rule: for new `###` (or deeper) headings introduced in the PR diff, verify that at least one paragraph of explanatory text follows the heading before the next heading or code block
- This is specific to documentation-heavy repositories where skills and workflows are defined in Markdown files
- Follow the same pattern as other language-specific rules in Check 6b -- the rule should be a concise description of what to check

## Acceptance Criteria
- [ ] Check 6b includes a Markdown-specific documentation coverage rule instead of skipping Markdown files
- [ ] The Markdown rule checks that new headings have introductory/explanatory text
- [ ] The Markdown rule does not flag headings that already have explanatory text

## Test Requirements
- [ ] Verify Check 6 correctly identifies undocumented new Markdown headings (headings without explanatory text)
- [ ] Verify Check 6 does not flag Markdown headings that have explanatory text

## Review Context
Reviewer reviewer-b commented on `plugins/sdlc-workflow/skills/verify-pr/style-conventions.md` line 310:

> The Check 6 description says 'Markdown: not applicable -- skip Markdown files' but this is a documentation-heavy repository where skills are defined in Markdown. The check should still verify that new Markdown sections have introductory text explaining their purpose, even if traditional doc comments don't apply. Consider adding a Markdown-specific rule that checks whether new `###` headings have at least one paragraph of explanatory text before any sub-sections or code blocks.

## Target PR
https://github.com/RHEcosystemAppEng/sdlc-plugins/pull/747
