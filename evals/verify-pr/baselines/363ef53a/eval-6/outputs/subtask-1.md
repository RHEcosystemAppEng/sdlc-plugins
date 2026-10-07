## Repository
sdlc-plugins

## Target Branch
main

## Description
Replace the blanket Markdown exclusion in Check 6 (Documentation Coverage) with a Markdown-specific documentation rule. The current check says "Markdown: not applicable -- skip Markdown files" but this repository is documentation-heavy with skills defined in Markdown. The check should verify that new Markdown sections (headings) have introductory explanatory text, adapting the documentation coverage concept to Markdown's structure.

## Files to Modify
- `plugins/sdlc-workflow/skills/verify-pr/style-conventions.md` -- replace the Markdown exclusion in Check 6 step 6b with a Markdown-specific rule that checks whether new `###` headings have at least one paragraph of explanatory text before any sub-sections or code blocks

## Implementation Notes
- In step 6b's language-specific doc comment patterns list, replace the current entry:
  `- **Markdown:** not applicable -- skip Markdown files`
  with a Markdown-specific rule, e.g.:
  `- **Markdown:** new `###` (or deeper) headings must have at least one paragraph of explanatory text before any sub-sections or code blocks`
- The check should scan Markdown files in the PR diff for new heading lines (lines starting with `###` or deeper that appear with a `+` prefix)
- For each new heading, verify that at least one paragraph of text appears between the heading and the next heading or code block
- Follow the same verdict logic: documented (has explanatory text) or undocumented (heading immediately followed by a sub-heading or code block with no explanatory paragraph)

## Acceptance Criteria
- [ ] Check 6 step 6b includes a Markdown-specific documentation rule instead of blanket exclusion
- [ ] The Markdown rule checks that new headings have at least one paragraph of explanatory text
- [ ] Markdown files are no longer skipped entirely by Check 6
- [ ] The existing language-specific rules (Rust, TypeScript/Java, Python, Go) remain unchanged

## Review Context
**Comment ID:** 50001
**Author:** reviewer-b
**File:** plugins/sdlc-workflow/skills/verify-pr/style-conventions.md, line 310
**Comment text:**
> The Check 6 description says 'Markdown: not applicable -- skip Markdown files' but this is a documentation-heavy repository where skills are defined in Markdown. The check should still verify that new Markdown sections have introductory text explaining their purpose, even if traditional doc comments don't apply. Consider adding a Markdown-specific rule that checks whether new `###` headings have at least one paragraph of explanatory text before any sub-sections or code blocks.

## Target PR
https://github.com/RHEcosystemAppEng/sdlc-plugins/pull/747
