# Review Comment 50001: Classification

- **Comment ID:** 50001
- **Author:** reviewer-b
- **Parent review:** 40002 (state: `CHANGES_REQUESTED`)
- **File/line:** `plugins/sdlc-workflow/skills/verify-pr/style-conventions.md`, line 310 (RIGHT side, the `- **Markdown:** not applicable — skip Markdown files` rule in Check 6b)
- **Prior classification reply:** none found, so the comment is unclassified and goes through classification

## Comment text

> The Check 6 description says 'Markdown: not applicable — skip Markdown files' but this is a documentation-heavy repository where skills are defined in Markdown. The check should still verify that new Markdown sections have introductory text explaining their purpose, even if traditional doc comments don't apply. Consider adding a Markdown-specific rule that checks whether new `###` headings have at least one paragraph of explanatory text before any sub-sections or code blocks.

## Classification: **Code change request**

## Reasoning

1. **Directive language.** "The check **should still verify** that new Markdown sections have introductory text" states required behavior. It names a defect in the current wording (a blanket Markdown exclusion) and the behavior that should replace it.
2. **Concrete fix.** The comment gives an implementable rule: new `###` headings must have at least one paragraph of explanatory text before any sub-sections or code blocks. A suggestion would only float an alternative.
3. **Review state.** The parent review 40002 was submitted as `CHANGES_REQUESTED`, and its body ("I have a concern about the Markdown exclusion rule") points to this comment as the blocking concern.
4. **"Consider adding…"** is softer, but it only describes *how* to meet the requirement already stated with "should still verify". It does not make the requirement optional.
5. **Grounded in the repository.** CONVENTIONS.md says the repository is "Documentation-first", that "Skills are defined in Markdown (`SKILL.md` files)", and that the "Primary format" is "Markdown documentation". The PR under review changes only Markdown files, so Check 6 as written would always return N/A on PRs to this repository. That undercuts the check's purpose where it matters most.

It is not a nit (it changes behavior, not style) and not a question (it asks for nothing to be clarified).

## Convention upgrade check

Not applicable. The comment is classified directly as a code change request, so the suggestion-to-code-change-request upgrade in Style/Conventions Check 1 does not run. For the record, CONVENTIONS.md has no explicit rule that new Markdown headings need introductory paragraphs. The classification rests on the reviewer's language, not on an upgrade.

## Scope

The fix belongs to the current task: it changes the Check 6 text this PR adds (`style-conventions.md`, sub-step 6b). It is not a broader concern.

## Outcome

- Sub-task created: see `subtask-1.md`, labels `["ai-generated-jira", "review-feedback"]`, linked with **Blocks** to TC-9106.
- Reply that would be posted to the thread (`gh api repos/mrizzi/sdlc-plugins/pulls/747/comments/50001/replies`):

> [sdlc-workflow/verify-pr] Classified as **code change request** — sub-task [TC-XXXX](<sub-task-webUrl>) created to address this feedback.
