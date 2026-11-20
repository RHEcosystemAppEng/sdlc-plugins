# Review Comment 50001 — Classification

- **Author:** reviewer-b (parent review 40002, state `CHANGES_REQUESTED`)
- **File/line:** `plugins/sdlc-workflow/skills/verify-pr/style-conventions.md`, line 310 (RIGHT). This is the `**Markdown:** not applicable — skip Markdown files` line in Check 6b.
- **Prior classification reply:** none found, so the comment is unclassified and goes through Step 4c.

## Comment text
> The Check 6 description says 'Markdown: not applicable — skip Markdown files' but this is a documentation-heavy repository where skills are defined in Markdown. The check should still verify that new Markdown sections have introductory text explaining their purpose, even if traditional doc comments don't apply. Consider adding a Markdown-specific rule that checks whether new `###` headings have at least one paragraph of explanatory text before any sub-sections or code blocks.

## Classification: **Code change request**

## Reasoning
1. **The core statement is a requirement.** "The check **should still verify** that new Markdown sections have introductory text" asks for a change to the behavior of the code under review. It is not phrased as an optional alternative.
2. **The review blocks the PR.** The parent review 40002 has state `CHANGES_REQUESTED`, and its body says the reviewer has "a concern about the Markdown exclusion rule". The reviewer is gating the merge on this point.
3. **"Consider" describes how to fix it, not whether.** The second sentence ("Consider adding a Markdown-specific rule … `###` headings … at least one paragraph") suggests a way to implement the fix. The requirement itself is in the first sentence.
4. **It points to a real functional gap, not style.** CONVENTIONS.md says the repository's primary format is Markdown documentation and that skills are defined in Markdown `SKILL.md` files. With Markdown excluded, Check 6 returns N/A for almost every PR in this repository, so the check does nothing in exactly the place the reviewer cares about.
5. **It is not a question or a nit.** It asks for no clarification and concerns check logic, not formatting.

## Convention-upgrade check (Step 4b / Style/Conventions Check 1)
The comment is classified directly as a code change request, so no convention upgrade is needed. For completeness, I checked whether it would have qualified as a convention upgrade:
- CONVENTIONS.md was read from the repository root (`./CONVENTIONS.md`). It records Markdown as the primary format ("Primary format: Markdown documentation"; "Skills are defined in Markdown (`SKILL.md` files)"). It does **not** document a rule that new headings must open with introductory text.
- Codebase pattern: the existing checks in `style-conventions.md` follow this practice. For example, `### Check 5 — Eval Result Extraction` opens with an explanatory paragraph before `#### 5a`, and the new `### Check 6` does the same. So the practice is demonstrated but not documented.
- Either way, the outcome is a code change request and a sub-task.

## Outcome
- A sub-task is created: **subtask-1** (`subtask-1.md`), "Extend Check 6 Documentation Coverage with a Markdown section-introduction rule". Labels: `ai-generated-jira`, `review-feedback`. Link: Blocks TC-9106.
- Planned PR reply, not posted in eval mode:
  `[sdlc-workflow/verify-pr] Classified as **code change request** — sub-task [<SUBTASK-1-KEY>](<url>) created to address this feedback.`
- Root cause: convention gap. The project's CONVENTIONS.md never states that documentation-coverage rules apply to Markdown skill files, and the task's Implementation Notes listed only code-language doc-comment conventions. See the report's Root-Cause section.
