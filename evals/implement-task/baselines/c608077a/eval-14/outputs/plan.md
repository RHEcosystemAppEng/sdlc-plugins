# Implementation Plan — Add eval coverage for the CPE requirement (Container Images)

Simulation only. I made no Jira calls and changed no repository files. This file is the plan
for the eval update I would make.

## Step 0 — Project Configuration check
CLAUDE.md has a Repository Registry (sdlc-plugins, `./`), a Jira Configuration (TC, Cloud ID,
Feature type 10142) and a Code Intelligence section (no Serena). The check passes.

## Steps 1 to 3 — Task parsing, digest, dependencies, Jira transition
- Repository: sdlc-plugins. Target Branch: `main`. No Target PR. No Bookend Type.
- All required sections are present: Description, Files to Modify, Files to Create (None),
  API Changes (N/A), Implementation Notes, Acceptance Criteria, Test Requirements and
  Dependencies (None).
- Digest check, dependency check, assign, and transition to In Progress: these were skipped
  because this is a simulation (no Jira).

## Step 4 — Understanding the code (Read/Grep fallback, since no Serena is configured)
- `evals/setup/evals.json` holds `{skill_name, evals[]}`. Each case has `id`, `prompt`,
  `expected_output`, `files` and `assertions[]`.
- The Setup case for Container Images already exists: **eval id 7**. It uses the fixture
  `files/security-matrix-image-identity.md`.
- That fixture's rows 2.1.0/api-rhel9 and 2.1.0/api-rhel10 both carry the same CPE,
  `cpe:2.3:a:example:trustify_api:2.1.0:*:*:*:*:*:*:*`. The task's "Supplied Fixture Values"
  match this exactly.
- The authoritative contract is `docs/project-config-contract.md` (lines 269-271): *"Each
  Container Images row must include a CPE. The same CPE value may appear on multiple rows.
  Require unique CPE values only when a specific contract explicitly says they must be
  unique."* Constraint 1.101 (`docs/constraints.md`) requires a CPE per row but says nothing
  about uniqueness.
- Sibling convention: assertions are single declarative sentences that name the output file
  and the fixture values. The existing assertion at line 116 already says "without requiring
  CPE uniqueness across platforms".

## Reconciling the inputs (Step 7: eval assertion/fixture consistency)

| Source | What it says about CPE |
|---|---|
| Description | Add eval coverage for "the CPE requirement" |
| Acceptance Criteria | Every image row includes a **non-empty** CPE value |
| Project config contract | A CPE is required per row. **Repeated CPEs are allowed.** Uniqueness only applies if a contract states it explicitly |
| Supplied fixture | Two 2.1.0 rows (api-rhel9, api-rhel10) **share the same CPE** |
| Test Requirements (proposed assertion) | "Every image row has a CPE, **and every CPE value is unique across all rows**" |

**Conflict:** the second half of the proposed assertion adds a uniqueness constraint.
- Neither the Acceptance Criteria nor the contract states that constraint, and the contract
  explicitly allows repeated CPEs.
- The supplied fixture breaks it. A correct Setup output keeps the fixture's CPE on both rows,
  so the eval would fail even when Setup behaves correctly.
- It also contradicts eval 7's own `expected_output` ("do not invent platform-specific CPEs")
  and assertion 116.

**Resolution:** the skill rule says to fix the assertion so it matches the authoritative
requirement and fixture, and not to change the fixture or contract to make the assertion pass.
So I would:
- **not** add the uniqueness clause;
- **not** edit `security-matrix-image-identity.md` to invent distinct, platform-specific CPEs;
- **not** touch the contract.

The source of truth is clear here: the Acceptance Criteria and the explicit contract text both
say a CPE is required and may repeat. I would therefore apply the correction and record the
deviation, without blocking. The Jira comment and the PR description would call out that the
Test Requirements wording was narrowed.

## Step 6/7 — Proposed change (only file: `evals/setup/evals.json`)

Append one assertion to the `assertions` array of **eval id 7**, after the existing line 116
assertion:

```json
"Every Container Images row in outputs/security-matrix-review.md has a non-empty CPE value; the 2.1.0 api-rhel9 and api-rhel10 rows both carry the fixture's cpe:2.3:a:example:trustify_api:2.1.0:*:*:*:*:*:*:* value, and the repeated CPE is accepted as valid rather than flagged, deduplicated, or replaced with invented platform-specific CPEs"
```

- No changes to `prompt`, `files` or `expected_output`. The expected output already describes
  a shared CPE on both rows.
- No new eval case. Following the Implementation Notes, this extends the existing Setup case
  that uses the supplied fixture.
- No fixture changes.

## Step 8 — Acceptance Criteria
- "Every image row includes a non-empty CPE value": the new assertion checks this directly, on
  the real fixture values. Satisfied.

## Step 9 — Self-verification (planned)
- Scope: only `evals/setup/evals.json` is changed, as listed in Files to Modify. Nothing
  outside the scope.
- JSON validity: after the edit, `python3 -m json.tool evals/setup/evals.json` must pass.
- Example consistency: the new assertion's CPE string, versions and components match the
  fixture rows 35-36 and eval 7's `expected_output`.
- Cross-section consistency: the assertion agrees with assertion 116 ("without requiring CPE
  uniqueness"). They do not contradict each other.
- Eval coverage currency: no SKILL.md is modified, so this check does not apply.
- Sensitive patterns: none.

## Steps 10 and 11 — Commit, PR and Jira (simulated, not executed)
- Commit: `test(evals): assert non-empty CPE on every Setup Container Images row`, with the
  footer `Implements <TASK-ID>` and the trailer `Assisted-by: Claude Code (Claude Opus 5.5)`.
- PR against `main`. The description notes the deviation: the Test Requirements' uniqueness
  clause was dropped because it conflicts with the Acceptance Criteria,
  `docs/project-config-contract.md` and the supplied fixture (a shared trustify_api:2.1.0 CPE).
- Jira: set the PR link field (customfield_10875), add a comment that includes the deviation
  and the footnote, and transition the task to In Review.
