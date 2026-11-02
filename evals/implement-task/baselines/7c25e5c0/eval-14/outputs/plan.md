# Implementation Plan — Eval Assertion Update for CPE Requirement

## Analysis: Assertion/Fixture Consistency Check

### Inputs reconciled

1. **Description**: "Add eval coverage for the CPE requirement in a Container Images table."
2. **Acceptance Criteria**: "Every image row includes a non-empty CPE value."
3. **Test Requirements (proposed assertion)**: "Every image row has a CPE, and every CPE value is unique across all rows."
4. **Supplied Fixture**:

   | Product Version | Component | CPE |
   |---|---|---|
   | 2.1.0 | api-rhel9 | `cpe:2.3:a:example:trustify_api:2.1.0:*:*:*:*:*:*:*` |
   | 2.1.0 | api-rhel10 | `cpe:2.3:a:example:trustify_api:2.1.0:*:*:*:*:*:*:*` |

### Conflict detected

The proposed assertion in Test Requirements contains **two conditions**:

1. **"Every image row has a CPE"** — supported by the Acceptance Criteria ("Every image row includes a non-empty CPE value") and by the fixture (both rows have a non-empty CPE).
2. **"Every CPE value is unique across all rows"** — **NOT** supported by either the Acceptance Criteria or the fixture.

**Evidence of conflict:**

- The `api-rhel9` and `api-rhel10` rows share the **exact same CPE value**: `cpe:2.3:a:example:trustify_api:2.1.0:*:*:*:*:*:*:*`. This is semantically correct — both components are builds of the same product version (`trustify_api 2.1.0`) for different RHEL versions, so they share a CPE.
- The Acceptance Criteria only require that every row **includes** a non-empty CPE. There is no uniqueness requirement.
- Requiring uniqueness would be an **unstated contract constraint** — it adds a condition that neither the Description nor the Acceptance Criteria establish.

Per the implement-task skill's eval assertion/fixture consistency guidance (Step 7):

> "Assertions must not add constraints that the contract does not state. In particular, requiring a value on every row does not imply that values must be unique across rows. Repeated fixture values are valid unless the applicable requirement explicitly requires uniqueness."

### Decision: Reject the uniqueness condition

The proposed assertion's uniqueness clause conflicts with:
- The **Acceptance Criteria**, which require only per-row presence, not cross-row uniqueness.
- The **fixture semantics**, where `api-rhel9` and `api-rhel10` deliberately share the same CPE value.

Per the skill guidance, the correct action is to **correct the assertion to match the authoritative requirement and fixture**, not to silently change the fixture or add an unstated constraint.

## Recommended change

### File to modify

`evals/setup/evals.json`

### Corrected assertion

Instead of:
> "Every image row has a CPE, and every CPE value is unique across all rows."

Use:
> "Every image row has a non-empty CPE value."

This assertion:
- Matches the explicit Acceptance Criterion ("Every image row includes a non-empty CPE value").
- Is consistent with the fixture, where both `api-rhel9` and `api-rhel10` have CPE values (which happen to be identical, and that is valid).
- Does **not** impose a uniqueness constraint that the contract does not require.

### What the assertion verifies

For each row in the Container Images table, the assertion checks that the CPE column contains a non-empty string. It does **not** check that CPE values are distinct across rows, because:
1. The Acceptance Criteria do not require uniqueness.
2. The fixture explicitly demonstrates that repeated CPE values are valid (two different components of the same product version share one CPE).
3. Adding uniqueness would be an unsupported contract constraint that would cause the assertion to fail against the supplied fixture.

### What we do NOT change

- The fixture values are **not** modified. The repeated CPE for `api-rhel9` and `api-rhel10` is intentional and correct.
- The Acceptance Criteria are **not** expanded to include uniqueness.
- No new constraints are introduced beyond what the contract states.
