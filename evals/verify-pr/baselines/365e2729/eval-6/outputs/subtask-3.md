# Sub-task 3 — Restrict Check 6a to new public/exported symbols

- **Issue Type:** Sub-task
- **Parent:** TC-9106
- **Labels:** ai-generated-jira, review-feedback
- **Link:** Blocks TC-9106

## Repository
sdlc-plugins

## Target Branch
main

## Description
TC-9106 Acceptance Criterion 1 requires Check 6 to scan for new **public** symbol definitions. Check 6a as implemented counts every new function, method, struct, class, interface, enum and type, with no visibility filter. Private helpers and non-exported symbols would therefore produce false WARNs. Add per-language visibility rules to 6a so only public or exported symbols are checked.

## Files to Modify
- `plugins/sdlc-workflow/skills/verify-pr/style-conventions.md` — Check 6a: add a visibility filter with per-language rules
- `evals/verify-pr/evals.json` — add or update eval assertions to cover the new behavior

## Implementation Notes
- Put the visibility rules in 6a, in the same bullet-list style that 6b uses for per-language doc-comment conventions:
  - Rust: `pub` (including `pub(crate)`, which counts as public within the crate)
  - Java: `public`/`protected`
  - TypeScript: `export`
  - Go: identifier starts with an uppercase letter
  - Python: name does not start with `_`
- State explicitly that non-public symbols are excluded, so a PR adding only private symbols yields N/A.
- Keep the 6a definition of "new" unchanged: a `+` line with no matching `-` line.

## Reuse Candidates
- `plugins/sdlc-workflow/skills/verify-pr/style-conventions.md::Check 6 — 6b` — the existing per-language rule list to mirror

## Acceptance Criteria
- [ ] Check 6a only counts new symbols that are public/exported under the language's visibility rules
- [ ] A PR that adds only private/non-exported symbols yields N/A for Documentation Coverage
- [ ] Visibility rules are listed for every language covered in 6b (Rust, TypeScript/Java, Python, Go)

## Test Requirements
- [ ] Verify an undocumented private symbol is not flagged
- [ ] Verify an undocumented public symbol is flagged
- [ ] Update eval assertions in `evals/verify-pr/evals.json` to cover the behavior changes introduced by this task. Add new eval cases if existing cases do not exercise the modified behavior, or update assertions on existing cases if their expected output changes.

## Review Context
Source: verify-pr Correctness sub-agent, Acceptance Criteria check. AC1 "Check 6 scans the PR diff for new public symbol definitions" was judged FAIL. The PR diff for `style-conventions.md` (6a, hunk `@@ -282,6 +282,48 @@`) scans for "newly added function, method, struct, class, interface, enum, and type definitions" and never puts the "public" qualifier into practice.

## Target PR
https://github.com/RHEcosystemAppEng/sdlc-plugins/pull/747

Add commits to the existing PR #747 head branch; do not open a new PR. The Repository Registry entry `sdlc-plugins` (path `./`) resolves to origin `RHEcosystemAppEng/sdlc-plugins`. The TC-9106 Git Pull Request field records the same PR number as `https://github.com/mrizzi/sdlc-plugins/pull/747`.

## Dependencies
- Depends on: TC-9106 — Add documentation coverage check to style-conventions sub-agent (this sub-task amends its PR)
