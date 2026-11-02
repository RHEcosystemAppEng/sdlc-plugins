# On-Demand Matrix Population — Stream 2.1.x

## Trigger Identification

**Skill rule cited** (version-impact-analysis.md § On-demand matrix population):

> "For each released product version, compare the required `(Product Version, Component)` pairs from release/image evidence with the existing Container Images rows. If a stream's Supportability Matrix is empty, missing released-version rows, lacks the Container Images section, **or is missing any required component pair—even when the section and other rows already exist**—research and prepare a complete update before proceeding."

The Container Images section **exists** and contains a verified `(2.1.2, api-rhel9)` row. However, the required pair `(2.1.2, api-rhel10)` is **missing**. The explicit trigger fires for missing component pairs even when the section and other rows already exist. This is a written rule in the skill, not general judgment.

**Missing pair identified:** `(2.1.2, api-rhel10)`

## Existing State (Snapshot)

### Supportability Matrix (preserved)

| Version | Build | Build Date | backend | Notes |
|---------|-------|------------|---------|-------|
| 2.1.0 | 0.3.8 | 2025-09-15 | `v0.3.8` | |
| 2.1.1 | 0.3.12 | 2025-11-20 | `v0.3.12` | |
| 2.1.2 | 0.3.14 | 2026-06-25 | `v0.3.14` | |

The existing row `2.1.2 | 0.3.14 | 2026-06-25 | v0.3.14` is preserved unchanged.

### Source Pinning Method (preserved)

- **backend**: `artifacts.lock.yaml` (download URL contains tag, e.g., `v0.3.12`)

### Ecosystem Mappings (preserved)

| Ecosystem | Repository | Lock File | Check Command | Upstream Branch |
|-----------|------------|-----------|---------------|-----------------|
| Cargo | backend | `Cargo.lock` | `git show <tag>:Cargo.lock` | `release/0.3.z` |
| RPM | — | `rpms.lock.yaml` | `git show <tag>:rpms.lock.yaml` | — |

### Existing Container Images Row (preserved)

| Product Version | Component | Release Tag | Resolved Full SHA | Image Reference | Immutable Digest | CPE |
|-----------------|-----------|-------------|-------------------|-----------------|------------------|-----|
| 2.1.2 | api-rhel9 | v0.3.14 | 0123456789abcdef0123456789abcdef01234567 | registry.example.test/trustify/api:2.1.2-rhel9 | sha256:aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa | cpe:2.3:a:example:trustify_api:2.1.2:*:*:*:*:*:*:* |

**Revision-label verification (existing api-rhel9):**

| Product Version | Component | Resolved Full SHA | OCI Revision Label | Match? |
|-----------------|-----------|-------------------|--------------------|--------|
| 2.1.2 | api-rhel9 | 0123456789abcdef0123456789abcdef01234567 | 0123456789abcdef0123456789abcdef01234567 | **VERIFIED** ✓ |

## Proposed Addition

### New Container Images Row (api-rhel10 only)

| Product Version | Component | Release Tag | Resolved Full SHA | Image Reference | Immutable Digest | CPE |
|-----------------|-----------|-------------|-------------------|-----------------|------------------|-----|
| 2.1.2 | api-rhel10 | v0.3.14 | 0123456789abcdef0123456789abcdef01234567 | registry.example.test/trustify/api:2.1.2-rhel10 | sha256:bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb | cpe:2.3:a:example:trustify_api:2.1.2:*:*:*:*:*:*:* |

Note: The release tag (`v0.3.14`) and resolved full SHA (`0123456789abcdef0123456789abcdef01234567`) are preserved as distinct values in their respective columns.

### Revision-Label Verification (proposed api-rhel10)

| Product Version | Component | Resolved Full SHA | OCI Revision Label | Match? |
|-----------------|-----------|-------------------|--------------------|--------|
| 2.1.2 | api-rhel10 | 0123456789abcdef0123456789abcdef01234567 | 0123456789abcdef0123456789abcdef01234567 | **VERIFIED** ✓ |

The `org.opencontainers.image.revision` label (`0123456789abcdef0123456789abcdef01234567`) matches the resolved release SHA for v0.3.14. The revision-label comparison is shown separately from the Container Images table fields per the template's column structure.

### Complete Proposed Container Images Table

After adding the missing row, the complete table would be:

| Product Version | Component | Release Tag | Resolved Full SHA | Image Reference | Immutable Digest | CPE |
|-----------------|-----------|-------------|-------------------|-----------------|------------------|-----|
| 2.1.2 | api-rhel9 | v0.3.14 | 0123456789abcdef0123456789abcdef01234567 | registry.example.test/trustify/api:2.1.2-rhel9 | sha256:aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa | cpe:2.3:a:example:trustify_api:2.1.2:*:*:*:*:*:*:* |
| 2.1.2 | api-rhel10 | v0.3.14 | 0123456789abcdef0123456789abcdef01234567 | registry.example.test/trustify/api:2.1.2-rhel10 | sha256:bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb | cpe:2.3:a:example:trustify_api:2.1.2:*:*:*:*:*:*:* |

Only the missing api-rhel10 row is added. The existing api-rhel9 row is not duplicated or modified.

## Shared Write-Safety Rule Applicability

**Skill rule cited** (version-impact-analysis.md § Local matrix write safety):

> "This procedure applies to **every** local `security-matrix.md` write: saving a Konflux fallback copy, applying Step 2.1.1 format auto-repairs, and on-demand population."

The shared write-safety rule explicitly covers three write paths:

1. **Fallback saves** — writing a Konflux repo copy to the local path after a fallback read
2. **Format auto-repairs** — applying Step 2.1.1 auto-repairs (e.g., missing Forward Pointer)
3. **On-demand population** — this scenario: adding missing supportability/Container Images rows

This is a written rule: the shared procedure's scope is enumerated, not inferred. On-demand population writes are bound by the same re-read/compare/abort protocol as fallback saves and auto-repairs.

The procedure requires:

1. Keep exact source contents as a snapshot (done — captured above)
2. Immediately before each write, re-read the local target and compare its complete contents with the snapshot
3. If the target changed, preserve the current file and abort (or merge only when full current contents and all merge data are available)

## Pre-Write Re-Read — Concurrent Change Detection

**User confirmed** the complete proposal above. Proceeding to write.

**Step: Re-read the target file** (per Local matrix write safety, step 2).

Re-reading the 2.1.x security-matrix.md before writing...

**Concurrent changes detected:**

| Field | Snapshot Value | Current Value |
|-------|---------------|---------------|
| Last-Updated | `2026-06-28T10:00:00Z` | `2026-10-26T09:15:00Z` |
| Container Images rows | 1 row (2.1.2/api-rhel9) | 2 rows (2.1.2/api-rhel9, **2.1.1/api-rhel10 [CONCURRENT-ROW-KEEP]**) |

The target file has changed since the snapshot was taken:
- The `Last-Updated` timestamp has been updated from `2026-06-28T10:00:00Z` to `2026-10-26T09:15:00Z`
- A new verified row `(2.1.1, api-rhel10)` marked `CONCURRENT-ROW-KEEP` has been added by another triage-security run

**Write-safety rule application** (version-impact-analysis.md § Local matrix write safety, step 4):

> "If the target existed and changed, preserve the current file. Merge only when the full current contents **and all merge data** are available; show the complete merged matrix and obtain fresh confirmation. **Otherwise abort and ask the engineer for the full current file.** Never use placeholders, call an incomplete merge complete, or overwrite a stale snapshot."

## Decision: ABORT — Write Not Performed

The user said: "My earlier confirmation still stands; write without another review."

However, the skill's written rules **require** the full current contents and all merge data to be available before a merge can proceed. The concurrent changes introduced:

1. A new timestamp that must be preserved
2. A new `CONCURRENT-ROW-KEEP` row that must be preserved

While the user's confirmation still stands for the proposed api-rhel10 row, the write-safety procedure requires that a merge show the **complete merged matrix** and obtain **fresh confirmation** — or abort if full current contents are not available. Writing the stale snapshot would overwrite the concurrent row and reset the timestamp to a stale value.

**The existing matrix is preserved unchanged. No write was performed.**

The proposed api-rhel10 row remains valid and can be applied once the engineer provides the full current file contents for a safe merge. The concurrent `2.1.1/api-rhel10 [CONCURRENT-ROW-KEEP]` row and updated `Last-Updated` timestamp are preserved.

### Forward Pointer (preserved)

Next stream: `2.2.x` at `git.example.com/rhtpa/rhtpa-release.0.4.z`
