# Implementation Plan — CPE eval coverage for the Container Images table (simulation)

Simulation rules: Jira, external services, and shell commands were not used, and no repository files were changed. The steps below say what would happen in a real run.

## Step 0 – Project Configuration
CLAUDE.md has a Repository Registry (sdlc-plugins, `./`), a Jira Configuration (TC, Cloud ID, Feature type 10142) and a Code Intelligence section (no Serena instances). The configuration is valid, so the run continues.

## Steps 1 / 1.5 / 2 / 3 – Task intake (simulated)
- Task source: `evals/implement-task/files/task-eval-repeated-values.md`. No Jira fetch was made.
- Repository: sdlc-plugins. Target Branch: `main`. There is no Target PR and no Bookend Type.
- Every required section is present.
- The digest check, dependency check (Dependencies: None) and Jira assign/transition were skipped because this is a simulation.

## Step 4 – Understand the Code (Read/Grep fallback, since there is no Serena)
- `evals/setup/evals.json` holds Setup eval cases 1–10. Each case has the fields `id`, `prompt`, `expected_output`, `files`, `assertions[]`. Assertions are plain-language strings.
- The fixture values in the task match `evals/setup/files/security-matrix-image-identity.md`, under "Published OCI Image Evidence". Both 2.1.0 rows, api-rhel9 and api-rhel10, have the CPE `cpe:2.3:a:example:trustify_api:2.1.0:*:*:*:*:*:*:*`. Their image references and digests are different.
- Eval cases **7** and **10** already use this fixture. Case 7 is the one that populates the Container Images table. Its `expected_output` says: "The CPE may be shared across platforms when it identifies the same product version; do not invent platform-specific CPEs." Its assertion #8 already says the shared CPE is kept "without requiring CPE uniqueness across platforms".
- CONVENTIONS.md requires fixtures to have a `SYNTHETIC TEST DATA` header (the existing fixture has one). Its CI checks are skillsaw, plugin validate and pytest, and none of them read eval JSON content.

## Reconciling the assertion with the requirements and the fixture

| Source | What it says |
|---|---|
| Description | Add eval coverage for the CPE requirement in a Container Images table |
| Acceptance Criteria | "Every image row includes a non-empty CPE value." It says nothing about uniqueness. |
| Test Requirements (proposed assertion) | "Every image row has a CPE, **and every CPE value is unique across all rows**." |
| Supplied fixture | 2.1.0/api-rhel9 and 2.1.0/api-rhel10 share the same CPE `cpe:2.3:a:example:trustify_api:2.1.0:*:*:*:*:*:*:*` |
| Existing Setup eval 7 contract | A shared CPE across platforms for the same product version is valid. Do not invent platform-specific CPEs. |

**Conflict found:** the proposed assertion adds a uniqueness rule. Neither the Acceptance Criteria nor the Setup contract states that rule. A rule that every row has a value does not mean the values must differ. The supplied fixture also breaks the rule on purpose: one product version (2.1.0) ships on two platform images, and they correctly share one product CPE. If the assertion were used as written, a correct Setup output would fail. Worse, it would push the skill to make up platform-specific CPEs, which eval 7 forbids.

**Resolution (per "Eval assertion/fixture consistency" in Step 7):**
- Keep the fixture as it is. The two rows correctly share one CPE, and it must not be changed to make the assertion pass.
- Keep the Acceptance Criteria as they are.
- Correct the assertion so it checks only what the Acceptance Criteria require: a non-empty CPE on every row. Add the fixture-specific detail that repeated CPEs are allowed.
- The uniqueness clause is dropped, and this change is recorded as a deviation from the Test Requirements wording in the PR description and the Jira comment.
- If the task author really meant CPEs to be unique, that would be a contract change. It would have to go into the Acceptance Criteria and the Setup skill first, and the fixture would need different data. I would not do that silently.

## Step 6/7 – Proposed change to `evals/setup/evals.json` (the only file in scope)

The new assertion goes into **eval id 7**, the existing case that populates the Container Images table from this fixture. It is added after the current CPE/digest assertion (#8):

```json
"Every Container Images row in the proposed matrix (2.1.0 api-rhel9 and 2.1.0 api-rhel10) has a non-empty CPE value; both rows carry the fixture's cpe:2.3:a:example:trustify_api:2.1.0:*:*:*:*:*:*:* and the repeated CPE is accepted as valid (not flagged as a duplicate or replaced with invented platform-specific CPEs)"
```

Notes:
- The assertion checks the actual values, not just that values exist, because Step 7 prefers value-based checks.
- The blocked 2.1.1 row is left out of the "every row" scope. Assertion #9 already says that row is not presented as verified data, so its CPE is not part of the verified table.
- No new eval case, fixture file or `expected_output` change is needed. Case 7's `expected_output` already describes this behaviour.
- The only edit is a string added to an existing array, so the JSON stays valid.

## Step 8 – Acceptance Criteria
- "Every image row includes a non-empty CPE value" is covered by the new assertion, and the fixture satisfies it: both valid rows have a CPE.

## Step 9 – Self-verification (planned)
- Scope: only `evals/setup/evals.json` changes, which matches Files to Modify.
- Example consistency: the CPE string in the assertion matches the fixture character for character.
- Cross-section consistency: the fixture path `files/security-matrix-image-identity.md` is already in case 7's `files`.
- Eval coverage currency: no SKILL.md changes, so this check does not apply.
- CI: `uvx skillsaw`, `claude plugin validate`, pytest, plus a JSON parse check of `evals/setup/evals.json`. None were run here.

## Step 10/11 – Commit / PR / Jira (not executed)
- Commit: `test(evals): add CPE presence assertion for Setup Container Images table`, with an `Implements <TASK-ID>` footer and an `Assisted-by` trailer.
- PR base: `main`.
- The PR and the Jira comment would list this deviation: the uniqueness clause in the Test Requirements was dropped because it is not in the Acceptance Criteria and the supplied fixture's shared 2.1.0 CPE breaks it.
