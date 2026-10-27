# Eval Update Plan — CPE Assertion for Container Images Table

## Conflict Detected: Test Requirements vs. Acceptance Criteria and Fixture

### The Acceptance Criterion (authoritative)

> Every image row includes a non-empty CPE value.

This is a **per-row presence** requirement: each row must have a CPE, but nothing is said about values being distinct across rows.

### The Proposed Test Requirement (conflicts)

> "Every image row has a CPE, and every CPE value is unique across all rows."

The second clause — **"every CPE value is unique across all rows"** — introduces a **uniqueness constraint** that the Acceptance Criteria do not state. This is an unstated contract constraint.

### The Fixture Proves Uniqueness Is Wrong

The supplied fixture contains two rows that share the **exact same CPE value**:

| Product Version | Component | CPE |
|---|---|---|
| 2.1.0 | api-rhel9 | `cpe:2.3:a:example:trustify_api:2.1.0:*:*:*:*:*:*:*` |
| 2.1.0 | api-rhel10 | `cpe:2.3:a:example:trustify_api:2.1.0:*:*:*:*:*:*:*` |

`api-rhel9` and `api-rhel10` are different components (one targets RHEL 9, the other RHEL 10) but share the same product version (`2.1.0`) and therefore the same CPE. This is semantically correct — CPE encodes the product/version, not the OS target. Multiple image rows **can and do** legitimately share a CPE.

Adding a uniqueness assertion would:
1. **Contradict the fixture** — the assertion would fail against the very data it is supposed to validate.
2. **Add a constraint the contract does not require** — the Acceptance Criteria say "non-empty," not "unique."
3. **Misrepresent the domain** — CPEs identify product versions, not individual container images. Requiring uniqueness would incorrectly conflate these two concepts.

### Decision: Reject Uniqueness, Keep Per-Row Presence

Per the implement-task skill's eval assertion/fixture consistency guidance (Step 7):

> Assertions must not add constraints that the contract does not state. In particular, requiring a value on every row does not imply that values must be unique across rows. Repeated fixture values are valid unless the applicable requirement explicitly requires uniqueness.

The proposed uniqueness clause is rejected. The fixture values are **not** changed.

### Corrected Assertion

Replace the proposed assertion with one that checks per-row CPE presence while allowing duplicate values:

**Before (proposed, rejected):**
> "Every image row has a CPE, and every CPE value is unique across all rows."

**After (corrected):**
> "Every image row has a non-empty CPE value."

This assertion:
- Satisfies the Acceptance Criterion ("Every image row includes a non-empty CPE value").
- Passes against the supplied fixture (both rows have a CPE, even though they share the same value).
- Does not introduce constraints beyond what the contract requires.

### Files to Modify

- `evals/setup/evals.json` — add the corrected assertion: `"Every image row has a non-empty CPE value."` Do **not** add a uniqueness check.

### No Fixture Changes

The supplied fixture values (`api-rhel9` and `api-rhel10` sharing `cpe:2.3:a:example:trustify_api:2.1.0:*:*:*:*:*:*:*`) are semantically correct and remain unchanged. The plan does not alter fixture data to satisfy an invalid assertion.
