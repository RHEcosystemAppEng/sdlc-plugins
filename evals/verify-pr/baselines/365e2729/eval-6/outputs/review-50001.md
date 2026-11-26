# Review comment 50001 — classification

- **Author:** reviewer-b (part of review 40002, state CHANGES_REQUESTED)
- **Location:** `plugins/sdlc-workflow/skills/verify-pr/style-conventions.md`, line 310 (RIGHT side), which is the Check 6b bullet "**Markdown:** not applicable — skip Markdown files"
- **Prior classification reply:** none found, so the comment is unclassified and processed in this run

## Comment
> The Check 6 description says 'Markdown: not applicable — skip Markdown files' but this is a documentation-heavy repository where skills are defined in Markdown. The check should still verify that new Markdown sections have introductory text explaining their purpose, even if traditional doc comments don't apply. Consider adding a Markdown-specific rule that checks whether new `###` headings have at least one paragraph of explanatory text before any sub-sections or code blocks.

## Classification: **code change request**

## Reasoning
- **Directive wording.** The main ask is phrased as a requirement: "The check **should still verify** that new Markdown sections have introductory text". The review was submitted as **CHANGES_REQUESTED**. "Consider adding…" only proposes how to do it (check `###` headings for an explanatory paragraph). It does not make the request optional.
- **Not a question or a nit.** It asks for new behavior in Check 6 (a Markdown rule), not for clarification or a formatting change.
- **Valid concern.** CONVENTIONS.md says the repository is Markdown-first: "Primary format: Markdown documentation", and "Skills are defined in Markdown (`SKILL.md` files)". As written, Check 6 would return N/A for almost every PR in this repository, including this one, so the check adds little value here.
- **Convention evidence** (recorded for completeness; no upgrade was needed because the comment is already a code change request):
  - CONVENTIONS.md does not document a rule that a section heading needs an introductory paragraph.
  - The codebase does show the pattern. The Style/Conventions sub-agent counted 12 of 12 `### Check N` headings across `style-conventions.md` (5/5), `correctness.md` (3/3), `intent-alignment.md` (3/3) and `security.md` (1/1) that start with an introductory paragraph before any `####` sub-section or code block. The PR's own new Check 6 follows it too.
  - So the rule the reviewer wants is established in practice but not written down. That feeds the root-cause convention-gap task.
- **Scope.** The fix is limited to this task's Check 6 in `style-conventions.md`, so it belongs as a sub-task of TC-9106.

## Outcome
- Sub-task 1 created: "Add Markdown section-introduction rule to Check 6 (Documentation Coverage)". See `subtask-1.md`. Labels `ai-generated-jira`, `review-feedback`; it Blocks TC-9106.
- Reply posted to the thread (written to file, not posted):
  > [sdlc-workflow/verify-pr] Classified as **code change request** — sub-task [<SUBTASK-1-KEY>](<subtask-1-url>) created to address this feedback.
