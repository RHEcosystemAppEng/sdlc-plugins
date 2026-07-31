## Repository
sdlc-plugins

## Target Branch
main

## Description
Add a Markdown-specific documentation rule to Check 6 (Documentation Coverage) in the verify-pr style-conventions sub-agent. Currently, Check 6 skips Markdown files entirely ("Markdown: not applicable -- skip Markdown files"), but this is inappropriate for the sdlc-plugins repository where skills are defined in Markdown (SKILL.md files). The check should verify that new Markdown sections have introductory explanatory text.

## Files to Modify
- `plugins/sdlc-workflow/skills/verify-pr/style-conventions.md` -- replace the Markdown exclusion rule in Check 6 step 6b with a Markdown-specific documentation rule that checks whether new `###` headings have at least one paragraph of explanatory text before any sub-sections or code blocks

## Implementation Notes
- In step 6b of Check 6, the current rule is: "Markdown: not applicable -- skip Markdown files"
- Replace this with a rule that applies to Markdown files: check whether new section headings (e.g., `###` level headings added in the diff) have at least one paragraph of explanatory text before any sub-sections or code blocks
- Follow the structure of existing language-specific rules in step 6b (Rust, TypeScript/Java, Python, Go)
- The rule should scan for new heading lines in the diff (lines starting with `###` or deeper) and verify that explanatory text follows before the next heading or code block
- This aligns with the repository's nature as documented in CONVENTIONS.md: "This is a documentation-heavy repository -- skills are defined in Markdown (SKILL.md files) rather than traditional programming languages"

## Acceptance Criteria
- [ ] Check 6 step 6b includes a Markdown-specific documentation rule instead of skipping Markdown files
- [ ] The Markdown rule checks that new section headings have at least one paragraph of explanatory text
- [ ] The rule handles the case where a heading is immediately followed by a sub-heading or code block (no explanatory text) as an undocumented symbol
- [ ] Existing language-specific rules (Rust, TypeScript/Java, Python, Go) remain unchanged

## Review Context
**PR Comment #50001** by reviewer-b on `plugins/sdlc-workflow/skills/verify-pr/style-conventions.md` line 310:

> The Check 6 description says 'Markdown: not applicable -- skip Markdown files' but this is a documentation-heavy repository where skills are defined in Markdown. The check should still verify that new Markdown sections have introductory text explaining their purpose, even if traditional doc comments don't apply. Consider adding a Markdown-specific rule that checks whether new `###` headings have at least one paragraph of explanatory text before any sub-sections or code blocks.

## Target PR
https://github.com/RHEcosystemAppEng/sdlc-plugins/pull/747
