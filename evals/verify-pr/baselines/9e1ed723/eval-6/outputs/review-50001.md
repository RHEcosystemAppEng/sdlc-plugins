# Review comment 50001 (reviewer-b, inline)

- **File/line:** `plugins/sdlc-workflow/skills/verify-pr/style-conventions.md`, line 310 (RIGHT side). This is the `**Markdown:** not applicable — skip Markdown files` bullet in Check 6b.
- **Review:** part of review 40002 (state CHANGES_REQUESTED)
- **Prior classification reply:** none found (no `[sdlc-workflow/verify-pr] Classified as` reply in the thread). Listed as **unclassified** and classified on this run.

## Comment text

> The Check 6 description says 'Markdown: not applicable — skip Markdown files' but this is a documentation-heavy repository where skills are defined in Markdown. The check should still verify that new Markdown sections have introductory text explaining their purpose, even if traditional doc comments don't apply. Consider adding a Markdown-specific rule that checks whether new `###` headings have at least one paragraph of explanatory text before any sub-sections or code blocks.

## Classification: **Suggestion**

### Reasoning (reviewer language, Step 4c)

- The concrete request is worded as "**Consider adding** a Markdown-specific rule…". That proposes an alternative design and does not mandate it.
- The middle sentence says "should still verify", but it describes the reviewer's preferred design for the check. It does not point to a defect in what the task asked for.
- The proposal is a **scope extension**. TC-9106 defines Check 6 as covering new public *symbols* (function, method, struct, class), using language doc-comment patterns (`///`, `/** */`, `"""`, `//`). No acceptance criterion or Implementation Note mentions Markdown or headings. Markdown has no symbol definitions, so skipping it breaks no criterion (see criterion-2.md).
- The CHANGES_REQUESTED state is a reviewer action and is considered, but the comment's own wording is what decides the classification.

### Convention upgrade eligibility (Step 6b, Style/Conventions Check 1)

I checked whether a documented or demonstrated project convention backs the suggestion, which would upgrade it to a code change request.

1. **Documented convention (CONVENTIONS.md): no match.**
   - "Code Style" only says GitHub-flavored Markdown, no line-length limit, and manual review for consistency. Nothing about heading structure or introductory paragraphs.
   - "Naming Conventions" and "File Organization" cover file and directory naming and placement only.
   - "Testing Conventions → Fixture documentation" requires header comments in *eval/test fixture* files. That is a different scope.
   - "Shared Modules and Reuse → Skill patterns" asks new skills to follow existing skill structure (steps, guardrails, rules sections). It says nothing about prose under each heading.
   - Grepping CONVENTIONS.md, `docs/conventions-spec.md` and `docs/constraints.md` for "introduc", "explanatory" and "heading" found no relevant rule.
2. **Demonstrated convention (codebase pattern): not consistent enough to count.**
   - The Style/Conventions sub-agent counted the `###` headings outside code fences in the 22 Markdown files under `plugins/sdlc-workflow/skills/`. There are 239. 211 (88%) are followed directly by prose. 28 (12%) are not: 12 go to a list, 10 to a bold label, 5 to a code block, 1 to a table. Examples are `skills/verify-pr/SKILL.md:1142` and `skills/triage-security/remediation-templates.md:147`.
   - Intro prose is a common writing habit here, but it is not an enforced convention.
   - Even if it were, it is a convention about how documents are *written*. It does not establish that a verification check must *enforce* it. None of the existing verify-pr checks treat Markdown headings as needing documentation.
3. The PR's own new heading (`### Check 6 — Documentation Coverage`) already has an introductory paragraph, so the PR content itself does not violate the proposed rule.

**Result: not upgraded.** It stays a suggestion.

## Outcome

- **Sub-task created:** no
- **Reply that would be posted** (interactive mode, `gh api repos/mrizzi/sdlc-plugins/pulls/747/comments/50001/replies`):

> [sdlc-workflow/verify-pr] Classified as **suggestion** — the comment proposes an optional extension ("Consider adding a Markdown-specific rule") beyond TC-9106's scope, which defines Check 6 for code symbols using language doc-comment conventions only. No convention backs an upgrade: CONVENTIONS.md has no heading/intro-paragraph rule, and the codebase pattern (211 of 239 `###` headings in skill files followed by prose, 28 exceptions) is a writing habit, not an enforced convention. A follow-up task could be filed if the team wants Markdown section-intro enforcement. No sub-task created.
