## Repository
sdlc-plugins

## Target Branch
main

## Description
Add a Markdown-specific documentation checking rule to Check 6 (Documentation Coverage) in the style-conventions sub-agent. Currently Check 6 skips Markdown files entirely ("Markdown: not applicable -- skip Markdown files"), but this repository's skills are defined in Markdown files where section headings serve as the primary structural elements. The check should verify that new Markdown sections (identified by `###` or deeper headings) have at least one paragraph of introductory/explanatory text before any sub-sections or code blocks. This ensures documentation coverage extends to the repository's primary file type.

## Files to Modify
- `plugins/sdlc-workflow/skills/verify-pr/style-conventions.md` -- update Check 6 step 6b to replace the Markdown exclusion with a Markdown-specific rule that checks for introductory text after new section headings

## Implementation Notes
- In step 6b of Check 6, replace the current "Markdown: not applicable -- skip Markdown files" entry with a Markdown-specific rule
- The Markdown rule should: (1) identify new `###` or deeper headings in the diff, (2) check whether at least one paragraph of text follows the heading before the next heading or code block
- Follow the same structure as other language entries in step 6b (Rust, TypeScript/Java, Python, Go)
- The existing PASS/WARN/N/A verdict logic in step 6c should work without modification -- undocumented Markdown sections count as undocumented symbols

## Acceptance Criteria
- [ ] Check 6 step 6b includes a Markdown-specific rule for checking section documentation
- [ ] The Markdown rule checks that new headings (`###` or deeper) have at least one paragraph of explanatory text before sub-sections or code blocks
- [ ] The "Markdown: not applicable -- skip Markdown files" exclusion is removed
- [ ] Existing Check 6 behavior for non-Markdown files is unchanged

## Test Requirements
- [ ] Verify Check 6 flags a new Markdown heading with no introductory text
- [ ] Verify Check 6 passes a new Markdown heading that has explanatory text
- [ ] Verify Check 6 still works correctly for Rust, TypeScript, Python, and Go files

## Review Context
**Original review comment (comment 50001) by reviewer-b on style-conventions.md line 310:**
> The Check 6 description says 'Markdown: not applicable -- skip Markdown files' but this is a documentation-heavy repository where skills are defined in Markdown. The check should still verify that new Markdown sections have introductory text explaining their purpose, even if traditional doc comments don't apply. Consider adding a Markdown-specific rule that checks whether new `###` headings have at least one paragraph of explanatory text before any sub-sections or code blocks.

## Target PR
https://github.com/mrizzi/sdlc-plugins/pull/747
