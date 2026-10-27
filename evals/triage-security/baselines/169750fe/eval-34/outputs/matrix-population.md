# Matrix Population Review: 2.1.x Stream -- Product Version 2.1.3

## Trigger

On-demand matrix population requested for the 2.1.x stream (Konflux release repo
`git.example.com/rhtpa/rhtpa-release.0.3.z`). The existing Supportability Matrix
contains rows for 2.1.0 and 2.1.1 but is missing the newly released 2.1.3.

## Existing Matrix State (preserved unchanged)

The current `security-matrix.md` for the 2.1.x stream was last updated
2026-06-28T10:00:00Z and contains:

### Supportability Matrix (existing rows)

| Version | Build | Build Date | backend | Notes |
|---------|-------|------------|---------|-------|
| 2.1.0 | 0.3.8 | 2025-09-15 | `v0.3.8` | |
| 2.1.1 | 0.3.12 | 2025-11-20 | `v0.3.12` | |

### Source Pinning Method (existing -- preserved)

- **backend**: `artifacts.lock.yaml` (download URL contains tag, e.g., `v0.3.12`)

### Ecosystem Mappings (existing -- preserved)

| Ecosystem | Repository | Lock File | Check Command | Upstream Branch |
|-----------|------------|-----------|---------------|-----------------|
| Cargo | backend | `Cargo.lock` | `git show <tag>:Cargo.lock` | `release/0.3.z` |
| RPM | --- | `rpms.lock.yaml` | `git show <tag>:rpms.lock.yaml` | --- |

### Forward Pointer (existing -- preserved)

Next stream: `2.2.x` at `git.example.com/rhtpa/rhtpa-release.0.4.z`

---

## Proposed Addition: Version 2.1.3

### Supplied Evidence

| Field | Value |
|-------|-------|
| Product Version | 2.1.3 |
| Build | 0.3.15 |
| Build Date | 2026-07-01 |
| Backend source pin | `v0.3.15` |

### Proposed Supportability Matrix Row

| Version | Build | Build Date | backend | Notes |
|---------|-------|------------|---------|-------|
| 2.1.3 | 0.3.15 | 2026-07-01 | `v0.3.15` | |

### Proposed Container Images Row

| Product Version | Component | Konflux Release Tag | Resolved Release Commit SHA | Image Reference | Image Digest | CPE |
|---|---|---|---|---|---|---|
| 2.1.3 | api-rhel10 | `v0.3.15` | `abcdef0123456789abcdef0123456789abcdef01` | `registry.example.test/trustify/api:2.1.3-rhel10` | `sha256:cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc` | `cpe:2.3:a:example:trustify_api:2.1.3:*:*:*:*:*:*:*` |

---

## Revision-Label Comparison

The published image's `org.opencontainers.image.revision` label must equal the
resolved release commit SHA for the image row to be verified.

| Product Version | Component | Resolved Release Commit SHA | OCI Revision Label | Match? |
|---|---|---|---|---|
| 2.1.3 | api-rhel10 | `abcdef0123456789abcdef0123456789abcdef01` | `fedcba9876543210fedcba9876543210fedcba98` | **MISMATCH** |

**Detail:** The release tag `v0.3.15` resolves to commit SHA
`abcdef0123456789abcdef0123456789abcdef01`, but the published container image
`registry.example.test/trustify/api:2.1.3-rhel10` (digest
`sha256:cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc`) carries
an `org.opencontainers.image.revision` label of
`fedcba9876543210fedcba9876543210fedcba98`. These two SHA values do not match.

---

## Decision: UNRESOLVED -- NOT VERIFIED

The 2.1.3 / api-rhel10 image row is marked **UNRESOLVED -- NOT VERIFIED** due to the
revision-label mismatch described above.

Per the on-demand population procedure:

- A revision-label mismatch is treated as unresolved evidence.
- The affected image record must not be marked as verified.
- Neither SHA may be inferred or substituted.
- No part of the proposal may be written to the matrix while any image row is
  unresolved.

### Proposed Matrix Status: NOT WRITTEN

The existing `security-matrix.md` for the 2.1.x stream remains **unchanged**. Its
`Last-Updated` timestamp stays at `2026-06-28T10:00:00Z`. No supportability row,
Container Images row, or any other modification has been applied.

The complete proposed matrix displayed above is labeled **NOT WRITTEN** and is
shown for review purposes only.

---

## Action Required

Corrected release or image evidence is needed to resolve the mismatch before the
matrix can be updated. Possible causes include:

1. The published container image was built from a different commit than the release
   tag `v0.3.15` (e.g., a rebuild or hotfix that was not re-tagged).
2. The release tag `v0.3.15` was force-pushed after the image was built, changing
   the commit it points to.
3. The OCI revision label was set incorrectly during the image build pipeline.

**Please provide one of the following:**

- A corrected resolved release commit SHA that matches the image's OCI revision label
  (`fedcba9876543210fedcba9876543210fedcba98`), confirming the image was built from
  that commit; or
- A corrected OCI revision label (or a rebuilt image) whose revision label matches
  the release tag's resolved SHA (`abcdef0123456789abcdef0123456789abcdef01`); or
- An explanation for the discrepancy with guidance on which SHA is authoritative for
  this release.

Until corrected evidence is provided, the 2.1.3 row will not be added to the
security matrix and version impact analysis for 2.1.3 cannot proceed.
