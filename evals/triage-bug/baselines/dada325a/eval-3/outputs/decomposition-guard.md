# Decomposition Guard — ACME-502 (Step 6)

Prompt shown to the user before any Task is created:

---

> This bug appears to involve multiple independent issues:
>
> 1. **Malformed convention references in Implementation Notes**: the convention reference
>    formatter lowercases and kebab-cases CONVENTIONS.md headings (`§migration-patterns`)
>    when it should keep the literal heading text (`§Migration Patterns`) that
>    plan-feature's `Per CONVENTIONS.md §<Section Name>` format requires.
>    (in `plugins/sdlc-workflow/skills/shared/convention-utils.md` — convention formatter)
> 2. **Tasks created with the wrong issue type**: task creation passes the configured
>    Feature issue type ID (10142) to `jira.create_issue`. It should pass the Task type ID
>    from the Step 2.5 type-to-role mapping (10050 in custom issue type schemes).
>    (in `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` — Step 6a "Create the tasks")
>
> The two problems sit in different modules, on separate code paths (description rendering
> vs. Jira issue creation). They don't share data, and each can be fixed, tested, and
> shipped on its own. The reporter's Suggested Fix also calls them "two separate bugs".
>
> Options:
> 1. **Proceed** — create a single Task covering all fixes
> 2. **Split** — I recommend creating separate Bugs for each independent issue,
>    then triaging each one individually
>
> Choose (1/2):

---

## Recommendation

**Option 2 (Split).** Each issue has its own reproducer test (a convention-reference string
assertion vs. an issue type ID assertion), touches different files, and has different
consumers. The formatter is shared across skills, while the issue type fix only concerns
plan-feature. Bundling them would give one Task with two unrelated reproducers and a mixed
PR scope, which goes against the "Keep the generated Task scoped to a single fix" rule.

## Behavior per choice

- **1 — Proceed**: create one Task (labeled `ai-generated-jira`, Target Branch `main`). It
  gets two reproducer tests as the first acceptance criteria, then both fixes, then a
  no-regression check. Link it to ACME-502 with "Blocks" (Task = inward/blocker,
  ACME-502 = outward/blocked), then post the description digest comment.
- **2 — Split**: stop. Don't create any Task. Suggest that the user create two Bug issues,
  for example:
  - "plan-feature: convention references rendered in kebab-case instead of the literal
    heading" (component sdlc-workflow; affected module `shared/convention-utils.md`)
  - "plan-feature: tasks created with Feature issue type instead of Task in custom issue type
    schemes" (component sdlc-workflow; affected module `plan-feature/SKILL.md` Step 6a)

  Each new Bug should include the required `### **Environment / Version**` section, which is
  missing from ACME-502. Then run `/triage-bug <new-bug-key>` on each one. ACME-502 can be
  linked to (or closed in favor of) the two new Bugs.
