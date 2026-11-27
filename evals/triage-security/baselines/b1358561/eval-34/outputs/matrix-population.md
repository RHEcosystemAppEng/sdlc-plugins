# TC-8001 — On-demand Matrix Population Review (2.1.x stream)

**Status: PROPOSAL NOT WRITTEN — image evidence UNRESOLVED — NOT VERIFIED**

Procedure followed: triage-security `version-impact-analysis.md` > "On-demand matrix
population" (interactive mode) and "Local matrix write safety". Evidence used: only the
synthetic release/image evidence supplied in the task. No Jira MCP, `git show`, registry
API, or other external tool was called. No project file (including the 2.1.x
`security-matrix.md`) was modified.

## 1. Why population was triggered

Source snapshot: the 2.1.x stream matrix (`rhtpa-release.0.3.z`, `Last-Updated:
2026-06-28T10:00:00Z`) as supplied in `security-matrix-mock.md`.

Coverage gaps against released-version evidence:

| Gap | Detail |
|---|---|
| Missing released-version row | 2.1.3 (build 0.3.15, 2026-07-01) is released but absent from the Supportability Matrix (rows end at 2.1.1). |
| Missing `#### Container Images` section | The stream matrix has no Container Images table at all, so no `(Product Version, Component)` pair is recorded. |
| Missing required component pair | `(2.1.3, api-rhel10)` has no Container Images row. |
| Pre-existing pairs without evidence | 2.1.0 and 2.1.1 image components are also unrecorded; no image evidence for them was supplied (see section 5). |

## 2. Collected evidence for `(2.1.3, api-rhel10)` (kept distinct)

| Field | Value | Source |
|---|---|---|
| Product Version | 2.1.3 | supplied release evidence |
| Build / Build Date | 0.3.15 / 2026-07-01 | supplied release evidence |
| backend source pin | `v0.3.15` | supplied release evidence |
| Konflux Release Tag | `v0.3.15` | supplied release evidence |
| Resolved Release Commit SHA (from tag) | `abcdef0123456789abcdef0123456789abcdef01` | supplied tag resolution |
| Image Reference | `registry.example.test/trustify/api:2.1.3-rhel10` | supplied image evidence |
| Image Digest | `sha256:cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc` | supplied image evidence |
| CPE | `cpe:2.3:a:example:trustify_api:2.1.3:*:*:*:*:*:*:*` | supplied image evidence |
| `org.opencontainers.image.revision` label | `fedcba9876543210fedcba9876543210fedcba98` | supplied image evidence |

## 3. Revision-label comparison (reported separately from the Container Images table)

| Product Version | Component | Resolved Release Commit SHA (`v0.3.15`) | Image `org.opencontainers.image.revision` | Result |
|---|---|---|---|---|
| 2.1.3 | api-rhel10 | `abcdef0123456789abcdef0123456789abcdef01` | `fedcba9876543210fedcba9876543210fedcba98` | **MISMATCH — UNRESOLVED — NOT VERIFIED** |

The published image's revision label does not match the commit resolved from the
`v0.3.15` release tag. Under the procedure a revision-label mismatch is unresolved
evidence. Neither SHA is inferred, substituted, or preferred. It is not established that
the published image `sha256:cccc...` was built from the `v0.3.15` release commit.

## 4. Proposed matrix (display only — NOT WRITTEN)

The proposal keeps every existing Supportability Matrix row and source column, the Source
Pinning Method, the Ecosystem Mappings, and the Forward Pointer. It adds the 2.1.3 row and
a Container Images section that uses the canonical template fields. The existing column
header `Version` is left as it is, because existing columns are preserved.

```markdown
<!-- Last-Updated: 2026-06-28T10:00:00Z -->   <-- UNCHANGED (no write performed)

## Version Stream

This Konflux release repo covers the **2.1.x** product version stream.

## Supportability Matrix

| Version | Build | Build Date | backend | Notes |
|---------|-------|------------|---------|-------|
| 2.1.0 | 0.3.8 | 2025-09-15 | `v0.3.8` | |
| 2.1.1 | 0.3.12 | 2025-11-20 | `v0.3.12` | |
| 2.1.3 | 0.3.15 | 2026-07-01 | `v0.3.15` | PROPOSED — NOT WRITTEN; api-rhel10 image UNRESOLVED (revision-label mismatch) |

#### Container Images

| Product Version | Component | Konflux Release Tag | Resolved Release Commit SHA | Image Reference | Image Digest | CPE |
|---|---|---|---|---|---|---|
| 2.1.3 | api-rhel10 | `v0.3.15` | `abcdef0123456789abcdef0123456789abcdef01` | `registry.example.test/trustify/api:2.1.3-rhel10` | `sha256:cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc` | `cpe:2.3:a:example:trustify_api:2.1.3:*:*:*:*:*:*:*` |

> Row status: **UNRESOLVED — NOT VERIFIED**. The image revision label
> (`fedcba98...`) does not equal the resolved release commit SHA (`abcdef01...`).

### Source Pinning Method

- **backend**: `artifacts.lock.yaml` (download URL contains tag, e.g., `v0.3.12`)

## Ecosystem Mappings

| Ecosystem | Repository | Lock File | Check Command | Upstream Branch |
|-----------|------------|-----------|---------------|-----------------|
| Cargo | backend | `Cargo.lock` | `git show <tag>:Cargo.lock` | `release/0.3.z` |
| RPM | — | `rpms.lock.yaml` | `git show <tag>:rpms.lock.yaml` | — |

## Forward Pointer

Next stream: `2.2.x` at `git.example.com/rhtpa/rhtpa-release.0.4.z`
```

## 5. Other observations

- **No 2.1.2 evidence.** The versions jump from 2.1.1 to 2.1.3. Nothing supplied shows
  whether 2.1.2 was released. No 2.1.2 row has been invented. Please confirm whether
  2.1.2 exists and, if it does, supply its build, date, pin, and image evidence.
- **2.1.0 and 2.1.1 image records missing.** The Container Images section is new for this
  stream, so the existing released versions also need `(version, component)` rows. No
  image evidence was supplied for them, so no rows have been invented. Both are
  outstanding evidence items.
- **No lock-file data for `v0.3.15`.** The mock lock-file data stops at `v0.3.12`. Even
  after the matrix is corrected, version-impact analysis for 2.1.3 will need the
  `Cargo.lock` / `rpms.lock.yaml` contents at the verified release commit. Until then,
  2.1.3 cannot be assessed and must be reported as unknown, not "not affected".

## 6. Decision

**Do not write.** Because the `(2.1.3, api-rhel10)` image record is UNRESOLVED — NOT
VERIFIED:

- The current 2.1.x `security-matrix.md` is left exactly as it is, including
  `Last-Updated: 2026-06-28T10:00:00Z`.
- No part of the proposal is written. That includes the 2.1.3 Supportability row on its
  own, because a partial write is prohibited while any image row is unresolved.
- The "Local matrix write safety" write path (final re-read/compare, then
  create-if-absent or merge) was not entered, because the precondition that all image
  rows are verified was not met.
- Triage of TC-8001 should not treat 2.1.3 as covered by the matrix. Any 2.1.3 impact
  verdict stays pending until this is resolved.

## 7. Corrected evidence requested from the engineer

Please supply one of the following for `(2.1.3, api-rhel10)`:

1. **Corrected image evidence.** The reference and digest of an api-rhel10 image whose
   `org.opencontainers.image.revision` equals
   `abcdef0123456789abcdef0123456789abcdef01`, with its CPE.
2. **Corrected tag resolution.** If `v0.3.15` really resolves to
   `fedcba9876543210fedcba9876543210fedcba98` (for example, the tag was moved or
   re-pointed), supply authoritative evidence of the correct tag-to-SHA resolution and
   confirm the backend source pin for 2.1.3.
3. **Explanation of the divergence.** For example, the published image was a rebuild or
   retag from a different commit. Supply evidence identifying the actual release commit
   and its pin.

Also outstanding:

- Confirm whether 2.1.2 exists.
- Supply image evidence for the 2.1.0 and 2.1.1 components.
- Supply lock-file contents at the verified 2.1.3 commit.

Once every image row is verified, the complete proposal will be shown again for explicit
confirmation. It will only be written under Local matrix write safety, and `Last-Updated`
will change only after that write succeeds.
