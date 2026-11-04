# Implementation Plan — Eval coverage for CPE requirement (simulation)

Source task: `evals/implement-task/files/task-eval-repeated-values.md`
Skill followed: `plugins/sdlc-workflow/skills/implement-task/SKILL.md` (read directly; the Skill tool did not recognize the skill)

> Simulation constraints: no Jira calls, no shell commands, no external services, no repository files modified. Steps that need those are recorded as "would do" only.

## Step 0 – Project Configuration
CLAUDE.md has Repository Registry (sdlc-plugins, `./`), Jira Configuration (key TC, Cloud ID, Feature type 10142) and Code Intelligence (no Serena instances, so Read/Grep/Glob are used instead). Validation passes.

## Steps 1–3 – Task parsing, integrity, dependencies, transition
- All required sections are present: Repository = sdlc-plugins, Target Branch = main, Description, Files to Modify, Files to Create (None), API Changes (N/A), Implementation Notes, Acceptance Criteria, Test Requirements, Dependencies (None).
- No Target PR or Bookend Type, so the default flow applies.
- Step 1.5 digest check, Step 2 dependency check (none to check) and Step 3 assign + transition to In Progress: would run in a real execution. Skipped here because external calls are not allowed.

## Step 4 – Understand the code
- File to modify: `evals/setup/evals.json`. Each case has `id`, `prompt`, `expected_output`, `files`, `assertions[]`.
- Sibling/related coverage: **case id 7** (security matrix population from `files/security-matrix-image-identity.md`) already has a Container Images table with separate 2.1.0 `api-rhel9` and `api-rhel10` rows. Both rows share the CPE `cpe:2.3:a:example:trustify_api:2.1.0:*:*:*:*:*:*:*`. Its `expected_output` says: "The CPE may be shared across platforms when it identifies the same product version; do not invent platform-specific CPEs." Its existing assertion (line 116) says: "...retain the fixture's trustify_api:2.1.0 CPE on both api-rhel9 and api-rhel10 rows **without requiring CPE uniqueness across platforms**...".
- Conventions: assertions are single declarative sentences, written in natural language, that a grader can check against the output files. They refer to concrete fixture values.
- No CONVENTIONS.md lookup result affects this change. No new symbols are introduced.

## Step 7 – Eval assertion/fixture consistency check (key finding)

| Source | What it says |
|---|---|
| Description | Add eval coverage for the CPE requirement in a Container Images table |
| Acceptance Criteria (authoritative requirement) | "Every image row includes a non-empty CPE value." This is about presence only. |
| Supplied fixture | Two rows (2.1.0 / api-rhel9, 2.1.0 / api-rhel10) with the **same** CPE `cpe:2.3:a:example:trustify_api:2.1.0:*:*:*:*:*:*:*` |
| Test Requirements (proposed assertion) | "Every image row has a CPE, **and every CPE value is unique across all rows**." |

**Conflict:** The uniqueness clause in the proposed assertion is not in the Acceptance Criteria or the Description. Requiring a value on every row does not mean the values must be unique. The supplied fixture also breaks the uniqueness clause: both rows have the same CPE, which is valid because both rows identify the same product version (trustify_api 2.1.0) on different platforms. If the assertion were added as written, it would fail on correct output. It could also push the agent under test to make up platform-specific CPEs, which case 7's `expected_output` explicitly forbids.

**Resolution (per the skill):** Leave the fixture and the contract unchanged. Do not make the fixture CPEs unique, and do not add a uniqueness requirement to the AC. Instead, correct the assertion so it matches the authoritative requirement and the fixture:

> "Every Container Images row (including both 2.1.0 api-rhel9 and api-rhel10) has a non-empty CPE value; the shared fixture CPE cpe:2.3:a:example:trustify_api:2.1.0:*:*:*:*:*:*:* is retained on both rows and repeated CPE values across rows are accepted (uniqueness is not required)"

This deviation from the literal Test Requirements text will be reported in the PR description and the Jira comment. If the task author really intended uniqueness, the AC and the fixture both have to change first, and the user/author has to decide that. It cannot be inferred from the assertion.

## Step 6 – Proposed change (not applied)

File: `evals/setup/evals.json`, case `id: 7` (it already uses this fixture and table, so it follows the existing Setup eval case structure as the Implementation Notes ask).

Add one assertion to `assertions[]`, right after the existing image-row assertion on line 116:

```json
"Every Container Images row (including both 2.1.0 api-rhel9 and api-rhel10) has a non-empty CPE value; the shared fixture CPE cpe:2.3:a:example:trustify_api:2.1.0:*:*:*:*:*:*:* is retained on both rows and repeated CPE values across rows are accepted (uniqueness is not required)",
```

- No change to `prompt`, `expected_output`, `files`, or any fixture file. `expected_output` already agrees: "CPE may be shared across platforms".
- Not adding a new case: a new case would duplicate case 7's prompt and fixture. Extending the existing case avoids that duplication (Step 9 duplication check).
- Alternative considered: change only line 116. Rejected. That assertion covers several things (digests, references, revision label), and the task asks for a dedicated assertion for the CPE requirement.

## Step 8 – Acceptance Criteria
- "Every image row includes a non-empty CPE value": the new assertion checks for a non-empty CPE on every row, and the fixture meets it (both rows have a CPE). Satisfied.

## Step 9 – Self-verification (planned)
- Scope: only `evals/setup/evals.json` would change, which is listed in Files to Modify. No fixture or other file is touched.
- JSON validity: the new string goes inside the existing array with a trailing comma, and the array's last element is unchanged.
- Example consistency: the assertion's CPE string, product version (2.1.0) and components (api-rhel9, api-rhel10) match `security-matrix-image-identity.md` and case 7's `expected_output`.
- No conflict with other assertions: case 7 line 116 already says uniqueness is not required. The proposed uniqueness assertion would have contradicted it inside the same case.
- Sensitive-pattern check, CI checks: would run. Nothing to run here because no shell is allowed.

## Steps 10–11 – Commit, PR, Jira (would do)
- Branch `TC-XXXX` from `main`. Commit: `test(evals): add CPE presence assertion to setup security-matrix eval` with footer `Implements TC-XXXX` and trailer `Assisted-by: Claude Code`.
- PR against `main`. The description notes the deviation: the uniqueness clause from Test Requirements was dropped because it is not in the AC and the supplied fixture contradicts it.
- Jira: set customfield_10875 to the PR URL, add a comment (summary + deviation + footnote), transition to In Review.
