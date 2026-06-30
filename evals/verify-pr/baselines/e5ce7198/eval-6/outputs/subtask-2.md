## Repository
sdlc-plugins

## Target Branch
TC-9106

## Description
Address reviewer feedback on PR #747: add a Markdown-specific documentation coverage rule to Check 6 in the style-conventions sub-agent. Currently Check 6 skips Markdown files entirely, but since this is a documentation-heavy repository where skills are defined in Markdown, the check should verify that new Markdown sections have introductory text explaining their purpose.

## Target PR
https://github.com/mrizzi/sdlc-plugins/pull/747

## Review Context
**Reviewer:** reviewer-b (comment id 50001)
**File:** plugins/sdlc-workflow/skills/verify-pr/style-conventions.md, line 310
**Comment:** "The Check 6 description says 'Markdown: not applicable -- skip Markdown files' but this is a documentation-heavy repository where skills are defined in Markdown. The check should still verify that new Markdown sections have introductory text explaining their purpose, even if traditional doc comments don't apply. Consider adding a Markdown-specific rule that checks whether new `###` headings have at least one paragraph of explanatory text before any sub-sections or code blocks."

## Files to Modify
- `plugins/sdlc-workflow/skills/verify-pr/style-conventions.md` -- replace the "Markdown: not applicable -- skip Markdown files" rule in Check 6b with a Markdown-specific rule that checks new `###` headings for introductory text

## Implementation Notes
- In section 6b (Check Documentation Comments), replace the Markdown bullet from "not applicable -- skip Markdown files" to a rule that checks for explanatory text
- The Markdown-specific rule should: identify new `###` (or deeper) headings in the diff, and verify each has at least one paragraph of explanatory text before any sub-sections or code blocks
- Keep the existing language-specific patterns (Rust, TypeScript/Java, Python, Go) unchanged
- The WARN verdict should trigger if any new Markdown heading lacks introductory text

## Acceptance Criteria
- [ ] Check 6b includes a Markdown-specific documentation rule instead of skipping Markdown files
- [ ] The Markdown rule checks that new `###` headings have at least one paragraph of explanatory text before sub-sections or code blocks
- [ ] The WARN verdict fires when a new Markdown heading lacks introductory text
- [ ] Existing language-specific doc comment patterns remain unchanged

## Test Requirements
- [ ] Verify that a new Markdown heading with introductory text produces PASS
- [ ] Verify that a new Markdown heading without introductory text produces WARN
- [ ] Verify that non-Markdown files are unaffected by the new rule
