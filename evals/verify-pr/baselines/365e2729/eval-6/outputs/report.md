## Verification Report for TC-9106 (commit unavailable)

PR: https://github.com/mrizzi/sdlc-plugins/pull/747 (as recorded in the TC-9106 Git Pull Request field). The upstream repository from the Repository Registry is RHEcosystemAppEng/sdlc-plugins, PR #747. Head SHA: not available in the eval fixtures, so this report is not tied to a specific commit.
Mode: interactive (offline eval). Every Jira and GitHub write below was written to files in `outputs/` and was not executed.

| Check | Result | Details |
|-------|--------|---------|
| Review Feedback | WARN | 1 inline comment and 1 review body classified. Comment 50001 is a code change request (Markdown exclusion in Check 6), and sub-task 1 was created for it. Review-body-40002 is the same concern, already covered by sub-task 1. Review 40001 is an eval-result review, so it is excluded from classification. |
| Root-Cause Investigation | DONE | 4 root-cause tasks: 1 convention gap (Markdown section intros not documented), 2 implement-task skill gaps (acceptance-criteria and end-to-end self-check; eval regression check before PR), 1 plan-feature gap (eval coverage propagation not applied) |
| Scope Containment | PASS | The PR changes exactly the 2 files the task lists: `style-conventions.md` and `SKILL.md`. Nothing extra, nothing missing. |
| Diff Size | PASS | About 45 changed lines (+44/-1) in 2 files, proportionate to the task |
| Commit Traceability | N/A | The fixtures contain no commit data, so this could not be checked |
| Sensitive Patterns | PASS | No matches in any of the 6 pattern categories across all added lines in both files |
| CI Status | PASS | All CI checks pass |
| Acceptance Criteria | FAIL | 5 of 7 criteria met. AC1 fails: no "public" symbol filter. AC7 fails: the mapping row sits in a fenced block and maps to a "Style Quality" row that does not exist. |
| Test Quality | WARN | Eval Quality WARN: 54/56 assertions pass (96.4%; the review footer says 91%), eval-1/2/4/5 at 100%, eval-3 at 11/13 (85%). eval-3 has 2 failing assertions, both **regressions** against baseline: (1) "Convention upgrade eligibility is evaluated for review comment 30002 (index suggestion)…": `review-30002.md` does no CONVENTIONS.md lookup or codebase pattern analysis; (2) "Review comment 30002 (index suggestion) results in a sub-task regardless of classification path…": no sub-task was created for 30002. Eval-failure sub-task 2 was created. Repetitive Test Detection N/A and Test Documentation N/A (no test files). |
| Test Change Classification | N/A | The PR adds, modifies and deletes no test files |
| Verification Commands | N/A | The task has none, and the PR does not touch run-evals infrastructure |

### Overall: FAIL

Two acceptance criteria are not met (AC1, AC7), and a reviewer code change request is still open. The informational Test Quality row also shows 2 eval-3 regressions. Five sub-tasks block TC-9106. A human reviewer decides whether to merge. This skill does not merge the PR or transition the issue.

---

## Classified Review Comments (Step 4)

Enumeration (Step 4a): 2 reviews and 1 inline comment thread.
- **Eval result reviews (Step 4a.1):** 40001, from `github-actions[bot]`. It contains `## Eval Results` and the `sdlc-workflow/run-evals` footer, so it is excluded from classification and passed to Style/Conventions Check 5.
- **Unclassified items:** 50001 (inline) and review-body-40002. No `[sdlc-workflow/verify-pr]` classification replies exist yet.
- **Already-classified items:** none.

| ID | Author | Location | Classification | Outcome |
|---|---|---|---|---|
| 50001 | reviewer-b | `style-conventions.md:310` | code change request | Sub-task 1. See `review-50001.md` |
| review-body-40002 | reviewer-b | review body (CHANGES_REQUESTED) | code change request (same concern as 50001) | Covered by sub-task 1, no duplicate. See `review-40002.md` |

Convention upgrade (Step 6b): no comments were classified as suggestion, so there were no upgrades. For 50001, CONVENTIONS.md does not document a section-introduction rule, but the codebase shows it in 12 of 12 `### Check N` headings across the verify-pr sub-agent files.

Replies (Step 6e, written to file, not posted):
- 50001 (thread reply): `[sdlc-workflow/verify-pr] Classified as **code change request** — sub-task [<SUBTASK-1-KEY>](<url>) created to address this feedback.`
- review-body-40002 (standalone comment): `[sdlc-workflow/verify-pr] Re: @reviewer-b review — Classified as **code change request** — the Markdown exclusion concern is detailed in inline comment 50001; sub-task [<SUBTASK-1-KEY>](<url>) created to address this feedback.`

## Domain Findings

### From Intent Alignment
- **Scope Containment, PASS.** File-by-file comparison:

  | File | In task | In PR | Status |
  |---|---|---|---|
  | `plugins/sdlc-workflow/skills/verify-pr/style-conventions.md` | Files to Modify | +43/-1 | in scope |
  | `plugins/sdlc-workflow/skills/verify-pr/SKILL.md` | Files to Modify | +1/-0 | in scope |

  There are no out-of-scope files, no task files missing from the PR, and no Files to Create.
- **Diff Size, PASS.** 45 changed lines in 2 files, against 2 expected files.
- **Commit Traceability, N/A.** No commit list was provided, so no claim is made either way.

### From Security
- **Sensitive Pattern Scan, PASS.** Every added `+` line was scanned: 37 in `style-conventions.md` (hunks `@@ -282,6 +282,48 @@` and `@@ -291,4 +333,5 @@`) and 1 in `SKILL.md` (`@@ -354,6 +354,7 @@`). The 6 categories were hardcoded passwords/secrets, API keys/tokens (AKIA, sk-, ghp_, xoxb-, …), private keys/certificates, env/config files, cloud credentials (AWS/GCP/Azure) and database credentials. There were 0 matches, all in Markdown prose and table rows. The doc-comment markers (`///`, `/** */`, `"""`) are not credentials.

### From Correctness
- **CI Status, PASS.** All checks pass.
- **Acceptance Criteria, FAIL (5/7).**

  | # | Criterion | Verdict | Detail |
  |---|---|---|---|
  | 1 | Scans the PR diff for new public symbol definitions | FAIL | 6a scans every new definition with no visibility filter, even though the intro says "public". See `criterion-1.md` |
  | 2 | Checks for a doc comment using each language's convention | PASS | Covers Rust, TS/Java, Python and Go. The Python wording differs slightly from the 6b lead-in. See `criterion-2.md` |
  | 3 | PASS when all are documented | PASS | 6c PASS bullet. See `criterion-3.md` |
  | 4 | WARN when any are undocumented | PASS | 6c WARN bullet plus evidence rule. See `criterion-4.md` |
  | 5 | N/A when there are no new symbols | PASS | 6a short-circuit plus 6c N/A bullet. See `criterion-5.md` |
  | 6 | Output Format has a sixth row | PASS | "six rows" plus a Documentation Coverage row. The diff context table and the Constraints line ("four checks") are inconsistent. See `criterion-6.md` |
  | 7 | Step 6a mapping includes Documentation Coverage | FAIL | The row is in a fenced block under "Add a new mapping row:", not in the live Step 6a table. Its target "Style Quality *(new)*" is not in Step 8 or the verdict source mapping, and no combination rule was added. See `criterion-7.md` |

- **Test Requirements:** none of the 3 is covered. The PR has no eval fixtures and no `evals/verify-pr/evals.json` changes.
- **Verification Commands, N/A.**
- **Actions:** 3 `create-sub-task` actions, which became sub-tasks 3, 4 and 5.

### From Style/Conventions
- **Convention Upgrade, N/A.** No suggestions were classified. For context on 50001, the section-introduction pattern appears in 12 of 12 headings but is not documented in CONVENTIONS.md.
- **Repetitive Test Detection, N/A.** **Test Documentation, N/A.** **Test Change Classification, N/A.** No test files. The isolation sub-agent was not needed.
- **Eval Quality, WARN.** Review 40001, run-evals v0.9.1:

  | Eval | Passed | Failed | Pass Rate |
  |---|---|---|---|
  | eval-1 | 12/12 | 0 | 100% |
  | eval-2 | 11/11 | 0 | 100% |
  | eval-3 | 11/13 | 2 | 85% |
  | eval-4 | 10/10 | 0 | 100% |
  | eval-5 | 10/10 | 0 | 100% |

  The overall pass rate is 54/56, or 96.4%. The review footer states 91%, which does not match its own table.

  Failing assertions, with baseline comparison against `evals/verify-pr/baselines/latest/`, where eval-3 is 15/15:
  1. **Convention upgrade eligibility** for comment 30002. Evidence: `review-30002.md` classifies 30002 as a suggestion but documents no CONVENTIONS.md lookup or codebase pattern analysis. This is a **regression**: the identical assertion passed at baseline.
  2. **Sub-task creation** for comment 30002 ("results in a sub-task regardless of classification path"). Evidence: no sub-task was created, because 30002 stayed a suggestion and no upgrade was attempted. This is a **regression** under the conservative default, since there is no matching baseline assertion. The baseline held the opposite assertion ("does NOT result in a sub-task"), which passed. That suggests the eval-3 definition changed, and sub-task 2 asks for this conflict to be reconciled.

## Sub-tasks Created (Step 6d)

All have parent TC-9106, link "Blocks" (sub-task → TC-9106), and Target PR #747. Full descriptions are in `subtask-N.md`.

| # | Summary | Labels | Source |
|---|---|---|---|
| 1 | Add Markdown section-introduction rule to Check 6 (Documentation Coverage) | ai-generated-jira, review-feedback | Review comment 50001 (and review-body-40002) |
| 2 | Fix eval-3 assertion failures: convention upgrade eligibility, sub-task creation | ai-generated-jira, eval-failure | Eval Quality, 2 regressions |
| 3 | Restrict Check 6a to new public/exported symbols | ai-generated-jira, review-feedback | Correctness, AC1 |
| 4 | Wire Documentation Coverage into the live Step 6a mapping and the Step 8 report | ai-generated-jira, review-feedback | Correctness, AC7 |
| 5 | Add verify-pr eval coverage for Check 6 (Documentation Coverage) | ai-generated-jira, review-feedback | Correctness, Test Requirements |

Idempotency: there were no prior verify-pr classification replies and no existing review-feedback or eval-failure sub-tasks on TC-9106, so nothing was skipped.

## Root-Cause Investigation (Step 7)

The investigation took in all 5 sub-tasks: review feedback, Correctness acceptance-criteria and test gaps, and the eval failure, along with the aggregated domain findings above. Parent Feature TC-9100 could not be fetched in this offline eval, so the define-feature phase was assessed from the task description only.

| Defect (sub-task) | Universality | Method / Fact / Convention | Classification | Phase |
|---|---|---|---|---|
| Markdown files skipped in a Markdown-first repo (1) | Repo-specific: this repo writes skills in Markdown and uses sections with introductions | Not in CONVENTIONS.md | Convention gap | convention |
| eval-3 regressions for comment 30002 (2) | Universal | Method: "run the skill's evals and compare to baseline before opening a PR that modifies a skill" | Skill gap | implement-task |
| "public" qualifier not implemented (3) | Universal | Method: "check every qualifier in each acceptance criterion against the final text" | Skill gap | implement-task. The AC was correct, but the implementation followed narrower Implementation Notes. |
| Mapping row in the wrong place and orphaned report row (4) | Universal | Method: "trace each new output to its consumer (mapping → report table)" | Skill gap | implement-task |
| No eval coverage for Check 6 (5) | Universal | Method: "apply eval coverage propagation when a task modifies a SKILL.md with existing evals" | Skill gap | plan-feature. TC-9106 modifies `verify-pr/SKILL.md` and `evals/verify-pr/evals.json` exists, but the task does not list evals.json or eval Reuse Candidates. |

Root-cause tasks (labels `ai-generated-jira, root-cause`, link "Relates" to TC-9106, each with an analysis comment citing "Root-cause analysis from TC-9106 verification" plus the comment footnote):
1. **Root-cause: Document Markdown section-introduction convention in CONVENTIONS.md.** Add a Code Style rule: every new `##`/`###` section in skill and doc Markdown opens with at least one explanatory paragraph before sub-sections, code blocks, tables or lists. Scope it to `.md` files and cite the `### Check N` pattern in `plugins/sdlc-workflow/skills/verify-pr/*.md` as the example.
2. **Root-cause: implement-task self-check of acceptance-criteria qualifiers and end-to-end output wiring.** Before committing, implement-task re-reads each acceptance criterion against the final file contents and checks every qualifier (e.g. "public", "combined"). For any new output, verdict or field, it confirms that each consumer (mapping tables, report templates, combination rules) is updated, and that edits land in the live section rather than an example or fenced block.
3. **Root-cause: implement-task runs skill evals and checks for baseline regressions.** When a task modifies `plugins/*/skills/<skill>/` and `evals/<skill>/` exists, implement-task runs `/sdlc-workflow:run-evals` for that skill and compares the result with `evals/<skill>/baselines/latest/summary.md` before opening or updating the PR. Any regression is fixed or reported.
4. **Root-cause: plan-feature must apply eval coverage propagation.** Make sure plan-feature applies `plugins/sdlc-workflow/shared/eval-coverage-propagation.md` to every task whose Files to Modify includes a `SKILL.md` with existing evals. That means adding `evals/<skill>/evals.json` to Files to Modify, the eval Test Requirement, and fixture Reuse Candidates, with a self-check that blocks task creation without them.

Step 7c idempotency: no existing root-cause tasks are linked to TC-9106.

## Jira Comment

This report is also added as a comment on TC-9106 (written to file, not posted). It ends with the verify-pr comment footnote (plugin v0.14.0).

---
*This comment was AI-generated by [sdlc-workflow/verify-pr](https://github.com/RHEcosystemAppEng/sdlc-plugins) v0.14.0.*
