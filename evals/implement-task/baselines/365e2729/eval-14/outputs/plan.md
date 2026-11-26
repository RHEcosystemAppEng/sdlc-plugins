# Implementation Plan: Eval coverage for the Container Images CPE requirement

Simulation only. No Jira calls, external services, or repository changes were made. This plan describes the eval update I would make.

## Step 0: Project Configuration check

CLAUDE.md has a Repository Registry (sdlc-plugins, path `./`), Jira Configuration (project key TC, Cloud ID, Feature issue type ID 10142) and a Code Intelligence section (no Serena instances). The check passes. Code is inspected with Read, Grep and Glob instead of Serena.

## Steps 0.5 to 3: Jira operations (simulated, skipped)

- Step 1 (fetch task): the task came from `task-eval-repeated-values.md`. It has every required section: Repository = sdlc-plugins, Target Branch = main, Description, Files to Modify, Files to Create (None), API Changes (N/A), Implementation Notes, Acceptance Criteria, Test Requirements and Dependencies. It has no Target PR and no Bookend Type, so the default flow applies.
- Step 1.5 (digest check): skipped because this is a simulation and there are no comments to read.
- Step 2 (dependencies): "None", so nothing to verify.
- Step 3 (assign and move to In Progress): skipped in the simulation.

## Step 4: Understand the code

- **Target file:** `evals/setup/evals.json`, shaped as `{skill_name, evals: [...]}`. Each case has `id`, `prompt`, `expected_output`, `files` and `assertions`, and each assertion is a plain-English string. There are 10 cases now.
- **Matching case:** eval **7** (security-matrix population) already uses `files/security-matrix-image-identity.md`. That fixture has the same rows as the task's supplied fixture: 2.1.0 api-rhel9 and 2.1.0 api-rhel10, both with CPE `cpe:2.3:a:example:trustify_api:2.1.0:*:*:*:*:*:*:*`. Eval 7's `expected_output` already says: "The CPE may be shared across platforms when it identifies the same product version; do not invent platform-specific CPEs." One existing assertion also requires the 2.1.0 CPE on both rows "without requiring CPE uniqueness across platforms."
- **Authoritative contract:** `plugins/sdlc-workflow/skills/setup/SKILL.md` Step 10 (population), item 2, says to add "one Container Images row per unique Product Version / Component pair" and to keep "... image digest, and CPE as distinct values". "Distinct" here means separate columns. It does not mean CPEs must be unique across rows. The uniqueness key is the (Product Version, Component) pair. `docs/templates/security-matrix.template.md` defines `CPE` as a column with no uniqueness rule.
- **CONVENTIONS.md:** present. Fixture files need a `SYNTHETIC TEST DATA` header, which `security-matrix-image-identity.md` already has. CI checks include `uvx skillsaw` and plugin manifest validation.
- **Conventions from sibling cases:** each assertion is one declarative sentence about observable output, names concrete fixture values in backticks or literally, and states negative constraints explicitly (for example "does not ...", "without requiring ...").

## Step 6/7: Reconcile assertion against requirements and fixture

The inputs disagree:

| Source | What it says about CPE |
|---|---|
| Description | Add eval coverage for the CPE requirement in the Container Images table |
| Acceptance Criteria | Every image row includes a **non-empty** CPE value |
| Setup SKILL.md / template | CPE is its own column. Rows are unique per (Product Version, Component). There is **no** CPE uniqueness rule. |
| Supplied fixture | Both 2.1.0 rows have the **same** CPE (`...trustify_api:2.1.0...`) |
| Test Requirements (proposed assertion) | "Every image row has a CPE, **and every CPE value is unique across all rows**." |

**Conflict:** the second half of the proposed assertion adds a uniqueness rule that neither the Acceptance Criteria nor the Setup contract states. The supplied fixture breaks that rule on purpose: one product version (2.1.0) ships two platform images that share one product CPE. That is valid data. Eval 7's `expected_output` already allows it and tells the workflow not to invent platform-specific CPEs. If the assertion were added as written, a correct Setup output would fail grading. It would also push the skill toward making up per-platform CPEs, which contradicts the fixture and the existing expected output.

**Resolution** (following the skill's "Eval assertion/fixture consistency" rule):
- I would not change the fixture to make the CPEs unique, and I would not change the contract.
- I would correct the assertion to match the authoritative requirement, which is "non-empty on every row". I would drop the uniqueness clause and explicitly accept repeated values, using the fixture's own values.
- The Acceptance Criterion and the Setup contract agree, so the source of truth is clear and this correction does not need to block on the user. I would still flag the deviation from the literal Test Requirements text in the PR description and in the Jira comment.

### Planned change to `evals/setup/evals.json`

I would add this assertion to eval **7**'s `assertions` array, directly after the existing "valid rows preserve distinct image references ..." assertion. I am not adding a new eval case: eval 7 already loads this fixture, which follows the Implementation Notes instruction to use the existing Setup eval case structure.

```json
"Every Container Images row in outputs/security-matrix-review.md has a non-empty CPE value; the repeated `cpe:2.3:a:example:trustify_api:2.1.0:*:*:*:*:*:*:*` on both the 2.1.0 api-rhel9 and api-rhel10 rows is accepted as valid and is not flagged, deduplicated, or replaced with invented platform-specific CPEs"
```

Not changed: the fixture `evals/setup/files/security-matrix-image-identity.md`, eval 7's `prompt` and `expected_output` (both already consistent), and all other eval cases.

Rejected form, from the Test Requirements as written:
> "Every image row has a CPE, and every CPE value is unique across all rows."

I rejected it because it contradicts the AC, the Setup contract and the supplied fixture.

## Step 8: Acceptance Criteria verification

- [x] "Every image row includes a non-empty CPE value." The new assertion checks exactly this for every Container Images row and grounds the check in the fixture's concrete rows.
- [x] Test Requirements: an eval assertion is added for the CPE requirement. The uniqueness clause is intentionally left out, for the reasons in the reconciliation above.

## Step 9: Self-verification (planned)

- **Scope:** only `evals/setup/evals.json` changes, which is in Files to Modify. Nothing is created.
- **Eval assertion/fixture consistency:** in the fixture, rows 2.1.0/api-rhel9 and 2.1.0/api-rhel10 have non-empty CPEs that are identical, so the new assertion holds. The 2.1.1/api-rhel10 row also has a non-empty CPE. Eval 7 marks that row as blocked by the revision mismatch, and the CPE assertion does not conflict with that.
- **Overlap:** the existing eval 7 assertion already says the 2.1.0 CPE appears on both rows "without requiring CPE uniqueness". The new assertion adds the non-empty rule for every row and explicitly forbids deduplicating or inventing CPEs. The two are consistent and do not contradict each other.
- **Cross-section consistency:** the fixture path `files/security-matrix-image-identity.md` matches eval 7's `files` list.
- **JSON validity:** after the edit, confirm that `evals.json` still parses (valid commas and quoting).
- **CI from CONVENTIONS.md:** run `uvx skillsaw` and the plugin manifest validation. Any failure stops the work before commit.
- **Sensitive patterns:** none. The fixture uses only synthetic identifiers.

## Step 10/11: Commit, PR, Jira (simulated, not run)

- Branch `<TASK-ID>` from `main`.
- Commit: `test(evals): assert non-empty CPE on every setup Container Images row`. The body explains that the uniqueness clause was dropped because the AC and Setup contract do not require it and the fixture shares one CPE across platforms. Footer `Implements <TASK-ID>` and trailer `Assisted-by: Claude Code (Claude Opus 5.5)`.
- PR against `main` with `Implements [<TASK-ID>](<webUrl>)`, listing the deviation from the literal Test Requirements text.
- Jira: set the PR link in customfield_10875, add a comment with a summary and the deviation note (plus the footnote), and move the task to In Review.
