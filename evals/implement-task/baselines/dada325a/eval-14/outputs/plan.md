# Implementation Plan — Eval coverage for Container Images CPE requirement

Simulation only: no Jira calls, no shell commands affecting the repo, no repository files modified.

## Step 0 – Project Configuration
CLAUDE.md contains Repository Registry (sdlc-plugins, `./`), Jira Configuration (TC, Cloud ID, Feature type 10142) and Code Intelligence (no Serena — fall back to Read/Grep/Glob). Validation passes.

## Steps 0.5–3 – Jira (simulated, skipped)
- Step 1: task parsed from `task-eval-repeated-values.md`. All required sections present (Repository: sdlc-plugins, Target Branch: main, Description, Files to Modify, Files to Create: None, API Changes: N/A, Implementation Notes, Acceptance Criteria, Test Requirements, Dependencies: None). Extra input: Supplied Fixture Values.
- Step 1.5 (digest), Step 2 (no dependencies), Step 3 (assign / In Progress): would run against Jira; skipped in simulation.

## Step 4 – Understand the code
- `evals/setup/evals.json` — `{ skill_name, evals[] }`; each case has `id`, `prompt`, `expected_output`, `files`, `assertions[]` (natural-language strings).
- Eval case **id 7** (security matrix scaffold + populate from `files/security-matrix-image-identity.md`) already exercises the Container Images table. Its existing expected_output says: "the fixture's trustify_api:2.1.0 CPE on both rows. The CPE may be shared across platforms when it identifies the same product version; do not invent platform-specific CPEs." Assertion 116 already says "without requiring CPE uniqueness across platforms".
- `docs/templates/security-matrix.template.md` line 35: Container Images table has a `CPE` column; no uniqueness requirement is stated.
- No CONVENTIONS.md CI commands relevant to a JSON assertion edit beyond JSON validity.

## Eval assertion/fixture consistency check (Step 7) — CONFLICT FOUND

| Source | What it says |
|---|---|
| Description | Add eval coverage for the CPE **requirement** in a Container Images table |
| Acceptance Criteria | "Every image row includes a **non-empty** CPE value." |
| Test Requirements (proposed assertion) | "Every image row has a CPE, **and every CPE value is unique across all rows**." |
| Supplied fixture | 2.1.0 / api-rhel9 and 2.1.0 / api-rhel10 both have `cpe:2.3:a:example:trustify_api:2.1.0:*:*:*:*:*:*:*` (identical) |
| Existing eval 7 contract | CPE may be shared across platforms for the same product version; do not invent platform-specific CPEs |

The proposed assertion adds a uniqueness constraint that:
1. is not stated in the Description, the Acceptance Criteria, or the template contract ("requiring a value on every row does not imply that values must be unique");
2. directly contradicts the supplied fixture (the two rows legitimately repeat the same CPE because they describe the same product version on different platforms) — the assertion would fail against correct output;
3. contradicts eval 7's existing expected_output and assertion 116.

**Resolution:** do not alter the fixture (no fabricated platform-specific CPEs) and do not add uniqueness to the contract. Correct the assertion to match the authoritative Acceptance Criteria and fixture. The deviation from the literal Test Requirements wording is reported in the PR description and Jira comment (and the user may be asked to confirm if they truly intended a uniqueness rule — in which case the AC and fixture would need to change first, out of this task's scope).

## Step 6/7 – Planned change (single file: `evals/setup/evals.json`)

Add one assertion to the `assertions` array of eval case **id 7** (after the existing CPE-related assertion at line 116), following the existing natural-language assertion style:

```json
"Every Container Images row in outputs/security-matrix-review.md (including both 2.1.0 api-rhel9 and api-rhel10 rows) has a non-empty CPE value; repeated CPE values across rows are valid, and the shared fixture CPE cpe:2.3:a:example:trustify_api:2.1.0:*:*:*:*:*:*:* must not be replaced with invented platform-specific CPEs to make values unique"
```

Rejected wording (from Test Requirements, not used): "Every image row has a CPE, and every CPE value is unique across all rows."

No change to `expected_output` (it already describes the shared CPE), `files`, or the fixture file `evals/setup/files/security-matrix-image-identity.md`. No new eval case is needed — Implementation Notes say to follow the existing Setup case structure, and case 7 already carries the fixture.

Note: the blocked 2.1.1 api-rhel10 row is flagged as unverified in eval 7; the assertion targets the valid image rows plus "every row" in the presented table — if the blocked row is presented, it still carries a CPE per the fixture, so the assertion stays consistent.

## Step 8 – Acceptance Criteria
- [x] "Every image row includes a non-empty CPE value" — the new assertion checks exactly this for every Container Images row, and the supplied fixture satisfies it (both rows have the same non-empty CPE).

## Step 9 – Self-verification (planned)
- Scope: only `evals/setup/evals.json` modified — matches Files to Modify. Files to Create: none.
- JSON validity: would run `python3 -m json.tool evals/setup/evals.json`.
- Example consistency: new assertion, expected_output and assertion 116 all agree that the CPE is shared across the two platform rows.
- Duplication: the new assertion overlaps partially with assertion 116 (which covers retention of the shared CPE); the new one adds the explicit non-empty-for-every-row requirement from the AC. Acceptable; alternatively assertion 116 could be extended instead of adding a new one.
- Eval coverage currency: no SKILL.md modified — not applicable.
- Sensitive patterns: none.

## Step 10 – Commit / PR (simulated)
```
test(evals): assert non-empty CPE on every setup Container Images row

Add a setup eval 7 assertion requiring a non-empty CPE on every
Container Images row. Repeated CPE values across platform rows are
valid per the fixture; the task's proposed uniqueness clause was not
adopted because neither the acceptance criteria nor the fixture
support it.

Implements TC-XXXX
```
Trailer: `Assisted-by: Claude Code (Claude Opus 5.5)`. PR against `main`, description noting the deviation.

## Step 11 – Jira (simulated)
Comment would include PR link, summary, and the deviation: "Test Requirements asked for CPE uniqueness across rows; this conflicts with the Acceptance Criteria (non-empty only) and with the supplied fixture (both 2.1.0 rows share one CPE). Assertion corrected to the non-empty requirement; fixture left unchanged." Then transition to In Review.
