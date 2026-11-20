# Sub-task 1

- **Issue Type:** Sub-task
- **Parent:** TC-9106
- **Summary:** Extend Check 6 Documentation Coverage with a Markdown section-introduction rule
- **Labels:** `ai-generated-jira`, `review-feedback`
- **Link:** Blocks TC-9106 (inward: this sub-task, outward: TC-9106)

---

## Repository
sdlc-plugins

## Target Branch
main

## Description
Check 6 (Documentation Coverage) in the verify-pr Style/Conventions sub-agent currently skips Markdown files ("Markdown: not applicable — skip Markdown files"). In sdlc-plugins, skills and their sub-agent instructions are defined in Markdown, so the check is N/A for nearly every PR in this repository. Replace the Markdown exclusion with a Markdown-specific rule: every new `###` heading added in the PR must be followed by at least one paragraph of explanatory text before any sub-heading (`####` or deeper) or fenced code block. Headings that break this rule count as undocumented symbols and feed into the existing PASS/WARN/N/A verdict.

## Files to Modify
- `plugins/sdlc-workflow/skills/verify-pr/style-conventions.md` — in Check 6: add new Markdown `###` headings to the symbols identified in 6a, replace the "Markdown: not applicable" bullet in 6b with the section-introduction rule, and make sure the 6c verdict and evidence wording cover Markdown sections (file path plus heading line number)

## Implementation Notes
- Follow the structure of the existing Check 6 sub-steps (6a Identify, 6b Check, 6c Verdict) in `plugins/sdlc-workflow/skills/verify-pr/style-conventions.md`. Add the Markdown rule as another bullet in the 6b language list. Do not create a separate check.
- Define a "new Markdown section" the same way 6a defines a new symbol: a `+`-prefixed `### ` heading line in the diff with no corresponding `-` line, which excludes renamed or reworded headings.
- Define "introductory text": at least one non-empty prose line, meaning not a heading, not a fence (```` ``` ````) and not a table row. It must appear between the `###` heading and the next heading of any level or fenced code block. List items count as prose only if the team agrees. Spell out the chosen rule explicitly in 6b.
- Existing examples of the desired pattern, to quote in the rule: `### Check 5 — Eval Result Extraction` opens with "Extract eval quality metrics from eval result reviews posted by CI…" before `#### 5a`, and the new `### Check 6 — Documentation Coverage` opens with "Verify that new public symbols introduced in the PR…" before `#### 6a`.
- Update the N/A wording in 6a and 6c so N/A means no new code symbols **and** no new Markdown `###` sections.
- Keep the Output Format row count (six rows) and the `Documentation Coverage` row unchanged. Only the one-line summary content may now mention Markdown sections.

## Reuse Candidates
- `plugins/sdlc-workflow/skills/verify-pr/style-conventions.md::Check 6 — Documentation Coverage` — the check this sub-task extends. Reuse the 6a "new symbol" definition and the 6c verdict wording.
- `plugins/sdlc-workflow/skills/verify-pr/style-conventions.md::Check 3 — Test Documentation` — an existing documentation-presence check whose flagging and evidence format can be mirrored

## Acceptance Criteria
- [ ] Check 6b no longer says Markdown files are skipped. It defines a Markdown rule: each new `###` heading must have at least one paragraph of explanatory text before any sub-heading or fenced code block
- [ ] Check 6a identifies new Markdown `###` headings (added lines with no matching removed line) as symbols to evaluate
- [ ] A new `###` heading directly followed by a `####` sub-heading or a code block is reported as undocumented, with file path and line number, and produces WARN
- [ ] A new `###` heading followed by an explanatory paragraph is treated as documented and does not cause WARN
- [ ] N/A applies only when the PR introduces neither new code symbols nor new Markdown `###` sections
- [ ] The Output Format still has exactly six rows, including `Documentation Coverage`

## Test Requirements
- [ ] Verify Check 6 flags a new `###` heading that has no introductory paragraph before its first sub-section or code block
- [ ] Verify Check 6 does not flag a new `###` heading that has an introductory paragraph
- [ ] Verify Check 6 does not flag modified or renamed existing `###` headings
- [ ] Add or update an eval case in `evals/verify-pr/evals.json` (for example, extend eval-6 fixture `evals/verify-pr/files/pr-diff-with-eval-results.md`) with assertions covering the Markdown section-introduction rule

## Review Context
- **Reviewer:** reviewer-b (review 40002, state CHANGES_REQUESTED; inline comment 50001)
- **PR file/line:** `plugins/sdlc-workflow/skills/verify-pr/style-conventions.md`, line 310 (RIGHT side). This is the `**Markdown:** not applicable — skip Markdown files` bullet in Check 6b.
- **Original comment:**
  > The Check 6 description says 'Markdown: not applicable — skip Markdown files' but this is a documentation-heavy repository where skills are defined in Markdown. The check should still verify that new Markdown sections have introductory text explaining their purpose, even if traditional doc comments don't apply. Consider adding a Markdown-specific rule that checks whether new `###` headings have at least one paragraph of explanatory text before any sub-sections or code blocks.

## Target PR
https://github.com/mrizzi/sdlc-plugins/pull/747
