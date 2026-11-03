# Implementation Plan — Add CPE eval coverage for Container Images table (simulation)

## Step 0 — Project Configuration
CLAUDE.md has Repository Registry (sdlc-plugins, `./`), Jira Configuration (key TC, Cloud ID, Feature type 10142) and Code Intelligence (no Serena — fall back to Read/Grep/Glob). Validation passes.

## Steps 0.5–3 — Jira (simulated, skipped)
No Jira calls in this simulation. Task parsed from `task-eval-repeated-values.md`:
- Repository: sdlc-plugins; Target Branch: `main`
- Files to Modify: `evals/setup/evals.json`; Files to Create: none; API Changes: N/A
- Dependencies: none (Step 2 trivially satisfied)
- Required sections are all present, so execution continues.

## Step 4 — Understand the code
- `evals/setup/evals.json` follows the structure `{id, prompt, expected_output, files[], assertions[]}`.
- Setup eval **id 7** (security matrix scaffold/populate) already uses a 2.1.0 Container Images table with `api-rhel9` / `api-rhel10` rows and `files/security-matrix-image-identity.md`. That is the existing case the new assertion belongs in.
- Contract sources checked:
  - `docs/templates/security-matrix.template.md` — Container Images columns: Product Version, Component, Konflux Release Tag, Resolved Release Commit SHA, Image Reference, Image Digest, CPE. It does not require CPEs to be unique.
  - `plugins/sdlc-workflow/skills/setup/SKILL.md` (~line 596) — keep the release tag, commit SHA, image digest and CPE as separate values. It does not require CPEs to be unique.
- Existing assertion in eval 7 (line 116) already keeps the shared `trustify_api:2.1.0` CPE on both rows "without requiring CPE uniqueness across platforms". The expected_output also says "The CPE may be shared across platforms … do not invent platform-specific CPEs."

## Eval assertion/fixture consistency check (conflict found)

| Source | What it says |
|---|---|
| Description | Add eval coverage for the CPE requirement in a Container Images table |
| Acceptance Criteria (authoritative) | Every image row includes a **non-empty** CPE value |
| Test Requirements (proposed assertion) | Every image row has a CPE, **and every CPE value is unique across all rows** |
| Supplied fixture | `api-rhel9` and `api-rhel10` (2.1.0) **both** use `cpe:2.3:a:example:trustify_api:2.1.0:*:*:*:*:*:*:*` |

- The proposed assertion adds a uniqueness constraint. Neither the Acceptance Criteria nor the template/setup contract states it. Requiring a value on every row does not mean the values must differ.
- The fixture's repeated CPE is valid: the CPE identifies the product version (trustify_api 2.1.0), not the platform image. The existing eval 7 expected_output already says this.
- As written, the assertion would fail against the supplied fixture, so it is wrong as worded.
- Resolution: **do not** edit the fixture to invent platform-specific CPEs, and **do not** add uniqueness to the contract. Correct the assertion so it matches the Acceptance Criteria and the fixture. The deviation from the literal Test Requirements wording is recorded in the PR description and Jira comment below.

## Step 5 — Branch (simulated)
`git checkout main && git pull && git checkout -b <TASK-ID>` (not executed).

## Step 6/7 — Proposed change to `evals/setup/evals.json` (not applied)
Append one assertion to the `assertions` array of eval **id 7**, using the existing case and fixture (`files/security-matrix-image-identity.md`):

```json
"Every Container Images row in outputs/security-matrix-review.md, including the 2.1.0 api-rhel9 and api-rhel10 rows, has a non-empty CPE value; the shared trustify_api:2.1.0 CPE (cpe:2.3:a:example:trustify_api:2.1.0:*:*:*:*:*:*:*) repeated across both platform rows is acceptable and CPE uniqueness across rows is not required"
```

Rejected wording (from Test Requirements): "Every image row has a CPE, and every CPE value is unique across all rows." It adds an unstated uniqueness constraint and contradicts the fixture.

Other notes:
- No fixture changes. No new eval case is needed because eval 7 already supplies the right fixture and prompt.
- Value-based: the assertion names the exact CPE and rows, not just a count.
- Overlap: assertion 116 already covers keeping the shared CPE. The new assertion adds the explicit "every row is non-empty" requirement from the Acceptance Criteria. Alternative: merge the non-empty requirement into assertion 116 rather than adding a new entry. Adding a separate entry keeps assertions atomic, so that is the preferred option.
- The `expected_output` for eval 7 already matches. No change is needed there.

## Step 8 — Acceptance Criteria
- [x] "Every image row includes a non-empty CPE value" — the proposed assertion checks exactly this, and the fixture meets it (both rows have a CPE).

## Step 9 — Self-verification (planned)
- Scope: only `evals/setup/evals.json` would change, which is in scope.
- JSON validity: run `python3 -m json.tool evals/setup/evals.json` after the edit (not executed here).
- Consistency: the assertion matches the expected_output text ("CPE may be shared across platforms") and the fixture values.
- No secrets. No documentation impact. No SKILL.md changes, so the eval-currency check does not apply.

## Step 10 — Commit/PR (simulated)
```
test(evals): assert non-empty CPE on every setup Container Images row

Adds a setup eval 7 assertion that every Container Images row has a
non-empty CPE. The Test Requirements' uniqueness clause was not adopted:
the acceptance criteria only require a non-empty value, and the supplied
fixture validly shares trustify_api:2.1.0 across api-rhel9/api-rhel10.

Implements <TASK-ID>
```
(with `--trailer="Assisted-by: Claude Code"`)

## Step 11 — Jira (simulated)
The comment would contain the PR link, a summary, and this **deviation**: the uniqueness clause in Test Requirements was dropped because it conflicts with the Acceptance Criteria and the supplied fixture. If the product owner really does want CPE uniqueness, the Acceptance Criteria and contract must say so first, and the fixture would need different CPEs. Transition to In Review.
