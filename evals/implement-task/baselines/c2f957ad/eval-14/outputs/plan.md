# Implementation Plan — Eval coverage for Container Images CPE requirement

Simulation only. No Jira calls, external services, shell commands, or repository edits were made.

## Step 0 – Project Configuration validation

CLAUDE.md has everything the skill needs: the Repository Registry (sdlc-plugins, `./`), Jira Configuration (project key TC, Cloud ID, Feature issue type ID 10142) and Code Intelligence (no Serena instances, so Read/Grep/Glob are used instead). **Pass.**

## Step 0.5 / 1 / 1.5 / 2 / 3 – Jira operations (simulated)

- **Task source:** `evals/implement-task/files/task-eval-repeated-values.md`. It stands in for `jira.get_issue`.
- **Parsed sections:**
  - Repository: `sdlc-plugins`
  - Target Branch: `main`
  - Description, Files to Modify, Files to Create (None), API Changes (N/A), Implementation Notes, Acceptance Criteria, Test Requirements and Dependencies (None) are all present.
  - There is no Target PR and no Bookend Type, so the default flow applies.
- **GitHub Issue field (customfield_10747):** no value in the mock. Skipped.
- **Description digest check (Step 1.5):** no comments are available in the simulation. Under the backward-compatibility rule this means a warning, not a block: "No description digest found — skipping integrity check."
- **Dependencies:** none, so nothing to verify.
- **Step 3:** would assign the task to the current user and move it to In Progress. Not executed.

## Step 4 – Understand the code

- **File to modify:** `evals/setup/evals.json`. It holds a top-level `evals` array. Each case has `id`, `prompt`, `expected_output`, `files` and `assertions` (a list of natural-language strings).
- **Related existing coverage:**
  - Setup eval **id 7** (security matrix population from `files/security-matrix-image-identity.md`) already has a Container Images table with separate 2.1.0 `api-rhel9` and `api-rhel10` rows. Both rows share the CPE `cpe:2.3:a:example:trustify_api:2.1.0:*:*:*:*:*:*:*`.
  - Its `expected_output` says: "The CPE may be shared across platforms when it identifies the same product version; do not invent platform-specific CPEs."
  - Its assertion at line 116 already says "...retain the fixture's trustify_api:2.1.0 CPE on both api-rhel9 and api-rhel10 rows **without requiring CPE uniqueness across platforms**...".
  - Setup eval **id 8** checks that the scaffold keeps a CPE column.
- **Conventions in sibling eval cases:**
  - Each assertion is one declarative sentence.
  - Assertions name concrete fixture values (component names, versions, SHAs).
  - Assertions state explicitly when a constraint is *not* required, as in "without requiring CPE uniqueness".
- **CONVENTIONS.md:** none at the repository root. No CI commands were extracted.

## Step 6/7 – Eval assertion/fixture consistency check (key finding)

The SKILL.md section "Eval assertion/fixture consistency" says to check the proposed assertion against the explicit requirements and against the fixture's meaning.

| Source | What it says |
|---|---|
| Description | "Add eval coverage for the CPE requirement in a Container Images table." |
| Acceptance Criteria (authoritative requirement) | "Every image row includes a non-empty CPE value." This asks for presence only and says nothing about uniqueness. |
| Supplied fixture | Two rows (2.1.0 / `api-rhel9` and 2.1.0 / `api-rhel10`) with the **same** CPE `cpe:2.3:a:example:trustify_api:2.1.0:*:*:*:*:*:*:*`. |
| Test Requirements (proposed assertion) | "Every image row has a CPE, and every CPE value is unique across all rows." |

**There is a conflict.** The "every CPE value is unique across all rows" clause adds a constraint that neither the Acceptance Criteria nor the Description states. It also fails against the supplied fixture, where the same CPE correctly appears on two platform rows of one product version. Requiring a value on every row does not imply that values must be unique, so repeated values are valid here.

**Resolution, following the skill's rule:**

- Do **not** change the fixture, for example by inventing a platform-specific CPE such as `trustify_api_rhel10`. That would also contradict eval 7's existing guidance against inventing platform-specific CPEs.
- Do **not** add a uniqueness requirement to the contract.
- **Correct the assertion** so it matches the Acceptance Criteria and the fixture. It drops the uniqueness clause and says explicitly that repeated CPEs are allowed.

The Acceptance Criteria and the fixture agree with each other, so the source of truth is clear and no user question is needed. The deviation from the Test Requirements wording will be recorded in the commit/PR description and the Jira comment.

## Proposed change to `evals/setup/evals.json`

Add one assertion to Setup eval **id 7**. That is the existing case that uses this exact fixture (`files/security-matrix-image-identity.md`), so the implementation note "Follow the existing Setup eval case structure and use the supplied fixture values" is satisfied without a new case or fixture file.

Insert after the existing Container Images row assertion (current line 110):

```json
"Every Container Images row in outputs/security-matrix-review.md has a non-empty CPE value, including both 2.1.0 api-rhel9 and api-rhel10 rows; repeated CPE values across rows (e.g. the shared cpe:2.3:a:example:trustify_api:2.1.0:*:*:*:*:*:*:* on both platforms) are valid and must not be flagged or replaced",
```

**Rejected wording** (from Test Requirements, not used as written):

> "Every image row has a CPE, and every CPE value is unique across all rows."

Reason: it adds a uniqueness constraint the Acceptance Criteria don't state, and it would fail against the supplied fixture.

**Existing line 116:** no change. It already covers CPE retention without uniqueness and stays consistent with the new assertion.

**No other files change.** That keeps scope within Files to Modify, and Files to Create is None.

## Step 8 – Acceptance Criteria verification

- [x] **"Every image row includes a non-empty CPE value."** The new assertion requires a non-empty CPE on every Container Images row, naming both 2.1.0 rows. The supplied fixture satisfies it: both rows have a CPE.

## Step 9 – Self-verification (planned)

- **Scope containment:** only `evals/setup/evals.json` changes, which is in Files to Modify.
- **Untracked files:** none expected.
- **Sensitive patterns:** none. The change is a plain-text assertion string.
- **Example consistency:** the assertion's example CPE, components and version match the fixture exactly.
- **Cross-section reference consistency:** `evals/setup/evals.json` is the only path referenced, and it is used consistently.
- **Duplication check:**
  - The new assertion overlaps partly with line 116. It is still kept because line 116 is about retaining fixture values, while the new one makes the AC's every-row non-empty requirement explicit and directly testable.
  - If reviewers prefer, the alternative is to fold the "every row non-empty" wording into line 116 instead of adding a line.
- **JSON validity:** would be checked by parsing the file. Not executed in the simulation.
- **CI checks:** no CONVENTIONS.md, so the fallback is the repo's eval/JSON validation if present. Not executed.
- **Data-flow, query-scope, Rust test and contract/sibling parity checks:** mostly not applicable to a single eval-assertion string. For sibling parity, the assertion follows the declarative, fixture-specific style of the id 7/8 assertions.

## Step 10 – Commit and PR (simulated, not executed)

- **Branch:** `git checkout main && git pull && git checkout -b <TASK-ID>`
- **Commit message:**

  ```
  test(evals): add Container Images CPE presence assertion to setup eval

  Assert every image row has a non-empty CPE. The proposed uniqueness
  clause from Test Requirements was dropped: Acceptance Criteria require
  presence only, and the supplied fixture shares one trustify_api:2.1.0
  CPE across api-rhel9 and api-rhel10 rows.

  Implements <TASK-ID>
  ```

  with `--trailer="Assisted-by: Claude Code (Claude Opus 5.5)"`.
- **PR:** `gh pr create --base main`. The body would include `Implements [<TASK-ID>](<webUrl>)` and a note on the deviation. There is no `Closes` line because no GitHub issue is linked.

## Step 11 – Jira update (simulated, not executed)

- Set `customfield_10875` to the PR URL as an ADF inlineCard.
- Add a comment with:
  - the PR link
  - a summary: one assertion added to Setup eval id 7
  - **the deviation:** the uniqueness clause was removed from the Test Requirements assertion because it conflicts with the AC and the fixture
  - the `implement-task` footnote
- Transition the task to In Review.
