# On-Demand Matrix Population Review — 2.1.x Stream (TC-8001)

## Context

Vulnerability issue TC-8001 requires triage against the 2.1.x product version stream.
The existing supportability matrix for Stream 1 (`rhtpa-release.0.3.z`, covering the
2.1.x stream) contains rows for product versions 2.1.0 and 2.1.1 only. Product version
2.1.3 has been released but is absent from the matrix. On-demand population is required
before version impact analysis can proceed.

## Existing Matrix State

| Version | Build | Build Date | backend | Notes |
|---------|-------|------------|---------|-------|
| 2.1.0 | 0.3.8 | 2025-09-15 | `v0.3.8` | |
| 2.1.1 | 0.3.12 | 2025-11-20 | `v0.3.12` | |

The matrix has no Container Images section. Version 2.1.3 is not present.

## Supplied Release Evidence for 2.1.3

| Field | Value |
|-------|-------|
| Product Version | 2.1.3 |
| Build | 0.3.15 |
| Build Date | 2026-07-01 |
| Backend source pin | `v0.3.15` |
| Release tag resolves to (full SHA) | `abcdef0123456789abcdef0123456789abcdef01` |

### Container Image Evidence (api-rhel10)

| Field | Value |
|-------|-------|
| Component | api-rhel10 |
| Image Reference | `registry.example.test/trustify/api:2.1.3-rhel10` |
| Image Digest | `sha256:cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc` |
| CPE | `cpe:2.3:a:example:trustify_api:2.1.3:*:*:*:*:*:*:*` |
| `org.opencontainers.image.revision` label | `fedcba9876543210fedcba9876543210fedcba98` |

## Revision-Label Comparison

Per the on-demand population procedure, the published image's
`org.opencontainers.image.revision` label must be compared against the resolved
release commit SHA.

| Evidence | Value |
|----------|-------|
| Resolved release commit SHA (from v0.3.15 tag) | `abcdef0123456789abcdef0123456789abcdef01` |
| Image `org.opencontainers.image.revision` label | `fedcba9876543210fedcba9876543210fedcba98` |
| **Match?** | **NO -- MISMATCH** |

The resolved release commit SHA (`abcdef01...`) does **not** match the image's
`org.opencontainers.image.revision` label (`fedcba98...`). This means the container
image may have been built from a different source commit than the one the release tag
points to. The source provenance of the published image cannot be verified.

## Proposed Supportability Matrix Row

| Version | Build | Build Date | backend | Notes |
|---------|-------|------------|---------|-------|
| 2.1.0 | 0.3.8 | 2025-09-15 | `v0.3.8` | |
| 2.1.1 | 0.3.12 | 2025-11-20 | `v0.3.12` | |
| 2.1.3 | 0.3.15 | 2026-07-01 | `v0.3.15` | |

### Proposed Container Images Section

| Product Version | Component | Konflux Release Tag | Resolved Release Commit SHA | Image Reference | Image Digest | CPE |
|---|---|---|---|---|---|---|
| 2.1.3 | api-rhel10 | `v0.3.15` | `abcdef0123456789abcdef0123456789abcdef01` | `registry.example.test/trustify/api:2.1.3-rhel10` | `sha256:cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc` | `cpe:2.3:a:example:trustify_api:2.1.3:*:*:*:*:*:*:*` |

## Decision: UNRESOLVED -- NOT VERIFIED

The api-rhel10 image row for product version 2.1.3 is marked
**UNRESOLVED -- NOT VERIFIED**.

### Reason

The `org.opencontainers.image.revision` label on the published container image
(`fedcba9876543210fedcba9876543210fedcba98`) does **not** match the full commit SHA
resolved from the v0.3.15 release tag
(`abcdef0123456789abcdef0123456789abcdef01`). This is a revision-label mismatch,
which constitutes unresolved evidence per the on-demand population procedure.

### Consequence

Per the skill's on-demand population rules (Step 2.1):

1. The matrix **must not be written** while any image row has unresolved evidence.
2. The current matrix file and its `Last-Updated` timestamp remain unchanged.
3. The proposed matrix above is labeled **NOT WRITTEN**.
4. The engineer must provide corrected evidence explaining the SHA mismatch before
   the matrix can be updated.

### Required Action

The engineer must investigate and resolve the revision-label mismatch before the
matrix can be populated with version 2.1.3. Specifically:

- Confirm which source commit was actually used to build the published
  `registry.example.test/trustify/api:2.1.3-rhel10` image.
- Either (a) provide the correct release tag that resolves to the image's revision
  label SHA (`fedcba98...`), or (b) provide a corrected image reference built from
  the v0.3.15 tag commit (`abcdef01...`), or (c) explain why the mismatch is
  expected (e.g., a post-release rebuild) and provide the correct resolved SHA.

Until corrected evidence is supplied, the 2.1.3 image row cannot be verified and the
matrix update cannot proceed. Triage of TC-8001 against version 2.1.3 is blocked on
this resolution.

### Impact on Triage

The Supportability Matrix row for 2.1.3 (build 0.3.15, backend source pin v0.3.15)
can still be used for lock-file-based version impact analysis, since the source pin
is unambiguous. However, the Container Images table cannot be completed until the
revision-label mismatch is resolved, and therefore the full matrix write is withheld.
