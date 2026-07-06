## Repository
sdlc-plugins

## Target Branch
main

## Description
Add a Markdown-specific documentation rule to Check 6 (Documentation Coverage) in the style-conventions sub-agent. Currently, Check 6 skips Markdown files entirely ("Markdown: not applicable -- skip Markdown files"), but this repository is documentation-heavy with skills defined in Markdown. The check should verify that new Markdown sections (new `###` headings) have at least one paragraph of introductory/explanatory text before any sub-sections or code blocks.

## Files to Modify
- `plugins/sdlc-workflow/skills/verify-pr/style-conventions.md` -- add a Markdown-specific rule under Check 6b that checks whether new `###` headings in Markdown files have at least one paragraph of explanatory text before sub-sections or code blocks; update the "Markdown: not applicable" entry to reference the new Markdown-specific rule

## Implementation Notes
- The existing Check 6b lists language-specific doc comment patterns. Replace the current Markdown entry ("Markdown: not applicable -- skip Markdown files") with a Markdown-specific rule.
- The Markdown rule should check for new `###` headings (identified by `+` prefix lines starting with `###` in the diff) and verify that at least one paragraph of text follows before the next heading or code block.
- This is different from traditional doc comments -- instead of checking for a comment preceding a definition, check for explanatory prose following a section heading.
- Follow the structure of the existing language entries in Check 6b for consistency.
- The N/A condition in Check 6a still applies: if no new symbols AND no new Markdown headings are found, the verdict remains N/A.

## Acceptance Criteria
- [ ] Check 6b includes a Markdown-specific rule for verifying new `###` headings have explanatory text
- [ ] The Markdown rule checks that at least one paragraph exists between a new heading and the next sub-section or code block
- [ ] The previous "Markdown: not applicable" entry is replaced or updated to reference the new rule
- [ ] Check 6 correctly identifies undocumented new Markdown sections (headings without explanatory text)
- [ ] Check 6 does not flag Markdown headings that already have explanatory text following them

## Test Requirements
- [ ] Verify Check 6 flags new Markdown headings without explanatory text
- [ ] Verify Check 6 passes new Markdown headings with explanatory paragraphs
- [ ] Verify Check 6 still produces N/A when no new headings or symbols are present

## Review Context
**Original review comment (comment 50001, reviewer-b):**
> The Check 6 description says 'Markdown: not applicable -- skip Markdown files' but this is a documentation-heavy repository where skills are defined in Markdown. The check should still verify that new Markdown sections have introductory text explaining their purpose, even if traditional doc comments don't apply. Consider adding a Markdown-specific rule that checks whether new `###` headings have at least one paragraph of explanatory text before any sub-sections or code blocks.

**File reference:** `plugins/sdlc-workflow/skills/verify-pr/style-conventions.md`, line 310

## Target PR
https://github.com/mrizzi/sdlc-plugins/pull/747
