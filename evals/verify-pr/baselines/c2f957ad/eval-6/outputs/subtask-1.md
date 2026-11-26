# Sub-task 1

- **Issue Type:** Sub-task
- **Parent:** TC-9106
- **Summary:** Add Markdown section-introduction rule to Check 6 Documentation Coverage
- **Labels:** `["ai-generated-jira", "review-feedback"]`
- **Link:** Blocks, inward = this sub-task, outward = TC-9106

---

## Repository
sdlc-plugins

## Target Branch
main

## Description
Replace the blanket "Markdown: not applicable — skip Markdown files" exclusion in Check 6 (Documentation Coverage) of the verify-pr Style/Conventions sub-agent with a Markdown-specific rule. This repository is documentation-heavy and its skills are defined in Markdown (`SKILL.md` and sibling `.md` files). Because Check 6 currently skips Markdown, it returns N/A for most PRs here. The new rule checks that every new `###` heading added in the PR has at least one paragraph of explanatory text before any sub-heading or code block, so new Markdown sections explain their purpose the way doc comments explain code symbols.

## Files to Modify
- `plugins/sdlc-workflow/skills/verify-pr/style-conventions.md` — in Check 6, replace the Markdown exclusion bullet in 6b with a Markdown section-introduction rule; extend 6a so new `###` headings in `.md` files count as "new symbols"; update the 6c Evidence line to include undocumented Markdown headings
- `evals/verify-pr/evals.json` — add or update eval assertions to cover the new Markdown behaviour of Check 6

## Implementation Notes
- Keep the existing structure of Check 6 (6a Identify / 6b Check / 6c Verdict) introduced on the PR branch. Change only the Markdown handling.
- 6a: treat a `+`-prefixed `### ` heading line in a `*.md` file, with no matching `-` line, as a new documentable unit, using the same "new vs modified" rule 6a already applies to code symbols.
- 6b: replace `- **Markdown:** not applicable — skip Markdown files` with a rule like: "**Markdown:** a new `###` heading is documented when at least one non-empty paragraph line (not a heading, list-free prose, not a fenced code block or table) appears between the heading and the next heading (`####` or higher level) or code fence."
- 6c: verdict semantics stay as they are (PASS = all documented, WARN = any undocumented, N/A = no new symbols or headings). The Evidence line should list undocumented headings with file path, line number and heading text.
- Follow the style of the existing checks in the same file (for example Check 3 — Test Documentation, which lists per-language conventions as bullets).
- Fixture files under `evals/` (lines starting with the `SYNTHETIC TEST DATA` or `ADVERSARIAL TEST FIXTURE` comment headers) should not be flagged. Consider excluding `evals/**/files/*.md` from the Markdown rule.

## Reuse Candidates
- `plugins/sdlc-workflow/skills/verify-pr/style-conventions.md::Check 3 — Test Documentation` — existing per-language doc-comment rule list to mirror
- `plugins/sdlc-workflow/skills/verify-pr/style-conventions.md::Check 6 — Documentation Coverage` — the section added by PR #747, to be extended
- `evals/verify-pr/files/pr-diff-with-eval-results.md` — example PR diff fixture that changes Markdown skill files (adds a `### Check 6` heading with intro text)
- `evals/verify-pr/files/task-with-eval-results.md` — example task fixture for this check

## Acceptance Criteria
- [ ] Check 6 no longer skips Markdown files outright
- [ ] Check 6 identifies new `###` headings in Markdown files added by the PR
- [ ] A new `###` heading followed directly by a sub-heading or code block, with no explanatory paragraph in between, is recorded as undocumented and leads to a WARN verdict
- [ ] A new `###` heading with at least one explanatory paragraph before any sub-heading or code block is recorded as documented
- [ ] A Markdown-only PR whose new `###` headings all have introductory text gets PASS (not N/A)
- [ ] The 6c Evidence line includes file path, line number and heading text for undocumented headings

## Test Requirements
- [ ] Update eval assertions in `evals/verify-pr/evals.json` to cover the behaviour changes introduced by this task: a Markdown diff with an undocumented new `###` heading gives Documentation Coverage = WARN
- [ ] Add an eval case or assertion confirming that a Markdown diff whose new `###` headings all have introductory paragraphs gives Documentation Coverage = PASS

## Review Context
Review comment 50001 by `reviewer-b` on PR #747 (review 40002, state CHANGES_REQUESTED), file `plugins/sdlc-workflow/skills/verify-pr/style-conventions.md`, line 310 (RIGHT):

> The Check 6 description says 'Markdown: not applicable — skip Markdown files' but this is a documentation-heavy repository where skills are defined in Markdown. The check should still verify that new Markdown sections have introductory text explaining their purpose, even if traditional doc comments don't apply. Consider adding a Markdown-specific rule that checks whether new `###` headings have at least one paragraph of explanatory text before any sub-sections or code blocks.

Review body (review 40002): "The new Check 6 looks good overall, but I have a concern about the Markdown exclusion rule."

## Target PR
https://github.com/mrizzi/sdlc-plugins/pull/747
