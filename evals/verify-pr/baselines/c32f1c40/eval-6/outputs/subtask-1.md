## Repository
sdlc-plugins

## Target Branch
main

## Description
Add a Markdown-specific documentation coverage rule to Check 6 in the Style/Conventions sub-agent. The current implementation skips Markdown files entirely ("Markdown: not applicable -- skip Markdown files"), but since this is a documentation-heavy repository where skills are defined in Markdown, Check 6 should verify that new Markdown sections have introductory explanatory text. Specifically, add a rule that checks whether new `###` headings have at least one paragraph of explanatory text before any sub-sections or code blocks.

## Files to Modify
- `plugins/sdlc-workflow/skills/verify-pr/style-conventions.md` -- update Check 6 step 6b to add a Markdown-specific rule instead of skipping Markdown files entirely

## Implementation Notes
- In step 6b of Check 6, replace the "Markdown: not applicable -- skip Markdown files" entry with a Markdown-specific rule
- The new rule should check whether new `###` (or deeper) headings introduced in the PR diff have at least one paragraph of explanatory text before the next sub-section heading or code block
- A heading followed immediately by another heading or a fenced code block (without intervening prose) should be flagged as lacking documentation
- Follow the same pattern as the other language-specific entries in step 6b (Rust, TypeScript/Java, Python, Go)
- The verdict logic in step 6c remains the same: PASS if all new sections have explanatory text, WARN if any lack it, N/A if no new sections are introduced

## Acceptance Criteria
- [ ] Check 6 step 6b includes a Markdown-specific documentation rule instead of "not applicable"
- [ ] The Markdown rule checks that new headings (`###` and deeper) have at least one paragraph of explanatory text
- [ ] New headings followed immediately by another heading or code block (no intervening prose) are flagged as undocumented
- [ ] The existing verdict logic (PASS/WARN/N/A) applies correctly to Markdown sections

## Test Requirements
- [ ] Verify the Markdown rule flags a new heading with no explanatory text before a sub-heading
- [ ] Verify the Markdown rule flags a new heading with no explanatory text before a code block
- [ ] Verify the Markdown rule does not flag a heading that has a paragraph of explanatory text
- [ ] Verify N/A verdict when no new Markdown headings are introduced

## Review Context
**Comment ID:** 50001
**Author:** reviewer-b
**File:** `plugins/sdlc-workflow/skills/verify-pr/style-conventions.md`, line 310
**Comment text:**
> The Check 6 description says 'Markdown: not applicable -- skip Markdown files' but this is a documentation-heavy repository where skills are defined in Markdown. The check should still verify that new Markdown sections have introductory text explaining their purpose, even if traditional doc comments don't apply. Consider adding a Markdown-specific rule that checks whether new `###` headings have at least one paragraph of explanatory text before any sub-sections or code blocks.

## Target PR
https://github.com/mrizzi/sdlc-plugins/pull/747
