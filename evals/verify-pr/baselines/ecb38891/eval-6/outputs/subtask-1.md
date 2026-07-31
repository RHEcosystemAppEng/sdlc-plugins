## Repository
sdlc-plugins

## Target Branch
TC-9106

## Description
Add a Markdown-specific documentation coverage rule to Check 6 in the Style/Conventions sub-agent. The current implementation blanket-excludes Markdown files ("Markdown: not applicable -- skip Markdown files"), but this repository is documentation-heavy with skills defined entirely in Markdown. The check should verify that new Markdown sections have introductory text explaining their purpose.

## Files to Modify
- `plugins/sdlc-workflow/skills/verify-pr/style-conventions.md` -- replace the Markdown exclusion in Check 6 step 6b with a Markdown-specific rule that checks whether new `###` headings have at least one paragraph of explanatory text before any sub-sections or code blocks

## Implementation Notes
- The current Check 6 step 6b lists "Markdown: not applicable -- skip Markdown files" which should be replaced with a Markdown-specific documentation coverage rule
- The Markdown rule should check whether new `###` headings (and potentially `##` headings) have at least one paragraph of explanatory text before any sub-sections or code blocks
- This is distinct from traditional doc comments -- Markdown sections serve as the documentation for skills, so their introductory text serves the same purpose as doc comments in code
- Follow the structure of existing language-specific rules in step 6b (Rust, TypeScript/Java, Python, Go)

## Acceptance Criteria
- [ ] Check 6 step 6b includes a Markdown-specific documentation rule instead of blanket exclusion
- [ ] The Markdown rule checks whether new section headings have introductory explanatory text
- [ ] The rule does not flag headings that already have explanatory paragraphs
- [ ] The existing language-specific rules (Rust, TypeScript/Java, Python, Go) remain unchanged

## Test Requirements
- [ ] Verify new Markdown headings without introductory text are flagged
- [ ] Verify new Markdown headings with introductory text are not flagged
- [ ] Verify existing language-specific doc comment detection is unaffected

## Review Context
Reviewer reviewer-b (comment 50001) on file `plugins/sdlc-workflow/skills/verify-pr/style-conventions.md` line 310:

> The Check 6 description says 'Markdown: not applicable -- skip Markdown files' but this is a documentation-heavy repository where skills are defined in Markdown. The check should still verify that new Markdown sections have introductory text explaining their purpose, even if traditional doc comments don't apply. Consider adding a Markdown-specific rule that checks whether new ### headings have at least one paragraph of explanatory text before any sub-sections or code blocks.

## Target PR
https://github.com/RHEcosystemAppEng/sdlc-plugins/pull/747
