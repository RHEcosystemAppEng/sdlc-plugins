# Sub-task 1: Add Markdown-specific documentation coverage rule to Check 6

**Type:** Review feedback sub-task
**Parent:** TC-9106
**Labels:** ai-generated-jira, review-feedback
**Source:** Review comment 50001 from reviewer-b

---

## Repository
sdlc-plugins

## Target Branch
main

## Description
Modify Check 6 (Documentation Coverage) in the style-conventions sub-agent to add a Markdown-specific documentation coverage rule instead of skipping Markdown files entirely. The current implementation marks Markdown as "not applicable" and skips all Markdown files, but this repository is heavily Markdown-based with skills defined in Markdown. The check should verify that new Markdown sections have introductory text explaining their purpose.

## Files to Modify
- `plugins/sdlc-workflow/skills/verify-pr/style-conventions.md` -- update Check 6 step 6b to replace the "Markdown: not applicable" rule with a Markdown-specific documentation coverage rule

## Implementation Notes
- In step 6b (Check Documentation Comments), replace the current Markdown entry:
  `- **Markdown:** not applicable --- skip Markdown files`
  with a rule that checks whether new `###` headings have at least one paragraph of explanatory text before any sub-sections or code blocks.
- The Markdown rule should check for new heading definitions (lines starting with `#`, `##`, `###`, etc.) in the diff and verify each has at least one paragraph of text following it before the next heading or code block.
- Follow the same pattern as other language-specific rules in step 6b: describe the convention clearly so the sub-agent knows exactly what to look for.
- The verdict logic in step 6c remains unchanged (PASS when all documented, WARN when any lack documentation, N/A when no new symbols/sections).

## Acceptance Criteria
- [ ] Check 6 step 6b includes a Markdown-specific rule for documentation coverage
- [ ] The Markdown rule checks that new heading sections have introductory explanatory text
- [ ] The rule specifically checks `###` headings (and potentially other heading levels) for at least one paragraph before sub-sections or code blocks
- [ ] The "not applicable --- skip Markdown files" entry is removed or replaced

## Review Context
**Comment ID:** 50001
**Reviewer:** reviewer-b
**File:** plugins/sdlc-workflow/skills/verify-pr/style-conventions.md, line 310
**Comment text:**
> The Check 6 description says 'Markdown: not applicable --- skip Markdown files' but this is a documentation-heavy repository where skills are defined in Markdown. The check should still verify that new Markdown sections have introductory text explaining their purpose, even if traditional doc comments don't apply. Consider adding a Markdown-specific rule that checks whether new `###` headings have at least one paragraph of explanatory text before any sub-sections or code blocks.

## Target PR
https://github.com/RHEcosystemAppEng/sdlc-plugins/pull/747
