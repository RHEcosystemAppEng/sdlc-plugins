# Review Comment 50001: Classification

- **Author:** reviewer-b (human reviewer, not a bot)
- **Source:** inline review comment, part of review 40002 (state: `CHANGES_REQUESTED`)
- **Location:** `plugins/sdlc-workflow/skills/verify-pr/style-conventions.md`, line 310 (RIGHT side). This is the `- **Markdown:** not applicable — skip Markdown files` bullet in Check 6b.
- **Thread:** top-level (`in_reply_to_id: null`), no replies. There is no existing `[sdlc-workflow/verify-pr] Classified as` reply, so the comment is **unclassified** and goes through Step 4c.
- **Not an eval result:** the eval-review detection in Step 4a.1 needs all three conditions: author `github-actions[bot]`, a `## Eval Results` marker, and a `sdlc-workflow/run-evals` footer. This comment meets none of them, so it is classified only on the reviewer's own feedback.

## Comment text
> The Check 6 description says 'Markdown: not applicable — skip Markdown files' but this is a documentation-heavy repository where skills are defined in Markdown. The check should still verify that new Markdown sections have introductory text explaining their purpose, even if traditional doc comments don't apply. Consider adding a Markdown-specific rule that checks whether new `###` headings have at least one paragraph of explanatory text before any sub-sections or code blocks.

## Classification: **code change request**

### Reasoning
1. **Directive language about required behavior.** "The check **should still verify** that new Markdown sections have introductory text" states what Check 6 must do. It is not offered as an optional alternative. The reviewer points to a functional gap: in a repository where most changes are Markdown, the blanket Markdown skip means Check 6 returns N/A for almost every PR, this PR included.
2. **The review state confirms it is blocking.** The parent review 40002 was submitted as `CHANGES_REQUESTED`, and its body names this exact concern ("I have a concern about the Markdown exclusion rule"). The reviewer expects a change before approval.
3. **"Consider adding…" describes how, not whether.** The second sentence proposes a concrete way to implement the requested behavior: new `###` headings need at least one paragraph before sub-sections or code blocks. It softens the wording of the proposed rule, but the requirement itself ("should still verify") is directive.
4. **Not a question or nit.** It asks for no clarification, and it concerns check behavior, not formatting.

### Convention context (Step 4b)
CONVENTIONS.md (repository root `./`) describes the repo as "Documentation-first" with "Skills are defined in Markdown (`SKILL.md` files)". That supports the reviewer's premise. It does **not** document a rule that new Markdown sections need introductory text. No convention upgrade was needed, because the comment was classified as a code change request from its own wording. The missing convention is recorded as a convention gap in the root-cause investigation.

### Downstream effect
- A review-feedback sub-task is created (see `subtask-1.md`), labels `["ai-generated-jira", "review-feedback"]`, with a **Blocks** link to TC-9106.
- Planned threaded reply (not posted; eval mode):
  `gh api repos/mrizzi/sdlc-plugins/pulls/747/comments/50001/replies -f body="[sdlc-workflow/verify-pr] Classified as **code change request** — sub-task [<SUBTASK-1-KEY>](<subtask-1-url>) created to address this feedback."`
