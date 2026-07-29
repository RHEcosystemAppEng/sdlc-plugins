## Repository
sdlc-plugins

## Target Branch
main

## Description
Add Markdown-specific documentation checking to Check 6 (Documentation Coverage) in the style-conventions sub-agent. Currently, Check 6 skips Markdown files entirely with the rule "Markdown: not applicable -- skip Markdown files." Since this is a documentation-heavy repository where skills are defined in Markdown, the check should include a Markdown-specific rule that verifies new Markdown sections have introductory text explaining their purpose.

Replace the blanket "skip Markdown files" rule with a Markdown-specific check: for each new `###` heading introduced in the PR diff, verify that at least one paragraph of explanatory text exists before any sub-sections or code blocks.

## Files to Modify
- `plugins/sdlc-workflow/skills/verify-pr/style-conventions.md` -- replace the "Markdown: not applicable" entry in Check 6b with a Markdown-specific rule for heading documentation

## Implementation Notes
- In the Check 6b language-specific doc comment patterns list, replace the Markdown bullet ("not applicable -- skip Markdown files") with a new rule: verify that new `###`-level headings have at least one paragraph of explanatory text before any sub-sections or code blocks
- The Markdown check should scan added lines in the PR diff for new `###` headings, then verify that the lines following each heading contain explanatory prose (not immediately followed by another heading, code block, or end of section)
- Follow the structure of the existing language-specific checks (Rust, TypeScript/Java, Python, Go) for consistency
- The verdict logic in Check 6c remains unchanged: PASS (all documented), WARN (any undocumented), N/A (no new symbols/headings)
- Consider what constitutes "explanatory text" for Markdown: at minimum one non-empty paragraph that is not a code block, heading, or list without context

## Acceptance Criteria
- [ ] Check 6b includes a Markdown-specific rule for verifying new headings have explanatory text
- [ ] The Markdown rule checks that new `###` headings are followed by at least one paragraph of explanatory text
- [ ] The blanket "skip Markdown files" rule is removed
- [ ] PASS, WARN, and N/A verdicts apply correctly when Markdown files with new headings are present
- [ ] Existing language-specific checks (Rust, TypeScript/Java, Python, Go) are unchanged

## Review Context
**Comment ID:** 50001
**Author:** reviewer-b
**File:** plugins/sdlc-workflow/skills/verify-pr/style-conventions.md, line 310

**Original comment:**
> The Check 6 description says 'Markdown: not applicable -- skip Markdown files' but this is a documentation-heavy repository where skills are defined in Markdown. The check should still verify that new Markdown sections have introductory text explaining their purpose, even if traditional doc comments don't apply. Consider adding a Markdown-specific rule that checks whether new `###` headings have at least one paragraph of explanatory text before any sub-sections or code blocks.

## Target PR
https://github.com/mrizzi/sdlc-plugins/pull/747
