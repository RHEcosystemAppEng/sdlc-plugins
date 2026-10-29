# Implementation Plan: CPE Eval Assertion Update

## Conflict Detection

The task contains a conflict between its own sections:

| Source | Requirement |
|---|---|
| **Acceptance Criteria** | "Every image row includes a non-empty CPE value." |
| **Test Requirements** | "Every image row has a CPE, and every CPE value is unique across all rows." |
| **Supplied Fixture** | api-rhel9 and api-rhel10 share the same CPE: `cpe:2.3:a:example:trustify_api:2.1.0:*:*:*:*:*:*:*` |

The Test Requirements assertion adds a **uniqueness constraint** that is contradicted by both:

1. **The Acceptance Criteria** -- the authoritative contract says "non-empty CPE value" per row. It does not state or imply that CPE values must be unique across rows.
2. **The Supplied Fixture** -- the fixture explicitly demonstrates two distinct components (api-rhel9 and api-rhel10) sharing the same CPE value. This is semantically correct: both components belong to the same product version (2.1.0) and therefore share the same CPE identifier. Repeated CPE values across rows are valid domain data, not a fixture error.

## Resolution (per SKILL.md Step 7 -- Eval assertion/fixture consistency)

The skill's eval consistency rule states:

> Assertions must not add constraints that the contract does not state. In particular, requiring a value on every row does not imply that values must be unique across rows. Repeated fixture values are valid unless the applicable requirement explicitly requires uniqueness.

> If an assertion conflicts with the stated requirements or supplied fixture, do not silently change the fixture or contract to make the assertion pass. Correct the assertion to match the authoritative requirement and fixture.

**Decision: Reject the uniqueness assertion.** The Acceptance Criteria (authoritative requirement) does not require uniqueness. The fixture proves that duplicate CPE values are valid. The uniqueness clause in Test Requirements is unsupported by the contract and must be removed from the assertion.

## Corrected Assertion

**Original (from Test Requirements):**
> "Every image row has a CPE, and every CPE value is unique across all rows."

**Corrected:**
> "Every image row has a non-empty CPE value."

This corrected assertion:
- Satisfies the Acceptance Criteria ("every image row includes a non-empty CPE value")
- Is consistent with the supplied fixture (allows api-rhel9 and api-rhel10 to share the same CPE)
- Checks per-row CPE presence without imposing cross-row uniqueness
- Does not add constraints beyond what the contract states

## Planned Change

**File:** `evals/setup/evals.json`

Add an eval assertion that verifies each row in the Container Images fixture has a non-empty CPE field. The assertion iterates over all image rows and confirms the CPE column is present and non-empty, without enforcing uniqueness across rows.

### What the assertion checks

- For each row in the fixture: the CPE field exists and is a non-empty string.

### What the assertion does NOT check

- Cross-row uniqueness of CPE values. Two or more rows may share the same CPE, as demonstrated by the fixture.

## Fixture Values (unchanged)

The supplied fixture is used as-is. No fixture values are modified.

| Product Version | Component | CPE |
|---|---|---|
| 2.1.0 | api-rhel9 | `cpe:2.3:a:example:trustify_api:2.1.0:*:*:*:*:*:*:*` |
| 2.1.0 | api-rhel10 | `cpe:2.3:a:example:trustify_api:2.1.0:*:*:*:*:*:*:*` |

## Verification

- The corrected assertion passes against the supplied fixture (both rows have non-empty CPE values).
- The original uniqueness assertion would fail against the supplied fixture (two rows share the same CPE), confirming the conflict.
