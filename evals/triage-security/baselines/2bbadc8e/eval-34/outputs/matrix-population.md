# Matrix Population Review: 2.1.x Stream — Product Version 2.1.3

## Context

Vulnerability issue **TC-8001** requires version impact analysis across all supported
streams. The 2.1.x stream's `security-matrix.md` (covering `rhtpa-release.0.3.z`) is
incomplete: it contains rows for product versions 2.1.0 (build 0.3.8) and 2.1.1
(build 0.3.12) only. Product version **2.1.3** has been newly released and must be
added before triage can proceed with complete coverage.

On-demand population is configured. The following analysis uses only the supplied
synthetic release and image evidence as required by the eval constraints.

## Supplied Release Evidence

| Field | Value |
|-------|-------|
| Product Version | 2.1.3 |
| Build | 0.3.15 |
| Build Date | 2026-07-01 |
| Backend source pin | `v0.3.15` |
| Release tag | `v0.3.15` |
| Resolved release commit SHA | `abcdef0123456789abcdef0123456789abcdef01` |

## Supplied Image Evidence

| Field | Value |
|-------|-------|
| Component | api-rhel10 |
| Image Reference | `registry.example.test/trustify/api:2.1.3-rhel10` |
| Image Digest | `sha256:cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc` |
| CPE | `cpe:2.3:a:example:trustify_api:2.1.3:*:*:*:*:*:*:*` |
| `org.opencontainers.image.revision` label | `fedcba9876543210fedcba9876543210fedcba98` |

## Revision Label Comparison

| Evidence Source | SHA Value |
|-----------------|-----------|
| Resolved release commit (from `v0.3.15` tag) | `abcdef0123456789abcdef0123456789abcdef01` |
| Image `org.opencontainers.image.revision` label | `fedcba9876543210fedcba9876543210fedcba98` |

**MISMATCH DETECTED.** The `org.opencontainers.image.revision` label on the published
`api-rhel10` image (`fedcba9876543210fedcba9876543210fedcba98`) does **not** match the
full commit SHA resolved from the `v0.3.15` release tag
(`abcdef0123456789abcdef0123456789abcdef01`). These two values must be identical for the
image to be considered a verified build of that release commit.

Per the on-demand population procedure (version-impact-analysis.md, Step 2.1), a
revision-label mismatch constitutes unresolved evidence. The affected image record
must be marked **UNRESOLVED -- NOT VERIFIED** and the engineer must supply corrected
evidence before the matrix can be written.

## Proposed Supportability Matrix Row (2.1.3)

If the revision mismatch is resolved, the following row would be added to the 2.1.x
stream's Supportability Matrix:

| Product Version | Build | Build Date | backend | Notes |
|-----------------|-------|------------|---------|-------|
| 2.1.0 | 0.3.8 | 2025-09-15 | `v0.3.8` | _(existing)_ |
| 2.1.1 | 0.3.12 | 2025-11-20 | `v0.3.12` | _(existing)_ |
| **2.1.3** | **0.3.15** | **2026-07-01** | **`v0.3.15`** | **new** |

## Proposed Container Images Row (2.1.3, api-rhel10)

**UNRESOLVED -- NOT VERIFIED**

| Product Version | Component | Konflux Release Tag | Resolved Release Commit SHA | Image Reference | Image Digest | CPE |
|-----------------|-----------|---------------------|-----------------------------|-----------------|--------------|-----|
| 2.1.3 | api-rhel10 | `v0.3.15` | `abcdef0123456789abcdef0123456789abcdef01` | `registry.example.test/trustify/api:2.1.3-rhel10` | `sha256:cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc` | `cpe:2.3:a:example:trustify_api:2.1.3:*:*:*:*:*:*:*` |

**Status: UNRESOLVED -- NOT VERIFIED**

The image revision label (`fedcba9876543210fedcba9876543210fedcba98`) does not match
the resolved release commit SHA (`abcdef0123456789abcdef0123456789abcdef01`). This
mismatch means either:

1. The image was built from a different commit than the one tagged `v0.3.15`, or
2. The release tag was moved after the image was built, or
3. The image's revision label was set incorrectly during the build process.

Until this discrepancy is resolved, the image record cannot be marked as verified and
the matrix cannot be updated.

## Decision: NOT WRITTEN

Because the `api-rhel10` image row has unresolved evidence (revision label mismatch),
the on-demand population procedure requires that:

1. The current `security-matrix.md` for the 2.1.x stream is **preserved unchanged**.
2. The `Last-Updated` timestamp (`2026-06-28T10:00:00Z`) remains **unchanged**.
3. **No part of this proposal is written** to the matrix file.
4. The proposal is labeled **NOT WRITTEN** pending corrected evidence.

## Action Required

Engineer: please provide corrected evidence for the `api-rhel10` image for product
version 2.1.3. Specifically, one of the following is needed:

1. **Corrected image reference** -- if the published image at
   `registry.example.test/trustify/api:2.1.3-rhel10` was built from a commit other
   than `v0.3.15`, provide the correct release tag and its resolved SHA.
2. **Corrected revision label** -- if the image was genuinely built from `v0.3.15`
   (SHA `abcdef0123456789abcdef0123456789abcdef01`), the
   `org.opencontainers.image.revision` label on the image needs to be corrected to
   match.
3. **Rebuild confirmation** -- if the image needs to be rebuilt from the correct
   commit, confirm once the rebuild is complete and provide the updated digest.

Once corrected evidence is provided and the revision label matches the resolved
release commit SHA, the matrix population can proceed and triage of TC-8001 can
continue with complete 2.1.x stream coverage.
