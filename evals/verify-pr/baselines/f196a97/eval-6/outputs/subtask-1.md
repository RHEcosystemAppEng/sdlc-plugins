## Repository
sdlc-plugins

## Target Branch
main

## Description
Add a Markdown-specific documentation rule to Check 6 (Documentation Coverage) in the style-conventions sub-agent. Currently, Check 6 skips Markdown files entirely ("Markdown: not applicable — skip Markdown files"), but this repository is documentation-heavy with skills defined in Markdown. The check should verify that new Markdown sections (headings) have introductory text explaining their purpose.

This addresses review feedback from reviewer-b on PR #747: the Markdown exclusion is too broad for documentation-focused repositories. A Markdown-specific rule should check whether new `###` headings have at least one paragraph of explanatory text before any sub-sections or code blocks.

## Files to Modify
- `plugins/sdlc-workflow/skills/verify-pr/style-conventions.md` — replace the "Markdown: not applicable — skip Markdown files" bullet in Check 6b with a Markdown-specific rule that checks new headings for explanatory text

## Implementation Notes
- In section "6b — Check Documentation Comments", replace the Markdown exclusion bullet with a new rule: for Markdown files, check whether new `###` (or deeper) headings introduced in the PR diff have at least one paragraph of explanatory text before any sub-sections or code blocks
- Follow the pattern of the existing language-specific rules in 6b (Rust, TypeScript/Java, Python, Go) — each is a bullet with the language name, colon, and the convention description
- The rule should apply to headings at level 3 (`###`) and deeper, as top-level and second-level headings typically serve as structural titles
- A heading "has explanatory text" if there is at least one non-empty paragraph between the heading line and the next heading or code block
- If a new heading is immediately followed by another heading or a code block with no intervening text, it should be flagged as lacking documentation

## Review Context
reviewer-b commented on `plugins/sdlc-workflow/skills/verify-pr/style-conventions.md` line 310:

> The Check 6 description says 'Markdown: not applicable — skip Markdown files' but this is a documentation-heavy repository where skills are defined in Markdown. The check should still verify that new Markdown sections have introductory text explaining their purpose, even if traditional doc comments don't apply. Consider adding a Markdown-specific rule that checks whether new `###` headings have at least one paragraph of explanatory text before any sub-sections or code blocks.

## Target PR
https://github.com/mrizzi/sdlc-plugins/pull/747

## Acceptance Criteria
- [ ] Check 6b includes a Markdown-specific rule for verifying heading documentation
- [ ] The Markdown rule checks that new `###` headings have at least one paragraph of explanatory text before sub-sections or code blocks
- [ ] The previous "Markdown: not applicable — skip Markdown files" exclusion is removed or replaced
- [ ] Markdown files with properly documented headings produce PASS for Check 6
- [ ] Markdown files with undocumented headings (no explanatory text after heading) produce WARN for Check 6
