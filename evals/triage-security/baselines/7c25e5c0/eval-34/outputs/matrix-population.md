# On-Demand Matrix Population Review — 2.1.3 / api-rhel10

## Trigger

The on-demand population trigger fires because the configured 2.1.x matrix is incomplete for newly released product version 2.1.3. Version 2.1.3 does not appear in the existing Supportability Matrix (which only lists 2.1.0 and 2.1.1). The skill's explicit missing-pair trigger also fires for Container Images: even if a Container Images section existed, the required `(2.1.3, api-rhel10)` component pair is missing. Per the triage-security skill's version-impact-analysis.md § On-demand matrix population, any missing required `(Product Version, Component)` pair — even when the section and other rows already exist — triggers research and preparation of a complete update.

## Supplied Evidence

| Field | Value |
|---|---|
| Product Version | 2.1.3 |
| Build | 0.3.15 |
| Build Date | 2026-07-01 |
| Backend Source Pin | v0.3.15 |
| Release Tag | v0.3.15 |
| Resolved Release Commit SHA | `abcdef0123456789abcdef0123456789abcdef01` |
| Image Reference (api-rhel10) | `registry.example.test/trustify/api:2.1.3-rhel10` |
| Image Digest (api-rhel10) | `sha256:cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc` |
| CPE (api-rhel10) | `cpe:2.3:a:example:trustify_api:2.1.3:*:*:*:*:*:*:*` |
| OCI Revision Label (api-rhel10) | `fedcba9876543210fedcba9876543210fedcba98` |

## Revision-Label Comparison

| Component | Resolved Release SHA | OCI `org.opencontainers.image.revision` | Match? | Status |
|---|---|---|---|---|
| api-rhel10 | `abcdef0123456789abcdef0123456789abcdef01` | `fedcba9876543210fedcba9876543210fedcba98` | **NO — MISMATCH** | **UNRESOLVED — NOT VERIFIED** |

The v0.3.15 release tag resolves to full SHA `abcdef0123456789abcdef0123456789abcdef01`, but the published api-rhel10 image's `org.opencontainers.image.revision` label reports `fedcba9876543210fedcba9876543210fedcba98`. These values do not match. The image row cannot be marked as verified while this discrepancy exists.

## Proposed Matrix (NOT WRITTEN)

> **WARNING: This draft is NOT WRITTEN to any file.** The revision-label mismatch for 2.1.3/api-rhel10 remains unresolved. The existing matrix is unchanged and its `Last-Updated` timestamp is preserved. No write will occur while any image row is unresolved.

### Proposed Supportability Matrix (2.1.x stream)

| Version | Build | Build Date | backend | Notes |
|---------|-------|------------|---------|-------|
| 2.1.0 | 0.3.8 | 2025-09-15 | `v0.3.8` | |
| 2.1.1 | 0.3.12 | 2025-11-20 | `v0.3.12` | |
| 2.1.3 | 0.3.15 | 2026-07-01 | `v0.3.15` | **NEW — pending image verification** |

### Proposed Container Images (2.1.x stream)

| Product Version | Component | Konflux Release Tag | Resolved Release Commit SHA | Image Reference | Image Digest | CPE |
|---|---|---|---|---|---|---|
| 2.1.3 | api-rhel10 | `v0.3.15` | `abcdef0123456789abcdef0123456789abcdef01` | `registry.example.test/trustify/api:2.1.3-rhel10` | `sha256:cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc` | `cpe:2.3:a:example:trustify_api:2.1.3:*:*:*:*:*:*:*` |

**Row status: UNRESOLVED — NOT VERIFIED** (revision label mismatch — see comparison above)

### Preserved Sections (unchanged)

The following sections from the existing security-matrix-mock.md are preserved without modification:

- **Source Pinning Method**: `backend` → `artifacts.lock.yaml` (download URL contains tag)
- **Ecosystem Mappings**: Cargo (backend, Cargo.lock, release/0.3.z) and RPM (rpms.lock.yaml)
- **Forward Pointer**: Next stream: `2.2.x` at `git.example.com/rhtpa/rhtpa-release.0.4.z`
- **Existing Supportability Matrix rows**: 2.1.0 and 2.1.1 are preserved exactly as-is

## Shared Write-Safety Rule

Per version-impact-analysis.md § Local matrix write safety, the shared write-safety rule applies to **all** local `security-matrix.md` writes: saving a Konflux fallback copy, applying Step 2.1.1 format auto-repairs, and on-demand population writes. Before any write, the procedure requires:

1. Keeping the exact source contents as a snapshot
2. Re-reading the target immediately before writing and comparing with the snapshot
3. If the target changed, preserving the current file and merging only when the full current contents and all merge data are available
4. Never overwriting stale content

## Decision

**No write is performed.** The existing matrix remains unchanged.

The revision label (`fedcba9876543210fedcba9876543210fedcba98`) does not match the resolved release SHA (`abcdef0123456789abcdef0123456789abcdef01`) for the 2.1.3/api-rhel10 image. Per the on-demand population rules (version-impact-analysis.md § On-demand matrix population, item 4):

> "Treat a missing release-tag resolution, image reference, digest, CPE, or revision label — and any revision-label mismatch — as unresolved evidence. Mark the affected image record UNRESOLVED — NOT VERIFIED, state which evidence is missing or conflicts, and ask the engineer for corrected evidence. Never infer or substitute either SHA, and never mark an unresolved image as verified."

And per item 6:

> "If any image evidence is unresolved, keep the current matrix and its Last-Updated timestamp unchanged, label any displayed proposal NOT WRITTEN, and ask for corrected evidence."

**Action required:** Please provide corrected release/image evidence for 2.1.3/api-rhel10. Either:
1. The correct release tag SHA that matches the image revision label, or
2. An updated image with a revision label matching the v0.3.15 resolved SHA `abcdef0123456789abcdef0123456789abcdef01`

The proposed matrix above will not be written until the mismatch is resolved and all image rows are verified.
