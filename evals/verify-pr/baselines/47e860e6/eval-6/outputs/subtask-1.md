# Sub-task: Add Markdown section-introduction rule to Check 6 Documentation Coverage

- **Issue Type:** Sub-task
- **Parent:** TC-9106
- **Labels:** `["ai-generated-jira", "review-feedback"]`
- **Link:** Blocks (inward: this sub-task → outward: TC-9106)

---

## Repository
sdlc-plugins

## Target Branch
main

## Description
Replace the blanket Markdown exclusion in Check 6 (Documentation Coverage) of the verify-pr Style/Conventions sub-agent with a Markdown-specific documentation rule. This repository defines its skills in Markdown, so skipping Markdown files makes Check 6 return N/A for almost every PR. The new rule must check that every newly added `###` heading in a changed Markdown file is followed by at least one paragraph of explanatory text before any sub-heading, list, table or fenced code block. This addresses reviewer-b's change request on PR #747.

## Files to Modify
- `plugins/sdlc-workflow/skills/verify-pr/style-conventions.md`: in Check 6, change 6a so new `###` headings in Markdown files count as documentable units, and replace the `- **Markdown:** not applicable — skip Markdown files` bullet in 6b with the section-introduction rule. Update 6c evidence wording so undocumented headings are reported with file path and line.
- `evals/verify-pr/evals.json`: add or update eval assertions to cover the new Markdown rule

## Implementation Notes
- Change only Check 6 (`### Check 6 — Documentation Coverage`, added by PR #747). Keep the 6a/6b/6c sub-step structure and the PASS/WARN/N/A verdict semantics.
- 6a: a Markdown symbol is "new" when a `+### <title>` line appears in the diff with no matching `-### <title>` line. This is the same new-vs-modified rule 6a already uses for code symbols.
- 6b Markdown rule: the first non-blank line after the new heading must be a prose paragraph, not another heading (`#`), list item (`-`, `*`, `1.`), table row (`|`) or code fence. A heading with no prose before its first sub-heading or code block counts as undocumented.
- Leave eval and test fixtures out of scope, e.g. `evals/*/files/*.md`. CONVENTIONS.md (§ Testing Conventions, "Fixture documentation") treats them as deliberate test material, not documentation.
- Keep the code-language rules (Rust `///`, TS/Java `/** */`, Python `"""`, Go `//`) unchanged.
- Model the new rule's wording on the existing language bullets in 6b, so all conventions stay in one list.

## Reuse Candidates
- `plugins/sdlc-workflow/skills/verify-pr/style-conventions.md::Check 6 — Documentation Coverage`: the check being extended
- `plugins/sdlc-workflow/skills/verify-pr/style-conventions.md::Check 3 — Test Documentation`: sibling doc-comment check, shows the per-item recording and evidence pattern
- `evals/verify-pr/files/pr-diff-with-eval-results.md`: fixture with the Check 6 diff, a natural base for a Markdown-heading scenario
- `evals/verify-pr/files/task-with-eval-results.md`: matching task fixture for TC-9106
- `evals/verify-pr/files/pr-reviews-with-evals.md`: review fixture with comment 50001, the origin of this request

## Acceptance Criteria
- [ ] Check 6b no longer skips Markdown files entirely
- [ ] Check 6 treats each newly added `###` heading in a non-fixture Markdown file as a symbol to check
- [ ] A new `###` heading followed by at least one prose paragraph before any sub-heading, list, table or code block counts as documented
- [ ] A new `###` heading followed directly by a sub-heading, list, table or code block counts as undocumented and produces WARN, with file path and line in the evidence
- [ ] Eval/test fixture Markdown files (`evals/*/files/`) are excluded from the Markdown rule
- [ ] Existing code-language doc-comment rules and the PASS/WARN/N/A semantics are unchanged

## Test Requirements
- [ ] Verify a diff adding a `###` heading with an introductory paragraph yields PASS for Documentation Coverage
- [ ] Verify a diff adding a `###` heading directly followed by a `####` sub-heading or code block yields WARN and names the heading
- [ ] Verify Markdown files under `evals/*/files/` are not flagged
- [ ] Update eval assertions in `evals/verify-pr/evals.json` to cover the Markdown section-introduction rule. Add a new eval case if no existing case exercises it

## Review Context
- **Reviewer:** reviewer-b (review 40002, `CHANGES_REQUESTED`)
- **Comment ID:** 50001
- **File/line:** `plugins/sdlc-workflow/skills/verify-pr/style-conventions.md`, line 310 (RIGHT)
- **Original comment:**
  > The Check 6 description says 'Markdown: not applicable — skip Markdown files' but this is a documentation-heavy repository where skills are defined in Markdown. The check should still verify that new Markdown sections have introductory text explaining their purpose, even if traditional doc comments don't apply. Consider adding a Markdown-specific rule that checks whether new `###` headings have at least one paragraph of explanatory text before any sub-sections or code blocks.
- **Classification:** code change request

## Target PR
https://github.com/mrizzi/sdlc-plugins/pull/747
