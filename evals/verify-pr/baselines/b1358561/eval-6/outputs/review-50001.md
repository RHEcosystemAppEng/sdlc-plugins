# Review comment 50001 — reviewer-b (inline, style-conventions.md line 310)

**Classification: code change request** (sub-task created: subtask-1)

## Comment
> The Check 6 description says 'Markdown: not applicable — skip Markdown files' but this is a documentation-heavy repository where skills are defined in Markdown. The check should still verify that new Markdown sections have introductory text explaining their purpose, even if traditional doc comments don't apply. Consider adding a Markdown-specific rule that checks whether new `###` headings have at least one paragraph of explanatory text before any sub-sections or code blocks.

## Enumeration / idempotency
- Top-level inline thread (`in_reply_to_id: null`) with no replies. No `[sdlc-workflow/verify-pr] Classified as` reply exists, so the comment is **unclassified** and is classified now.

## Reasoning
- **Directive language:** "The check **should still verify** that new Markdown sections have introductory text…" is a direct request to change Check 6's behavior. It is not a request for clarification.
- **Review state:** the parent review (40002) was submitted as `CHANGES_REQUESTED`. Its body says the reviewer has "a concern about the Markdown exclusion rule", which shows the reviewer considers this blocking.
- **Softer second sentence:** "Consider adding a Markdown-specific rule…" proposes *how* to fix it (check that each new `###` heading has a paragraph before sub-sections or code blocks). It does not make the request optional. The *what* (do not silently skip Markdown in a Markdown-first repo) is stated as "should".
- **Not a nit or question:** the comment changes the check's coverage, not formatting, and it asks no question.
- **Context check:** CONVENTIONS.md says "Primary format: Markdown documentation" and "Skills are defined in Markdown (`SKILL.md` files)". In this repository, the blanket `Markdown: not applicable — skip Markdown files` rule means Check 6 returns N/A for almost every PR. That supports the reviewer's concern.

## Convention-upgrade note
The comment is classified directly as a code change request, so it does not go through the Check 1 suggestion-upgrade path. For completeness: if it had been read as a suggestion, CONVENTIONS.md does not document an "introductory paragraph under every `###` heading" rule. An upgrade would then depend on a counted codebase pattern rather than a documented convention.

## Scope note
The request goes beyond the original task text, which lists Rust/Java/TS/Python/Go conventions. It is still within the area the PR touches (Check 6 in style-conventions.md), so it is tracked as a review-feedback sub-task on the same PR.

## Reply that would be posted
`[sdlc-workflow/verify-pr] Classified as **code change request** — sub-task [{{subtask-1.key}}]({{subtask-1.url}}) created to address this feedback.`
