# Review Comment 50001 — Classification

- **Author:** reviewer-b
- **Source:** inline comment thread (top-level, `in_reply_to_id: null`), part of review 40002 (state `CHANGES_REQUESTED`)
- **Location:** `plugins/sdlc-workflow/skills/verify-pr/style-conventions.md`, line 310 (RIGHT side), the `- **Markdown:** not applicable — skip Markdown files` line in Check 6b
- **Prior classification reply:** none (no `[sdlc-workflow/verify-pr] Classified as` reply in the thread), so this item is **unclassified** and was processed in this run

## Comment text

> The Check 6 description says 'Markdown: not applicable — skip Markdown files' but this is a documentation-heavy repository where skills are defined in Markdown. The check should still verify that new Markdown sections have introductory text explaining their purpose, even if traditional doc comments don't apply. Consider adding a Markdown-specific rule that checks whether new `###` headings have at least one paragraph of explanatory text before any sub-sections or code blocks.

## Classification: **code change request**

### Reasoning (Step 4c, reviewer language)

- The main sentence is directive: "The check **should still verify** that new Markdown sections have introductory text explaining their purpose". It says what the check is required to do, not an optional idea.
- The reviewer names a specific defect in the PR's code: the line "Markdown: not applicable — skip Markdown files". They explain why it is wrong for this repository: "skills are defined in Markdown". With the rule as written, Check 6 returns N/A on almost every PR in this repo, including this one, because it changes only Markdown files.
- "Consider adding a Markdown-specific rule that checks whether new `###` headings have at least one paragraph..." is softer, but it describes *how* to fix the defect, not *whether* to fix it.
- The parent review was submitted with state **`CHANGES_REQUESTED`**, and its body says "I have a concern about the Markdown exclusion rule". The reviewer is blocking the PR on this point, which confirms the comment is a required change, not an optional suggestion.

### Convention cross-check (Step 4b / Style-Conventions Check 1)

This was checked as well, in case the comment were read as a plain suggestion:

- **CONVENTIONS.md** says "**Primary format**: Markdown documentation" and "Skills are defined in Markdown (`SKILL.md` files)". That supports the reviewer's point that Markdown is the main "source code" here, and that skipping it makes a documentation-coverage check meaningless for this repository. CONVENTIONS.md does **not** state a rule that new `###` headings need an introductory paragraph, so no documented convention matches the specific rule proposed.
- **Codebase pattern (demonstrated in the diff):** the PR's own new `###` heading, `### Check 6 — Documentation Coverage`, is followed by an explanatory paragraph before its sub-sections. So are Checks 1–5 in the base file, each `### Check N` opening with an explanatory paragraph. That is a consistent, demonstrated pattern across at least 6 `###` check sections in `style-conventions.md`.
- Even if the comment were classified as a suggestion, this demonstrated pattern would justify upgrading it under Check 1d ("demonstrated by consistent codebase usage"). Either way, the final classification is **code change request**.

### Scope assessment (Step 6c)

- **Files:** `plugins/sdlc-workflow/skills/verify-pr/style-conventions.md`, which replaces the Markdown exclusion in Check 6b with a Markdown-specific rule. It may also touch the Check 6a symbol-identification text so that new `###` headings in Markdown files count as "new symbols".
- **Scoped to the current task:** yes. It changes the Check 6 behavior this PR introduces, and the fix stays inside the same file and check.

## Outcome

- **Sub-task created:** yes, see `subtask-1.md` (labels `ai-generated-jira`, `review-feedback`; "Blocks" link to TC-9106)
- **PR reply that would be posted:**
  `[sdlc-workflow/verify-pr] Classified as **code change request** — sub-task [<SUB-TASK-KEY>](<sub-task-webUrl>) created to address this feedback.`
