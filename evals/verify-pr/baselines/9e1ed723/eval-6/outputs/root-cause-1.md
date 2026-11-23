# Root-cause task 1

- **Summary:** Root-cause: implement-task must check existing eval coverage and enumeration consistency when editing any skill prompt file
- **Labels:** `ai-generated-jira`, `root-cause`
- **Link:** Relates → TC-9106
- **Classification:** skill gap (universal, method-based), implement-task phase
- **Idempotency (Step 7c):** no existing root-cause task linked to TC-9106 carries "Root-cause analysis from TC-9106" for this phase and defect, so create it

---

## Repository
sdlc-plugins

## Target Branch
main

## Description
Extend implement-task's Step 9 self-verification so that edits to any file in a skill directory are checked for two things. That includes SKILL.md and supporting prompt files such as sub-agent definitions. The checks are: (1) regressions in behaviour already covered by that skill's eval assertions and baseline, and (2) stale counts, lists and cross-references to the set of checks, rows or steps the edit changed. This stops an edit to one part of a skill prompt from quietly breaking eval-covered behaviour elsewhere in it.

## Files to Modify
- `plugins/sdlc-workflow/skills/implement-task/SKILL.md` — broaden the "Eval coverage currency" trigger in Step 9 and add regression and enumeration-consistency checks
- `evals/implement-task/evals.json` — add or update eval assertions to cover the new behavior

## Implementation Notes
- Change the "### Eval coverage currency" subsection in Step 9 of `plugins/sdlc-workflow/skills/implement-task/SKILL.md`. It currently triggers only on `skills/<skill-name>/SKILL.md`; make it trigger on any modified file under `plugins/<plugin>/skills/<skill-name>/`.
- Add a regression-preservation step:
  - List the existing assertions in `evals/<skill-name>/evals.json` whose behaviour is defined in the modified files.
  - Confirm the diff does not change or weaken the instructions those assertions rely on.
  - If `evals/<skill-name>/baselines/latest/` exists, list the baseline-passing assertions that are at risk and show them to the user before commit. Keep this advisory, matching the subsection's existing non-blocking style.
- Add an enumeration-consistency step next to "### Cross-section reference consistency":
  - When the diff adds or removes an item from an enumerated set (checks, verdict rows, steps), search the file and its parent SKILL.md for count words and lists that refer to that set, such as "all four checks", "exactly five rows" or mapping tables, and update all of them.
  - Flag any mapping that targets an undefined row or section.
- Keep the guidance method-only, with no language- or framework-specific references.

## Reuse Candidates
- `plugins/sdlc-workflow/skills/implement-task/SKILL.md::Eval coverage currency` — existing subsection to extend
- `plugins/sdlc-workflow/skills/implement-task/SKILL.md::Cross-section reference consistency` — sibling consistency-check pattern to follow
- `plugins/sdlc-workflow/shared/eval-coverage-propagation.md` — existing eval-coverage rules
- `evals/implement-task/files/task-standard.md` — standard task fixture pattern
- `evals/implement-task/files/repo-backend.md` — repository manifest fixture pattern

## Acceptance Criteria
- [ ] Eval coverage currency triggers for any modified file under `plugins/<plugin>/skills/<skill-name>/`
- [ ] implement-task finds the existing eval assertions tied to the modified files and reports any whose supporting instructions were changed or weakened
- [ ] When a baseline exists, the baseline-passing assertions at risk are listed before commit
- [ ] Stale counts and lists ("all four checks", "exactly N rows") are detected and updated after an enumerated item is added or removed
- [ ] Mappings that point to undefined report rows or sections are flagged
- [ ] The guidance has no language- or framework-specific API references

## Test Requirements
- [ ] Update eval assertions in `evals/implement-task/evals.json` to cover the behavior changes introduced by this task. Add an eval case where a task adds a check to a skill sub-agent prompt that has a count-based constraint, and assert that the stale count is updated and that at-risk existing assertions are surfaced.

---

## Root-cause analysis comment (would be posted on the root-cause task)

Root-cause analysis from TC-9106 verification

- **What exposed the gap:** CI eval review 40001 on PR #747 reported verify-pr eval-3 at 11/13. Review comment 30002 (index suggestion) was classified as a suggestion, but its convention-upgrade eligibility was never evaluated. That assertion passed at baseline, so this is a regression. A second assertion ("30002 results in a sub-task") is not in the baseline and contradicts the current `evals.json`. It was treated as a regression only by the conservative default.
- **Phase:** implement-task. This is a skill gap: the knowledge is universal and the fix is a method, not a fact.
  - The implementation edited `verify-pr/style-conventions.md`, which also holds Check 1 (Convention Upgrade). It left "MUST process all four checks" stale and mapped Documentation Coverage to an undefined "Style Quality *(new)*" report row.
  - The behaviour in Check 1 then regressed with nothing flagging it.
  - implement-task's "Eval coverage currency" triggers only on SKILL.md, looks only for new behaviour that lacks coverage, and never checks existing assertions or baselines.
  - Secondary: plan-feature did not apply eval-coverage propagation to TC-9106 (`evals/verify-pr/evals.json` was not listed). That does not explain the regression.
- **Preventive fix:** broaden implement-task's Step 9 eval-coverage check to cover any file in a skill directory. Surface existing eval and baseline assertions put at risk by the diff. Add an enumeration and cross-reference consistency check.

---
*This comment was AI-generated by [sdlc-workflow/verify-pr](https://github.com/RHEcosystemAppEng/sdlc-plugins) v0.14.0.*
