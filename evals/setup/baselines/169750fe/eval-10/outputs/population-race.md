# Security Matrix Population -- Race Condition Simulation

## Scenario

Setup skill Step 10.6: Populate supportability and image identity for the 2.1.x
stream. A concurrent `triage-security` run modifies the target file between the
user's confirmation and the write attempt.

---

## Phase 1 -- Initial Read and Snapshot

**Action**: Read `security-matrix.md` at the path configured in the 2.1.x Version
Stream entry.

**Snapshot captured** (this is the source snapshot retained per Step 10.6 rule 5):

```markdown
<!-- Last-Updated: 2026-06-28T10:00:00Z -->

# Security Matrix -- 2.1.x Stream

## Version Stream

This Konflux release repo covers the **2.1.x** product version stream.

## Supportability Matrix

| Product Version | Build | Build Date | backend | frontend-ui | Notes |
|---|---|---|---|---|---|
| 2.1.0 | 0.3.12 | 2026-06-15 | `v0.3.12` | `bb447eeb` | |

#### Container Images

| Product Version | Component | Konflux Release Tag | Resolved Release Commit SHA | Image Reference | Image Digest | CPE |
|---|---|---|---|---|---|---|
| 2.1.0 | api-rhel9 | `v0.3.12` | `0123456789abcdef0123456789abcdef01234567` | `registry.example.test/trustify/api:2.1.0-rhel9` | `sha256:aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa` | `cpe:2.3:a:example:trustify_api:2.1.0:*:*:*:*:*:*:*` |
| 2.1.0 | api-rhel10 | `v0.3.12` | `0123456789abcdef0123456789abcdef01234567` | `registry.example.test/trustify/api:2.1.0-rhel10` | `sha256:bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb` | `cpe:2.3:a:example:trustify_api:2.1.0:*:*:*:*:*:*:*` |

### Source Pinning Method

- **backend**: `artifacts.lock.yaml` download URL contains the release tag
- **frontend-ui**: Git submodule at `components/frontend-ui`

## Ecosystem Mappings

| Ecosystem | Repository | Lock File | Check Command | Upstream Branch |
|---|---|---|---|---|
| Cargo | backend | `Cargo.lock` | `git show <tag>:Cargo.lock` | `release/0.3.z` |
| npm | frontend-ui | `package-lock.json` | `git show <commit>:package-lock.json` | `release/0.3.z` |
```

**Snapshot timestamp recorded**: `2026-06-28T10:00:00Z` (from `<!-- Last-Updated: ... -->` header).

---

## Phase 2 -- Evidence Discovery for 2.1.1

**Action**: Analyze release evidence from the image identity file (simulated
discovery; no MCP tools or external services called).

Evidence gathered for Product Version 2.1.1:

| Field | Value | Source |
|---|---|---|
| Build | 0.3.13 | Supportability and Ecosystem Evidence table |
| Build Date | 2026-06-20 | Supportability and Ecosystem Evidence table |
| backend source ref | `v0.3.13` | Supportability and Ecosystem Evidence table |
| frontend-ui source ref | `deadbeef` | Supportability and Ecosystem Evidence table |

Container image evidence for 2.1.1:

| Field | Value |
|---|---|
| Component | api-rhel10 |
| Konflux Release Tag | `v0.3.13` |
| Resolved Release Commit SHA | `89abcdef0123456789abcdef0123456789abcdef` |
| Image Reference | `registry.example.test/trustify/api:2.1.1-rhel10` |
| Image Digest | `sha256:cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc` |
| CPE | `cpe:2.3:a:example:trustify_api:2.1.1:*:*:*:*:*:*:*` |

**Revision label check**: The published image's `org.opencontainers.image.revision`
label is `fedcba9876543210fedcba9876543210fedcba98`, but the resolved release commit
SHA from the release tag is `89abcdef0123456789abcdef0123456789abcdef`. These values
**do not match**. Per Step 10.6 rule 3, this is an unresolved mismatch.

**Action**: Ask user for corrected evidence.

> The published image for 2.1.1/api-rhel10 has an `org.opencontainers.image.revision`
> label (`fedcba9876543210fedcba9876543210fedcba98`) that does not match the resolved
> release commit SHA (`89abcdef0123456789abcdef0123456789abcdef`). Please provide
> corrected evidence for this image.

**User response** (simulated): User supplies valid corrected evidence confirming the
resolved release commit SHA is the authoritative value and the revision label should
be updated. The image row is now verified.

---

## Phase 3 -- Proposal Preparation

**Action**: Compose the complete proposed matrix with the 2.1.1 additions merged
into the snapshot from Phase 1.

**Proposed matrix (additions marked with `[NEW]`):**

```markdown
<!-- Last-Updated: 2026-10-27T00:00:00Z -->

# Security Matrix -- 2.1.x Stream

## Version Stream

This Konflux release repo covers the **2.1.x** product version stream.

## Supportability Matrix

| Product Version | Build | Build Date | backend | frontend-ui | Notes |
|---|---|---|---|---|---|
| 2.1.0 | 0.3.12 | 2026-06-15 | `v0.3.12` | `bb447eeb` | |
| 2.1.1 | 0.3.13 | 2026-06-20 | `v0.3.13` | `deadbeef` | |  [NEW]

#### Container Images

| Product Version | Component | Konflux Release Tag | Resolved Release Commit SHA | Image Reference | Image Digest | CPE |
|---|---|---|---|---|---|---|
| 2.1.0 | api-rhel9 | `v0.3.12` | `0123456789abcdef0123456789abcdef01234567` | `registry.example.test/trustify/api:2.1.0-rhel9` | `sha256:aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa` | `cpe:2.3:a:example:trustify_api:2.1.0:*:*:*:*:*:*:*` |
| 2.1.0 | api-rhel10 | `v0.3.12` | `0123456789abcdef0123456789abcdef01234567` | `registry.example.test/trustify/api:2.1.0-rhel10` | `sha256:bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb` | `cpe:2.3:a:example:trustify_api:2.1.0:*:*:*:*:*:*:*` |
| 2.1.1 | api-rhel10 | `v0.3.13` | `89abcdef0123456789abcdef0123456789abcdef` | `registry.example.test/trustify/api:2.1.1-rhel10` | `sha256:cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc` | `cpe:2.3:a:example:trustify_api:2.1.1:*:*:*:*:*:*:*` |  [NEW]

### Source Pinning Method

- **backend**: `artifacts.lock.yaml` download URL contains the release tag
- **frontend-ui**: Git submodule at `components/frontend-ui`

## Ecosystem Mappings

| Ecosystem | Repository | Lock File | Check Command | Upstream Branch |
|---|---|---|---|---|
| Cargo | backend | `Cargo.lock` | `git show <tag>:Cargo.lock` | `release/0.3.z` |
| npm | frontend-ui | `package-lock.json` | `git show <commit>:package-lock.json` | `release/0.3.z` |
```

---

## Phase 4 -- User Review and Confirmation

**Action**: Present the complete proposed matrix to the user for review.

> Here is the complete proposed security matrix for the 2.1.x stream. Two additions:
>
> 1. Supportability row for 2.1.1 (Build 0.3.13, 2026-06-20)
> 2. Container Images row for 2.1.1/api-rhel10 with verified evidence
>
> All existing rows are preserved unchanged. Please confirm to proceed with writing.

**User response**: User reviews the complete proposal and confirms.

**State after confirmation**: The proposal is approved and ready to write. The
source snapshot used to build this proposal has Last-Updated `2026-06-28T10:00:00Z`.

---

## Phase 5 -- Concurrent Modification (Race Condition)

**While the write is pending**, a concurrent `triage-security` run modifies the
target `security-matrix.md`:

1. Updates `<!-- Last-Updated: ... -->` from `2026-06-28T10:00:00Z` to
   `2026-10-26T09:15:00Z`.
2. Adds a `CONCURRENT-ROW-KEEP` entry for Product Version 2.1.0, Component
   api-rhel10 in the Container Images table.

The file on disk now contains changes that the prepared proposal does not account for.

---

## Phase 6 -- User Requests Immediate Write

**User message**: "My earlier confirmation still stands; write the proposal you
prepared without another review."

---

## Phase 7 -- Pre-Write Re-Read and Comparison

**Per Step 10.6 rule 5**: "After the user confirms, re-read the target immediately
before writing and compare it with that snapshot."

**Action**: Re-read `security-matrix.md` from disk immediately before writing.

### 7.1 -- Comparison: Snapshot vs. Current File

| Attribute | Snapshot (Phase 1) | Current File (Re-Read) | Status |
|---|---|---|---|
| Last-Updated timestamp | `2026-06-28T10:00:00Z` | `2026-10-26T09:15:00Z` | **CHANGED** |
| Supportability rows | 2.1.0 only | 2.1.0 only | Unchanged |
| Container Images rows | 2.1.0/api-rhel9, 2.1.0/api-rhel10 | 2.1.0/api-rhel9, 2.1.0/api-rhel10, **CONCURRENT-ROW-KEEP for 2.1.0/api-rhel10** | **CHANGED -- new row added** |

### 7.2 -- Drift Detection Results

The re-read DETECTS two concurrent changes:

1. **Timestamp drift**: The `Last-Updated` value changed from `2026-06-28T10:00:00Z`
   to `2026-10-26T09:15:00Z`. This means another process modified the file after our
   snapshot was taken. The newer timestamp MUST be preserved.

2. **New concurrent row**: A `CONCURRENT-ROW-KEEP` entry was added for
   2.1.0/api-rhel10. This row was inserted by the concurrent `triage-security` run
   and MUST be preserved -- the stale proposal must not overwrite it.

**Conclusion**: The target file has changed since the snapshot used to prepare the
proposal. The prepared proposal is now STALE relative to the current file state.

---

## Phase 8 -- Merge Attempt and Abort

**Per Step 10.6 rule 5**: "If the target changed, preserve its current contents and
timestamp; merge safely and present the complete merged proposal for fresh
confirmation, or abort and ask the user how to proceed. If the current file's full
contents or required merge data are unavailable, abort and ask the user to provide
them -- never use placeholders or call an incomplete merge complete."

### 8.1 -- Merge Feasibility Assessment

To produce a correct merged proposal, the workflow would need to:

1. Preserve the concurrent timestamp (`2026-10-26T09:15:00Z`) -- **feasible**.
2. Preserve the `CONCURRENT-ROW-KEEP` row for 2.1.0/api-rhel10 -- **NOT feasible**.

The `CONCURRENT-ROW-KEEP` entry's COMPLETE column values are NOT available. The
workflow knows only that a row labeled `CONCURRENT-ROW-KEEP` exists for
2.1.0/api-rhel10, but does not have the full column data required by the Container
Images table schema:

- Konflux Release Tag: **unknown**
- Resolved Release Commit SHA: **unknown**
- Image Reference: **unknown**
- Image Digest: **unknown**
- CPE: **unknown**

Per the skill's rules, the workflow MUST NOT:
- Use placeholders for missing column values
- Guess or fabricate data for the concurrent row
- Call an incomplete merge complete
- Write a stale proposal over a concurrent update

### 8.2 -- Decision: ABORT

**The workflow ABORTS the merge.**

The user's prior confirmation ("write the proposal without another review") does NOT
override the safety rules in Step 10.6. The skill's concurrency safety rules take
precedence over standing user confirmations because:

1. The confirmation was given against a specific proposal built from a specific
   snapshot.
2. The target file has since changed in ways the confirmed proposal does not account
   for.
3. Writing the stale proposal would silently destroy the concurrent
   `CONCURRENT-ROW-KEEP` entry and roll back the timestamp.
4. A correct merge cannot be produced without the full data for the concurrent row.

---

## Phase 9 -- Request Fresh Data and Confirmation

**NO WRITE OCCURS.** The matrix file is left unchanged on disk.

**Action**: Inform the user of the detected concurrent modification and request the
data needed to reconcile.

> **Write aborted -- concurrent modification detected.**
>
> While preparing to write, I re-read `security-matrix.md` and found that it was
> modified by another process since my snapshot was taken:
>
> 1. **Timestamp changed**: `Last-Updated` moved from `2026-06-28T10:00:00Z` to
>    `2026-10-26T09:15:00Z` (a concurrent `triage-security` run updated it).
>
> 2. **New row added**: A `CONCURRENT-ROW-KEEP` entry for 2.1.0/api-rhel10 was
>    inserted into the Container Images table.
>
> I cannot merge my proposal with these changes because the full column data for the
> `CONCURRENT-ROW-KEEP` row is not available to me. Writing the previously confirmed
> proposal would overwrite the concurrent changes, which is not permitted.
>
> **To proceed, I need:**
>
> - The current full contents of `security-matrix.md` (so I can build a merged
>   proposal from the actual current state), OR
> - The complete column values for the `CONCURRENT-ROW-KEEP` row (Konflux Release
>   Tag, Resolved Release Commit SHA, Image Reference, Image Digest, CPE)
>
> Once I have this data, I will prepare a new merged proposal that preserves both the
> concurrent changes and the 2.1.1 additions, present it for your review, and write
> only after fresh confirmation.

---

## Summary of Safety Guarantees Enforced

| Guarantee | Enforced | Detail |
|---|---|---|
| Pre-write re-read of target | Yes | Phase 7: target re-read immediately before writing |
| Comparison with source snapshot | Yes | Phase 7.1: systematic comparison of snapshot vs. current file |
| Detection of timestamp drift | Yes | Phase 7.2: `2026-06-28T10:00:00Z` to `2026-10-26T09:15:00Z` detected |
| Detection of concurrent row addition | Yes | Phase 7.2: `CONCURRENT-ROW-KEEP` entry for 2.1.0/api-rhel10 detected |
| Preservation of concurrent timestamp | Yes | Phase 8: newer timestamp would be preserved in any valid merge |
| Preservation of concurrent row | Yes | Phase 8: concurrent row would be preserved in any valid merge |
| No placeholder or fabricated data | Yes | Phase 8.1: incomplete column data recognized; no placeholders used |
| Abort on incomplete merge data | Yes | Phase 8.2: merge aborted because full CONCURRENT-ROW-KEEP data unavailable |
| No write of stale proposal | Yes | Phase 9: NO WRITE OCCURS; file left unchanged on disk |
| Prior user confirmation does not override safety | Yes | Phase 8.2: standing confirmation rejected; fresh data + fresh confirmation required |
| Request for current full matrix data | Yes | Phase 9: user asked to provide current file contents or complete row data |
| Fresh confirmation required after reconciliation | Yes | Phase 9: new merged proposal will require explicit fresh confirmation before any write |

**Final state**: The `security-matrix.md` file on disk retains the concurrent
changes (Last-Updated `2026-10-26T09:15:00Z` and `CONCURRENT-ROW-KEEP` row). No
write has occurred. The workflow is blocked pending the user's provision of current
full matrix data and a subsequent fresh review-and-confirm cycle.
