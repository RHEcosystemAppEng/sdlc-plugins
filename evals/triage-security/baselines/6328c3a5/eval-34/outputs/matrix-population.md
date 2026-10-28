# On-Demand Matrix Population Review — 2.1.x Stream

## Trigger

The 2.1.x stream's Supportability Matrix is incomplete. The current matrix contains
versions 2.1.0 and 2.1.1 but is missing the newly released version 2.1.3. On-demand
population was requested per Step 2.1 of the triage-security skill.

## Supplied Release Evidence for 2.1.3

| Field | Value |
|---|---|
| Product Version | 2.1.3 |
| Build | 0.3.15 |
| Build Date | 2026-07-01 |
| Backend Source Pin | `v0.3.15` |

## Proposed Supportability Matrix Row

| Product Version | Build | Build Date | backend | Notes |
|---|---|---|---|---|
| 2.1.3 | 0.3.15 | 2026-07-01 | `v0.3.15` | |

## Supplied Image Evidence for 2.1.3

| Field | Value |
|---|---|
| Component | api-rhel10 |
| Konflux Release Tag | `v0.3.15` |
| Resolved Release Commit SHA | `abcdef0123456789abcdef0123456789abcdef01` |
| Image Reference | `registry.example.test/trustify/api:2.1.3-rhel10` |
| Image Digest | `sha256:cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc` |
| CPE | `cpe:2.3:a:example:trustify_api:2.1.3:*:*:*:*:*:*:*` |

## Proposed Container Images Row

| Product Version | Component | Konflux Release Tag | Resolved Release Commit SHA | Image Reference | Image Digest | CPE |
|---|---|---|---|---|---|---|
| 2.1.3 | api-rhel10 | `v0.3.15` | `abcdef0123456789abcdef0123456789abcdef01` | `registry.example.test/trustify/api:2.1.3-rhel10` | `sha256:cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc` | `cpe:2.3:a:example:trustify_api:2.1.3:*:*:*:*:*:*:*` |

## Revision-Label Comparison

| Field | Value |
|---|---|
| Resolved release commit SHA (from tag `v0.3.15`) | `abcdef0123456789abcdef0123456789abcdef01` |
| `org.opencontainers.image.revision` label (from published image) | `fedcba9876543210fedcba9876543210fedcba98` |
| **Match?** | **NO — MISMATCH** |

The published image's `org.opencontainers.image.revision` label
(`fedcba9876543210fedcba9876543210fedcba98`) does **not** match the full commit SHA
resolved from the `v0.3.15` release tag
(`abcdef0123456789abcdef0123456789abcdef01`).

## Decision: UNRESOLVED — NOT VERIFIED

Per the on-demand population procedure (Step 2.1, item 4):

> Treat a missing release-tag resolution, image reference, digest, CPE, or revision
> label — and any revision-label mismatch — as unresolved evidence. Mark the affected
> image record **UNRESOLVED — NOT VERIFIED**, state which evidence is missing or
> conflicts, and ask the engineer for corrected evidence. Never infer or substitute
> either SHA, and never mark an unresolved image as verified.

The image record for `(2.1.3, api-rhel10)` is marked **UNRESOLVED — NOT VERIFIED**
because the `org.opencontainers.image.revision` label does not match the resolved
release commit SHA. This is a revision-label mismatch.

## Proposal Status: NOT WRITTEN

Per the on-demand population procedure (Step 2.1, item 6):

> If any image evidence is unresolved, keep the current matrix and its `Last-Updated`
> timestamp unchanged, label any displayed proposal **NOT WRITTEN**, and ask for
> corrected evidence. Do not write any part of the proposal while an image row is
> unresolved.

**The current security matrix for the 2.1.x stream is unchanged.** The `Last-Updated`
timestamp remains `2026-06-28T10:00:00Z`. No rows have been added to the
Supportability Matrix or Container Images table.

## Action Required

The engineer must provide corrected evidence to resolve the revision-label mismatch
before the matrix can be updated. Specifically:

1. **Verify the release tag resolution**: Confirm the correct full SHA that tag
   `v0.3.15` resolves to. Is `abcdef0123456789abcdef0123456789abcdef01` correct?

2. **Verify the image revision label**: Confirm what SHA the published image
   `registry.example.test/trustify/api:2.1.3-rhel10` was actually built from.
   The `org.opencontainers.image.revision` label reports
   `fedcba9876543210fedcba9876543210fedcba98`.

3. **Provide the corrected evidence**: Either:
   - The release tag resolution is wrong and should be
     `fedcba9876543210fedcba9876543210fedcba98`, or
   - The image was built from a different commit and the image reference/digest
     should be updated to point to an image built from the correct release commit, or
   - There is a legitimate reason for the discrepancy (e.g., the image was rebuilt
     from a different commit) — document the reason.

Once corrected evidence is supplied, the on-demand population can be re-run to add
the 2.1.3 row to both the Supportability Matrix and the Container Images table.
