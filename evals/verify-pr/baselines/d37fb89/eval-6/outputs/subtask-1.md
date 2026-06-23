## Repository
sdlc-plugins

## Target Branch
main

## Description
Add a Markdown-specific documentation coverage rule to Check 6 in the style-conventions sub-agent. The current implementation blanket-skips Markdown files, but this repository defines skills and documentation primarily in Markdown. The new rule should check whether new `###` headings (sections) have at least one paragraph of explanatory text before any sub-sections or code blocks, ensuring that new Markdown sections are self-documenting.

## Files to Modify
- `plugins/sdlc-workflow/skills/verify-pr/style-conventions.md` -- update Check 6 section 6b to replace the "Markdown: not applicable" exclusion with a Markdown-specific documentation rule that checks for introductory text after new `###` headings

## Implementation Notes
- In section 6b of Check 6 (Documentation Coverage), replace the line "**Markdown:** not applicable -- skip Markdown files" with a Markdown-specific rule
- The rule should scan for new `###` heading lines in the PR diff (lines starting with `+### `)
- For each new heading, verify that at least one paragraph of explanatory text follows before the next sub-section heading or code block fence
- If a new `###` heading has no introductory text (immediately followed by another heading, code block, or list without explanation), flag it as undocumented
- Follow the existing structure of Check 6's language-specific patterns for consistency

## Acceptance Criteria
- [ ] Check 6 section 6b includes a Markdown-specific rule for documentation coverage
- [ ] The Markdown rule checks that new `###` headings have at least one paragraph of explanatory text
- [ ] The Markdown rule flags headings that lack introductory text before sub-sections or code blocks
- [ ] The blanket "skip Markdown files" exclusion is removed

## Test Requirements
- [ ] Verify the Markdown rule detects a new `###` heading without introductory text
- [ ] Verify the Markdown rule passes when a new `###` heading has explanatory text
- [ ] Verify the Markdown rule handles headings followed immediately by code blocks

## Review Context
**Original review comment (id: 50001) by reviewer-b on `plugins/sdlc-workflow/skills/verify-pr/style-conventions.md` line 310:**

> The Check 6 description says 'Markdown: not applicable -- skip Markdown files' but this is a documentation-heavy repository where skills are defined in Markdown. The check should still verify that new Markdown sections have introductory text explaining their purpose, even if traditional doc comments don't apply. Consider adding a Markdown-specific rule that checks whether new `###` headings have at least one paragraph of explanatory text before any sub-sections or code blocks.

## Target PR
https://github.com/mrizzi/sdlc-plugins/pull/747
