# Sub-task 1 (review feedback)

- **Issue Type:** Sub-task
- **Parent:** TC-9106
- **Summary:** Add Markdown section-introduction rule to Check 6 (Documentation Coverage) instead of skipping Markdown files
- **Labels:** `["ai-generated-jira", "review-feedback"]`
- **Link:** Blocks, sub-task (inward) to TC-9106 (outward)

---

## Repository
sdlc-plugins

## Target Branch
main

## Description
Check 6 (Documentation Coverage) in the verify-pr Style/Conventions sub-agent currently says "Markdown: not applicable — skip Markdown files". sdlc-plugins is a Markdown-first repository: skills, sub-agent instructions, and templates are all Markdown. With this rule, Check 6 returns N/A for nearly every PR in the repository. Replace the blanket exclusion with a Markdown-specific documentation rule. Each newly added `###` heading in a Markdown file must have at least one paragraph of explanatory text directly under it, before any sub-heading, list, table, or fenced code block. Report it the same way as the other languages' undocumented symbols.

## Files to Modify
- `plugins/sdlc-workflow/skills/verify-pr/style-conventions.md` — in Check 6: extend 6a to treat newly added `###` headings in `.md` files as new documentable items; replace the "Markdown: not applicable" bullet in 6b with the introductory-paragraph rule; make sure 6c evidence lists undocumented headings with file path and line number

## Implementation Notes
- Follow the structure of Check 6 sub-steps 6a/6b/6c and the existing Checks 1–5 in `plugins/sdlc-workflow/skills/verify-pr/style-conventions.md`. Keep the "skip to the Verdict and record N/A" early-exit wording used by Check 2a, Check 5a, and Check 6a.
- A Markdown heading is "new" under the same rule 6a uses for code symbols: the heading line appears with a `+` prefix and has no matching `-` line (not a rename or edit of an existing heading).
- "Documented" means the first non-blank content after the heading line is a prose paragraph. It is not a deeper heading (`####`), a fenced code block (```` ``` ````), a table row (`|`), or a list item.
- Existing sections in `style-conventions.md` already follow this pattern. For example, `### Check 5 — Eval Result Extraction` opens with a paragraph before `#### 5a`, and the new `### Check 6 — Documentation Coverage` opens with "Verify that new public symbols…". Use these as the reference example in the rule text.
- Keep the PASS / WARN / N/A semantics unchanged. Undocumented headings count toward WARN the same way undocumented code symbols do.
- Do not change the Output Format row count (still six rows).

## Reuse Candidates
- `plugins/sdlc-workflow/skills/verify-pr/style-conventions.md::Check 6 — Documentation Coverage` — the section being extended; reuse its 6a "new symbol" definition
- `plugins/sdlc-workflow/skills/verify-pr/style-conventions.md::Check 3 — Test Documentation` — existing documentation-presence check whose evidence format can be mirrored
- `evals/verify-pr/files/pr-diff-with-eval-results.md` — fixture with a Markdown-only diff that adds `###`/`####` headings; useful for exercising the new rule

## Acceptance Criteria
- [ ] Check 6 no longer skips Markdown files unconditionally
- [ ] Check 6 identifies newly added `###` headings in Markdown files in the PR diff
- [ ] A new `###` heading with no explanatory paragraph before its first sub-heading, list, table, or code block is reported as undocumented, with file path and line number
- [ ] A new `###` heading with an introductory paragraph is not flagged
- [ ] Check 6 verdict semantics (PASS/WARN/N/A) are unchanged and include Markdown headings

## Test Requirements
- [ ] Verify Check 6 flags a new `###` heading that is immediately followed by a `####` sub-heading or code block
- [ ] Verify Check 6 does not flag a new `###` heading followed by a prose paragraph
- [ ] Verify a Markdown-only PR with properly introduced new headings yields PASS, not N/A
- [ ] Add or update an eval case in `evals/verify-pr/evals.json` covering a Markdown diff with documented and undocumented headings

## Review Context
- **Reviewer:** reviewer-b (review 40002, state CHANGES_REQUESTED; inline comment 50001)
- **File/line:** `plugins/sdlc-workflow/skills/verify-pr/style-conventions.md`, line 310 (RIGHT side)
- **Original comment:**
  > The Check 6 description says 'Markdown: not applicable — skip Markdown files' but this is a documentation-heavy repository where skills are defined in Markdown. The check should still verify that new Markdown sections have introductory text explaining their purpose, even if traditional doc comments don't apply. Consider adding a Markdown-specific rule that checks whether new `###` headings have at least one paragraph of explanatory text before any sub-sections or code blocks.

## Target PR
https://github.com/mrizzi/sdlc-plugins/pull/747
