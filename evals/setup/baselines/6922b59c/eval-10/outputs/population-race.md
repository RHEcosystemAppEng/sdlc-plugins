# Security Matrix Population — Race Condition Report

## Stream: 2.1.x

Security Matrix Path: `security-matrix.md`
Scaffold source: `docs/templates/security-matrix.template.md`

---

## Step 1 — Initial Read and Snapshot

Read `security-matrix.md` at the configured path. Retained the file's full contents
as the source snapshot for later comparison.

**Source snapshot taken at start of population:**

```
<!-- Last-Updated: 2026-06-28T10:00:00Z -->
```

Supportability Matrix contains only one product version:

| Product Version | Build | Build Date | backend | frontend-ui | Notes |
|---|---|---|---|---|---|
| 2.1.0 | 0.3.12 | 2026-06-15 | `v0.3.12` | `bb447eeb` | |

Container Images table: empty (no rows).
Source Pinning Method: present but unpopulated.
Ecosystem Mappings: present but unpopulated.

---

## Step 2 — Evidence Analysis and Image Identity Verification

Analyzed release and published-image evidence from the supplied
`security-matrix-image-identity.md` file.

### Supportability rows discovered

| Product Version | Build | Build Date | backend | frontend-ui | Notes |
|---|---|---|---|---|---|
| 2.1.0 | 0.3.12 | 2026-06-15 | `v0.3.12` | `bb447eeb` | |
| 2.1.1 | 0.3.13 | 2026-06-20 | `v0.3.13` | `deadbeef` | |

### Container Image identity verification

For each image row, the published `org.opencontainers.image.revision` label
must equal the resolved release commit SHA.

| Product Version | Component | Resolved Release Commit SHA | OCI Revision Label | Match? |
|---|---|---|---|---|
| 2.1.0 | api-rhel9 | `0123456789abcdef0123456789abcdef01234567` | `0123456789abcdef0123456789abcdef01234567` | VERIFIED |
| 2.1.0 | api-rhel10 | `0123456789abcdef0123456789abcdef01234567` | `0123456789abcdef0123456789abcdef01234567` | VERIFIED |
| 2.1.1 | api-rhel10 | `89abcdef0123456789abcdef0123456789abcdef` | `fedcba9876543210fedcba9876543210fedcba98` | MISMATCH |

The 2.1.1/api-rhel10 mapping was initially flagged: the OCI revision label
`fedcba9876543210fedcba9876543210fedcba98` does not match the SHA resolved
from the `v0.3.13` release tag (`89abcdef0123456789abcdef0123456789abcdef`).
Corrected evidence was requested and the user supplied valid image evidence
for 2.1.1 that resolves the mismatch. The verified row was included in the
proposal.

---

## Step 3 — Proposed Matrix (Confirmed by User)

The following complete matrix was presented to the user for review and
**confirmed**.

```markdown
<!-- Last-Updated: <to-be-set-on-write> -->
# Security Matrix — 2.1.x Stream

## Version Stream

This Konflux release repo covers the **2.1.x** product version stream.

## Supportability Matrix

| Product Version | Build | Build Date | backend | frontend-ui | Notes |
|---|---|---|---|---|---|
| 2.1.0 | 0.3.12 | 2026-06-15 | `v0.3.12` | `bb447eeb` | |
| 2.1.1 | 0.3.13 | 2026-06-20 | `v0.3.13` | `deadbeef` | |

#### Container Images

| Product Version | Component | Konflux Release Tag | Resolved Release Commit SHA | Image Reference | Image Digest | CPE |
|---|---|---|---|---|---|---|
| 2.1.0 | api-rhel9 | `v0.3.12` | `0123456789abcdef0123456789abcdef01234567` | `registry.example.test/trustify/api:2.1.0-rhel9` | `sha256:aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa` | `cpe:2.3:a:example:trustify_api:2.1.0:*:*:*:*:*:*:*` |
| 2.1.0 | api-rhel10 | `v0.3.12` | `0123456789abcdef0123456789abcdef01234567` | `registry.example.test/trustify/api:2.1.0-rhel10` | `sha256:bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb` | `cpe:2.3:a:example:trustify_api:2.1.0:*:*:*:*:*:*:*` |
| 2.1.1 | api-rhel10 | `v0.3.13` | `89abcdef0123456789abcdef0123456789abcdef` | `registry.example.test/trustify/api:2.1.1-rhel10` | `sha256:cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc` | `cpe:2.3:a:example:trustify_api:2.1.1:*:*:*:*:*:*:*` |

### Source Pinning Method

- **backend**: `artifacts.lock.yaml` download URL contains the release tag
- **frontend-ui**: Git submodule at `components/frontend-ui`

## Ecosystem Mappings

| Ecosystem | Repository | Lock File | Check Command | Upstream Branch |
|---|---|---|---|---|
| Cargo | backend | `Cargo.lock` | `git show <tag>:Cargo.lock` | `release/0.3.z` |
| npm | frontend-ui | `package-lock.json` | `git show <commit>:package-lock.json` | `release/0.3.z` |

## Forward Pointer

None
```

User reviewed the complete proposal and confirmed it.

---

## Step 4 — Pre-Write Re-Read and Comparison

Per Step 10.6 item 5: "re-read the target immediately before writing and compare
it with that snapshot."

**Re-read of `security-matrix.md` immediately before writing:**

The target file has changed since the source snapshot was taken.

### Changes detected

| Aspect | Source Snapshot | Current File |
|---|---|---|
| `Last-Updated` | `2026-06-28T10:00:00Z` | `2026-10-26T09:15:00Z` |
| Container Images | (empty) | Contains a `CONCURRENT-ROW-KEEP` entry for 2.1.0/api-rhel10 |

A concurrent `triage-security` run modified the target between the initial read
and this pre-write re-read:

1. **Timestamp changed**: `Last-Updated` advanced from `2026-06-28T10:00:00Z` to
   `2026-10-26T09:15:00Z`, indicating a concurrent write.
2. **New row added**: A `CONCURRENT-ROW-KEEP` entry for Product Version 2.1.0 /
   Component api-rhel10 was added to the Container Images table by the concurrent
   triage-security run.

---

## Step 5 — Merge Decision

The proposal prepared in Step 3 is now **stale** relative to the current file.
The skill's Step 10.6 rules require:

> "If the target changed, preserve its current contents and timestamp; merge
> safely and present the complete merged proposal for fresh confirmation, or
> abort and ask the user how to proceed. If the current file's full contents
> or required merge data are unavailable, abort and ask the user to provide
> them — never use placeholders or call an incomplete merge complete. Never
> write a stale proposal over a concurrent update."

### User instruction

The user said: "My earlier confirmation still stands; write the proposal you
prepared without another review."

### Decision: ABORT — merge data unavailable

The concurrent `triage-security` run added a `CONCURRENT-ROW-KEEP` entry for
2.1.0/api-rhel10 to the Container Images table. However, the complete column
values of this concurrent row (Konflux Release Tag, Resolved Release Commit SHA,
Image Reference, Image Digest, CPE) are not available in this simulation context.

A safe merge requires the full contents of every concurrent row to ensure no data
is lost or replaced with placeholders. Since the concurrent row's complete values
were not supplied, the merge cannot be completed without risking data loss or
producing an incomplete result.

Per the skill's constraint — "If the current file's full contents or required
merge data are unavailable, abort and ask the user to provide them — never use
placeholders or call an incomplete merge complete" — the workflow aborts.

**The stale proposal is NOT written.** Writing the confirmed proposal without
merging would overwrite the concurrent `triage-security` update, violating the
rule: "Never write a stale proposal over a concurrent update."

---

## Step 6 — Action Required

**No write has occurred.** The security matrix file is unchanged.

To proceed, please provide the current full contents of `security-matrix.md`
(including the complete `CONCURRENT-ROW-KEEP` row values and the updated
`Last-Updated` timestamp). With the full current file contents available, the
workflow can:

1. Build a merged proposal that preserves all concurrent data (the
   `CONCURRENT-ROW-KEEP` entry for 2.1.0/api-rhel10, the newer
   `Last-Updated: 2026-10-26T09:15:00Z` timestamp, and any other concurrent
   changes).
2. Integrate the population data (2.1.1 row, remaining Container Images, Source
   Pinning Methods, Ecosystem Mappings).
3. Present the complete merged proposal for fresh confirmation before writing.
4. Upon confirmation, set `Last-Updated` to the current UTC time and write the
   merged file.

No write occurs until the concurrent change is reconciled and the final merged
proposal is confirmed by the user.
