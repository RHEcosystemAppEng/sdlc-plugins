# Implementation Plan — Eval coverage for Container Images CPE requirement

Simulation only: no Jira calls, no shell commands, no repository edits.

## Step 0 – Project Configuration
PASS. CLAUDE.md has Repository Registry (sdlc-plugins, `./`), Jira Configuration (TC, Cloud ID, Feature type 10142) and Code Intelligence (no Serena; fall back to Read/Grep/Glob).

## Step 1 – Parsed task
- Repository: sdlc-plugins. Target Branch: `main`. No Target PR or Bookend Type, so the mode is **default**.
- Description: add eval coverage for the CPE requirement in a Container Images table.
- Files to Modify: `evals/setup/evals.json`. Files to Create: none. API Changes: N/A.
- Acceptance Criteria: "Every image row includes a non-empty CPE value."
- Test Requirements (proposed assertion): "Every image row has a CPE, and every CPE value is unique across all rows."
- Supplied fixture: two 2.1.0 rows (`api-rhel9`, `api-rhel10`). Both rows have the same CPE, `cpe:2.3:a:example:trustify_api:2.1.0:*:*:*:*:*:*:*`.
- Dependencies: none.

## Steps 1.5, 2, 3 – Jira (simulated)
Skipped because this is a simulation. In a real run: check the description digest, then assign the task, then move it to In Progress.

## Step 4 – Understand the code
- `evals/setup/evals.json`: each case has `id`, `prompt`, `expected_output`, `files`, `assertions[]`. Assertions are plain-language strings that name the output file and the fixture values they expect.
- Setup case **id 7** already uses the fixture `evals/setup/files/security-matrix-image-identity.md`. Its rows 35–36 contain the same two 2.1.0 rows with the same repeated CPE as the task's fixture. Case 7 `expected_output` already says: "The CPE may be shared across platforms when it identifies the same product version; do not invent platform-specific CPEs." Its assertion at line 116 already says the CPE is retained on both rows "without requiring CPE uniqueness across platforms".
- `CONVENTIONS.md`: the CI checks are `uvx skillsaw`, `claude plugin validate plugins/sdlc-workflow`, and pytest (pytest is only needed when `scripts/` changes). Fixture files must carry a `SYNTHETIC TEST DATA` header, and the existing fixture already has one.
- Conventions from sibling assertions: name the output file (`outputs/security-matrix-review.md`), quote the exact fixture values, and state a positive behavior with a negative guard ("without requiring ...").

## Eval assertion/fixture consistency (Step 7) — CONFLICT FOUND
I checked the proposed Test Requirements assertion against both sources:

1. **Explicit requirement** (Description + Acceptance Criteria): only "every image row includes a non-empty CPE value". Nothing requires uniqueness.
2. **Fixture semantics**: `api-rhel9` and `api-rhel10` for 2.1.0 have the **same** CPE. That is valid, because a CPE identifies the product version, not the platform build.

The clause "every CPE value is unique across all rows" adds a constraint the contract does not state. A presence requirement does not imply uniqueness. The supplied fixture would also **fail** that clause, so a correct output would be graded as wrong.

Resolution, per the skill rule:
- I will **not** change the fixture (for example by inventing platform-specific CPEs). I will not change the Acceptance Criteria either.
- I will **correct the assertion** to match the authoritative requirement and the fixture. I will drop the uniqueness clause and add an explicit guard that repeated CPEs are allowed.
- I will record the deviation for the user, the PR, and the Jira comment.

## Step 5 – Branch (planned)
`git checkout main && git pull && git checkout -b <jira-issue-id>`

## Step 6/7 – Proposed change to `evals/setup/evals.json`
Use the existing fixture. Add a new assertion to the Setup case that already loads it (**id 7**), because that case's prompt produces the Container Images table. I am adding it to case 7 rather than creating a new case, which would duplicate the setup.

Assertion to add, after the current line 116 assertion in case 7's `assertions` array:

```json
"Every image row in the outputs/security-matrix-review.md Container Images table has a non-empty CPE value; the 2.1.0 api-rhel9 and api-rhel10 rows both carry cpe:2.3:a:example:trustify_api:2.1.0:*:*:*:*:*:*:* and the assertion does not require CPE values to be unique across rows"
```

Rejected wording (from Test Requirements, not used): "Every image row has a CPE, and every CPE value is unique across all rows."

Optional overlap note: the line 116 assertion already mentions retaining the shared CPE without requiring uniqueness. The new assertion adds the missing **non-empty on every row** check, which is the actual Acceptance Criterion, and it checks the CPE value itself rather than just counting rows. I will not edit line 116.

No change to `expected_output`. It already allows shared CPEs. No fixture edits.

## Step 8 – Acceptance Criteria
- "Every image row includes a non-empty CPE value": covered by the new assertion. It is consistent with the fixture, because every row in `security-matrix-image-identity.md` has a CPE.

## Step 9 – Self-verification (planned)
| # | Check | Result |
|---|---|---|
| 1 | Scope containment | PASS: only `evals/setup/evals.json` is changed |
| 3 | Sensitive patterns | PASS: synthetic `example`/`registry.example.test` values only |
| 5 | Duplication | PASS: reuses the existing case 7 and fixture, no new case. Overlap with the line 116 assertion is noted above |
| 10 | Cross-section references | PASS: the fixture path `files/security-matrix-image-identity.md` and the output path `outputs/security-matrix-review.md` match case 7 |
| 13 | Contract & sibling parity | FLAGGED: the Test Requirements assertion contradicts the AC and the fixture. Fixed by correcting the assertion, and the deviation is reported to the user |
| 14 | CI checks | Would run `uvx skillsaw` and `claude plugin validate plugins/sdlc-workflow`, and validate the JSON. pytest is not needed because `scripts/` is unchanged |

## Step 10 – Commit / PR (planned)
```
test(evals): assert non-empty CPE on every Setup Container Images row

Add a case 7 assertion that every image row has a non-empty CPE, using the
supplied fixture's shared trustify_api:2.1.0 CPE. The task's proposed
uniqueness clause was dropped: the acceptance criteria require presence only,
and the fixture deliberately repeats the CPE across api-rhel9/api-rhel10.

Implements <JIRA-ID>
```
Trailer: `Assisted-by: Claude Code (Claude Opus 5.5)`. Open the PR with `--base main`, and the description says `Implements [<JIRA-ID>](<webUrl>)`.

## Step 11 – Jira (planned)
Set customfield_10875 to the PR URL as ADF. Post a comment with the PR link, a summary, and this **deviation**: "Test Requirements assertion required unique CPEs; corrected to presence-only to match the Acceptance Criteria and the supplied fixture (repeated CPE across platforms is valid)". End the comment with the implement-task footnote, then move the task to In Review.

## Open question for the user
If uniqueness really is a requirement, the Acceptance Criteria and the fixture would both need to change, and that is a product decision. Until the user confirms it, I am following the AC and the fixture.
