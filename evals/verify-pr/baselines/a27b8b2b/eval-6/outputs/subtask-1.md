## Repository
sdlc-plugins

## Target Branch
main

## Description
Add a Markdown-specific documentation rule to Check 6 (Documentation Coverage) in the style-conventions sub-agent. Currently Check 6 skips Markdown files entirely with the rule "Markdown: not applicable -- skip Markdown files." However, since sdlc-plugins is a documentation-heavy repository where skills are defined in Markdown, this leaves a coverage gap. The new rule should verify that new Markdown section headings (`###` and below) have at least one paragraph of introductory text before any sub-sections or code blocks, ensuring documentation sections include explanatory context.

## Files to Modify
- `plugins/sdlc-workflow/skills/verify-pr/style-conventions.md` -- update Check 6 section 6b to replace the Markdown skip rule with a Markdown-specific documentation check for section heading introductory text

## Implementation Notes
- In section "6b -- Check Documentation Comments", replace the current Markdown rule:
  ```
  - **Markdown:** not applicable -- skip Markdown files
  ```
  with a Markdown-specific rule that checks whether new `###` headings (and deeper levels) have at least one paragraph of explanatory text before any sub-sections or code blocks.
- The rule should apply to headings introduced in the PR diff (lines with `+` prefix containing `###` or deeper heading markers).
- A heading "has explanatory text" if there is at least one non-empty paragraph between the heading line and the next heading or code block fence.
- Follow the structure of the other language-specific rules in section 6b (Rust, TypeScript/Java, Python, Go).
- The existing N/A early-exit in section 6a should still apply when no new symbols AND no new Markdown headings are found.

## Acceptance Criteria
- [ ] Check 6 section 6b includes a Markdown-specific rule for documentation coverage
- [ ] The rule checks that new `###` (and deeper) headings have at least one paragraph of introductory text before sub-sections or code blocks
- [ ] The rule replaces the current "Markdown: not applicable" skip instruction
- [ ] Markdown headings without introductory text are flagged as undocumented in Check 6's verdict
- [ ] Headings with explanatory text are not flagged

## Review Context
**Comment ID:** 50001
**Author:** reviewer-b
**File:** `plugins/sdlc-workflow/skills/verify-pr/style-conventions.md`, line 310
**Original comment:**
> The Check 6 description says 'Markdown: not applicable -- skip Markdown files' but this is a documentation-heavy repository where skills are defined in Markdown. The check should still verify that new Markdown sections have introductory text explaining their purpose, even if traditional doc comments don't apply. Consider adding a Markdown-specific rule that checks whether new `###` headings have at least one paragraph of explanatory text before any sub-sections or code blocks.

## Target PR
https://github.com/mrizzi/sdlc-plugins/pull/747
