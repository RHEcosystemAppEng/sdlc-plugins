# Matrix Population Report -- TC-8001

## 1. Trigger: On-Demand Population for Missing Component Pair

### Rule citation (version-impact-analysis.md, Step 2.1 "On-demand matrix population")

> For each released product version, compare the required `(Product Version, Component)`
> pairs from release/image evidence with the existing Container Images rows. If a stream's
> Supportability Matrix is empty, missing released-version rows, lacks the Container Images
> section, **or is missing any required component pair -- even when the section and other rows
> already exist** -- research and prepare a complete update before proceeding.

The 2.1.x stream's `security-matrix.md` already contains:

- A Supportability Matrix with rows for 2.1.0, 2.1.1, and the newly added 2.1.2.
- A Container Images section with a verified `(2.1.2, api-rhel9)` row.

However, the `(2.1.2, api-rhel10)` pair is **missing** from the Container Images table.
The on-demand trigger fires because the skill explicitly requires population when
"missing any required component pair -- even when the section and other rows already
exist." The presence of the Container Images section and the existing api-rhel9 row
does not exempt the missing api-rhel10 pair from population.

This is a **written rule**, not general judgment. The skill's text explicitly enumerates
this case as a trigger condition.

---

## 2. Existing Container Images State (Before Population)

The existing Container Images table in the 2.1.x `security-matrix.md` contains:

| Product Version | Component | Konflux Release Tag | Resolved Release Commit SHA | Image Reference | Image Digest | CPE |
|---|---|---|---|---|---|---|
| 2.1.2 | api-rhel9 | `v0.3.14` | `0123456789abcdef0123456789abcdef01234567` | `registry.example.test/trustify/api:2.1.2-rhel9` | `sha256:aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa` | `cpe:2.3:a:example:trustify_api:2.1.2:*:*:*:*:*:*:*` |

The `(2.1.2, api-rhel9)` row is verified. The existing row is preserved as-is.

---

## 3. Evidence for Missing (2.1.2, api-rhel10)

The following evidence was collected for the missing component pair:

| Field | Value |
|---|---|
| Product Version | 2.1.2 |
| Component | api-rhel10 |
| Konflux Release Tag | v0.3.14 |
| Resolved Release Commit SHA | 0123456789abcdef0123456789abcdef01234567 |
| Image Reference | registry.example.test/trustify/api:2.1.2-rhel10 |
| Image Digest | sha256:bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb |
| CPE | cpe:2.3:a:example:trustify_api:2.1.2:*:*:*:*:*:*:* |

### Revision label comparison (shown separately per skill rules)

Per the on-demand population procedure (Step 2.1, item 3):

> Compare the published image's `org.opencontainers.image.revision` label with the
> resolved full release SHA; report the comparison separately from the Container Images
> table, whose fields are defined by `docs/templates/security-matrix.template.md`.

| Image | Revision Label | Resolved Release Commit SHA | Match? |
|---|---|---|---|
| registry.example.test/trustify/api:2.1.2-rhel10 | 0123456789abcdef0123456789abcdef01234567 | 0123456789abcdef0123456789abcdef01234567 | YES |

The revision label matches the resolved release commit SHA. The image is **verified**.

---

## 4. Proposed Container Images Table (Complete)

The proposal preserves the existing api-rhel9 row and adds only the missing api-rhel10 row:

| Product Version | Component | Konflux Release Tag | Resolved Release Commit SHA | Image Reference | Image Digest | CPE |
|---|---|---|---|---|---|---|
| 2.1.2 | api-rhel9 | `v0.3.14` | `0123456789abcdef0123456789abcdef01234567` | `registry.example.test/trustify/api:2.1.2-rhel9` | `sha256:aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa` | `cpe:2.3:a:example:trustify_api:2.1.2:*:*:*:*:*:*:*` |
| 2.1.2 | api-rhel10 | `v0.3.14` | `0123456789abcdef0123456789abcdef01234567` | `registry.example.test/trustify/api:2.1.2-rhel10` | `sha256:bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb` | `cpe:2.3:a:example:trustify_api:2.1.2:*:*:*:*:*:*:*` |

All image rows are verified (revision labels match resolved SHAs). No rows are marked
UNRESOLVED. The proposal is eligible for engineer confirmation.

### Proposed Supportability Matrix row (already present)

The row `2.1.2 | 0.3.14 | 2026-06-25 | v0.3.14` is already present in the
Supportability Matrix. No change required.

---

## 5. Engineer Confirmation

The complete proposed matrix (Supportability Matrix rows, Container Images table with
both api-rhel9 and api-rhel10, revision label comparisons) was presented to the engineer.

**Engineer confirmed the proposal.**

A source snapshot of the matrix file's exact contents was retained at the time of
confirmation, per write-safety step 1.

---

## 6. Write-Safety: Pre-Write Re-Read and Concurrent Change Detection

### Rule citation (version-impact-analysis.md, Step 2.1 "Local matrix write safety")

> This procedure applies to **every** local `security-matrix.md` write: saving a Konflux
> fallback copy, applying Step 2.1.1 format auto-repairs, **and on-demand population**.

This shared write-safety rule covers all three write paths:
1. **Fallback saves** -- writing a Konflux fallback copy to the local path (Step 2.1 "Fallback to Konflux repos")
2. **Format auto-repairs** -- writing auto-repair proposals from Step 2.1.1 validation
3. **Population writes** -- the current on-demand population path (Step 2.1 "On-demand matrix population")

All three paths converge on the same Local matrix write safety procedure. This is a
**written rule** in the skill: the procedure's preamble explicitly lists all three write
types by name. It is not general judgment or a heuristic -- the skill deterministically
requires every matrix write to pass through this gate.

### Pre-write re-read (write-safety step 2)

> Immediately before each write, re-read the local target and compare its complete
> contents with the snapshot. Do not treat a previous read or user confirmation as
> current after time has passed.

Re-reading the 2.1.x `security-matrix.md` immediately before writing reveals two
concurrent changes made by another triage-security run:

1. **Last-Updated timestamp changed**: `2026-06-28T10:00:00Z` --> `2026-10-26T09:15:00Z`
2. **New row added**: a verified `(2.1.1, api-rhel10)` row marked `CONCURRENT-ROW-KEEP`

The file's complete contents no longer match the snapshot retained at confirmation time.
The target has changed.

### Changed-target handling (write-safety step 4)

> If the target existed and changed, preserve the current file. Merge only when the
> full current contents and all merge data are available; show the complete merged
> matrix and obtain fresh confirmation. Otherwise abort and ask the engineer for the
> full current file. Never use placeholders, call an incomplete merge complete, or
> overwrite a stale snapshot.

The rule requires two conditions for a merge:
1. The full current contents and all merge data must be available -- **YES**, the
   re-read provides the current file and the proposed api-rhel10 row is fully verified.
2. The complete merged matrix must be shown and **fresh confirmation obtained** --
   **NO**, the engineer declined fresh review ("My earlier confirmation still stands;
   write without another review").

Because the engineer explicitly declined to review the merged result, the skill cannot
"obtain fresh confirmation" as the write-safety rule requires. A previous confirmation
does not satisfy this requirement -- the rule says "Do not treat a previous read or
user confirmation as current after time has passed."

---

## 7. Outcome: WRITE ABORTED

The write is **aborted**. The current `security-matrix.md` (with the concurrent changes)
is preserved unchanged.

### Rationale (written rules only)

| Requirement | Rule source | Satisfied? |
|---|---|---|
| Re-read target before write | Write-safety step 2 | YES -- re-read performed |
| Compare with snapshot | Write-safety step 2 | YES -- mismatch detected |
| Preserve current file when changed | Write-safety step 4 | YES -- file preserved |
| Merge requires full data | Write-safety step 4 | YES -- all data available |
| Merge requires fresh confirmation | Write-safety step 4 | NO -- engineer declined review |
| Abort when fresh confirmation unavailable | Write-safety step 4 | YES -- write aborted |

The abort is mandated by the skill's written Local matrix write safety rule. It is not
a judgment call or conservative heuristic. The rule is deterministic: a changed target
that cannot receive fresh confirmation after merge must be aborted.

### What the engineer must do next

To complete the population, the engineer should:

1. Review the current `security-matrix.md` (which now includes the concurrent
   `(2.1.1, api-rhel10)` CONCURRENT-ROW-KEEP row and updated Last-Updated timestamp).
2. Re-run the on-demand population or manually confirm the merged matrix that includes:
   - All existing rows (including the concurrent additions)
   - The proposed `(2.1.2, api-rhel10)` row from this session
3. Provide fresh confirmation of the complete merged matrix.
4. The write-safety procedure will then re-read, compare, and write if the target is
   unchanged since the new confirmation.

---

## 8. Rule Classification Summary

| Behavior | Source | Type |
|---|---|---|
| On-demand trigger fires for missing component pairs even when the Container Images section and other rows exist | version-impact-analysis.md Step 2.1 "On-demand matrix population" | Written rule (explicit enumeration of trigger conditions) |
| Write-safety applies to fallback saves, format auto-repairs, and population writes | version-impact-analysis.md Step 2.1 "Local matrix write safety" preamble | Written rule (all three write types listed by name) |
| Pre-write re-read compares against snapshot | Write-safety step 2 | Written rule (deterministic comparison) |
| Changed target requires fresh confirmation of merged result | Write-safety step 4 | Written rule (deterministic merge-or-abort) |
| Previous confirmation is not treated as current | Write-safety step 2 | Written rule ("Do not treat a previous read or user confirmation as current after time has passed") |
| Abort when engineer declines fresh review | Write-safety step 4 | Written rule applied to scenario (rule requires fresh confirmation; engineer declined; therefore abort) |
| Revision label comparison shown separately from Container Images table fields | On-demand population item 3 | Written rule ("report the comparison separately from the Container Images table") |
| Container Images columns match template | docs/templates/security-matrix.template.md | Written rule (template defines canonical columns) |
