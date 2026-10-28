# Implementation Plan: Eval Update for CPE Requirement in Container Images Table

## Task Summary

Add eval coverage for the CPE requirement in a Container Images table, using
the supplied fixture values.

**File to modify:** `evals/setup/evals.json` -- add an assertion for the CPE
requirement.

## Inputs Reconciliation

Before writing the assertion, the implement-task workflow requires reconciling
the task's Description, Acceptance Criteria, Test Requirements, and supplied
fixture (per SKILL.md Step 7, "Eval assertion/fixture consistency").

### Acceptance Criteria (authoritative contract)

> Every image row includes a non-empty CPE value.

This states a **per-row presence** requirement: each row must have a CPE, and
the CPE must not be empty. It says nothing about uniqueness across rows.

### Test Requirements (proposed assertion)

> Every image row has a CPE, and every CPE value is unique across all rows.

This adds a **global uniqueness** constraint that goes beyond the Acceptance
Criteria. The second clause -- "every CPE value is unique across all rows" --
is an additional constraint not stated anywhere in the contract.

### Supplied Fixture Values

| Product Version | Component   | CPE                                                          |
|-----------------|-------------|--------------------------------------------------------------|
| 2.1.0           | api-rhel9   | `cpe:2.3:a:example:trustify_api:2.1.0:*:*:*:*:*:*:*`        |
| 2.1.0           | api-rhel10  | `cpe:2.3:a:example:trustify_api:2.1.0:*:*:*:*:*:*:*`        |

**Observation:** The `api-rhel9` and `api-rhel10` rows share the exact same
CPE value (`cpe:2.3:a:example:trustify_api:2.1.0:*:*:*:*:*:*:*`). This is
semantically correct -- both components ship the same product artifact at the
same version, so they share a CPE. The fixture intentionally models this
real-world scenario.

## Conflict Detection

The proposed uniqueness assertion in the Test Requirements **conflicts** with
both:

1. **The Acceptance Criteria (contract):** The acceptance criterion requires
   only that every image row includes a non-empty CPE value. It does not
   require that CPE values be unique across rows. Per the SKILL.md eval
   consistency guidance: "Assertions must not add constraints that the contract
   does not state. In particular, requiring a value on every row does not imply
   that values must be unique across rows."

2. **The supplied fixture:** The fixture's `api-rhel9` and `api-rhel10` rows
   share the same CPE value. A uniqueness assertion would fail against the
   fixture data that the task itself supplies. This confirms that uniqueness
   was never intended -- the fixture was designed to include repeated CPE
   values.

### Decision

The proposed uniqueness condition is an **unsupported contract constraint**.
It is contradicted by both the authoritative requirement (Acceptance Criteria)
and the supplied fixture semantics. Per the SKILL.md guidance:

> "If an assertion conflicts with the stated requirements or supplied fixture,
> do not silently change the fixture or contract to make the assertion pass.
> Correct the assertion to match the authoritative requirement and fixture."

Therefore:

- **Do NOT implement the uniqueness clause** from the Test Requirements.
- **Do NOT change the fixture values** (e.g., by giving api-rhel9 and
  api-rhel10 different CPE values) to make uniqueness pass.
- **Correct the assertion** to match the Acceptance Criteria and fixture.

## Corrected Assertion

The assertion to add to `evals/setup/evals.json` should be:

> "Every image row has a non-empty CPE value."

This assertion:
- Validates that each row in the Container Images table includes a CPE
  (per-row presence check).
- Does **not** require CPE values to be unique across rows, allowing the
  fixture's repeated `cpe:2.3:a:example:trustify_api:2.1.0:*:*:*:*:*:*:*`
  value for both `api-rhel9` and `api-rhel10`.
- Matches the Acceptance Criteria exactly.
- Passes against the supplied fixture without modification.

## Changes Summary

| File | Action | Detail |
|------|--------|--------|
| `evals/setup/evals.json` | Modify | Add a new eval assertion checking per-row CPE presence (non-empty) without a uniqueness constraint |

No fixture values are changed. No new files are created.

## Scope Containment

The only file modified is `evals/setup/evals.json`, which matches the task's
Files to Modify section. No out-of-scope files are touched.
