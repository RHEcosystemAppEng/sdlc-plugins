# TC-8001 — On-Demand Matrix Population Review (2.1.x stream)

**Decision: NOT WRITTEN — UNRESOLVED — NOT VERIFIED.**
The `(2.1.3, api-rhel10)` image record has a revision-label mismatch, so no part of this proposal may be written. The current 2.1.x `security-matrix.md` and its `<!-- Last-Updated: 2026-06-28T10:00:00Z -->` timestamp stay as they are. Corrected evidence is needed before anything can be written.

Scope: interactive on-demand population (Step 2.1, "On-demand matrix population"), using only the synthetic release and image evidence supplied in the task. No Jira MCP, `git show`, registry API, or other external call was made. No project file was changed. The only file written is this one.

---

## 1. Source snapshot (current 2.1.x matrix, as read)

Stream: `2.1.x`. Konflux release repo: `git.example.com/rhtpa/rhtpa-release.0.3.z`. Local path: `/home/dev/repos/rhtpa-release.0.3.z`.

- `Last-Updated: 2026-06-28T10:00:00Z`
- Supportability Matrix rows: 2.1.0 (0.3.8, 2025-09-15, `v0.3.8`) and 2.1.1 (0.3.12, 2025-11-20, `v0.3.12`)
- `#### Container Images` section: **absent**
- Source Pinning Method: backend uses `artifacts.lock.yaml`
- Ecosystem Mappings: Cargo/backend/`Cargo.lock`/`release/0.3.z`, and RPM/—/`rpms.lock.yaml`
- Forward Pointer: `2.2.x` at `git.example.com/rhtpa/rhtpa-release.0.4.z`

This snapshot is kept as the source for the proposal. Any later write would first need to re-read the file and compare it against this snapshot, as Local matrix write safety requires.

## 2. Coverage gaps found

| Gap | Detail |
|---|---|
| Missing released-version row | 2.1.3 was released (build 0.3.15, 2026-07-01) but has no Supportability Matrix row |
| Missing Container Images section | The stream has no `#### Container Images` table |
| Missing component pair | `(2.1.3, api-rhel10)` |
| Missing component pairs (no evidence supplied) | Container Images pairs for 2.1.0 and 2.1.1 are also absent. No image evidence was supplied for them, so no rows are proposed. Engineer input is needed. |
| 2.1.2 | The supplied evidence does not mention 2.1.2. Nothing is inferred for it. Please confirm whether 2.1.2 was released, and if so, supply its evidence. |

## 3. Image evidence and revision-label comparison

| Field | Value |
|---|---|
| Product Version | 2.1.3 |
| Component | api-rhel10 |
| Konflux Release Tag | `v0.3.15` |
| Resolved Release Commit SHA (from tag) | `abcdef0123456789abcdef0123456789abcdef01` |
| Image Reference | `registry.example.test/trustify/api:2.1.3-rhel10` |
| Image Digest | `sha256:cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc` |
| CPE | `cpe:2.3:a:example:trustify_api:2.1.3:*:*:*:*:*:*:*` |
| `org.opencontainers.image.revision` label | `fedcba9876543210fedcba9876543210fedcba98` |

**Revision-label comparison (reported separately from the Container Images table):**

| (Product Version, Component) | Resolved release SHA (`v0.3.15`) | Image revision label | Result |
|---|---|---|---|
| (2.1.3, api-rhel10) | `abcdef0123456789abcdef0123456789abcdef01` | `fedcba9876543210fedcba9876543210fedcba98` | **MISMATCH — UNRESOLVED — NOT VERIFIED** |

The published image's revision label points to a different commit than the one the `v0.3.15` release tag resolves to. Two explanations are possible:

- The image was built from a different commit than the release tag.
- The tag resolution is wrong, or the tag was moved.

Neither SHA has been substituted for the other or inferred. Both are recorded exactly as supplied. The record is **not** marked verified.

## 4. Proposed matrix (for review only — NOT WRITTEN)

> **NOT WRITTEN.** This is shown for engineer review only. It will not be written while the `(2.1.3, api-rhel10)` image record is unresolved. Existing source columns, Source Pinning Method, Ecosystem Mappings, and Forward Pointer are kept unchanged. Existing rows are not replaced.

```markdown
<!-- Last-Updated: 2026-06-28T10:00:00Z -->   (unchanged — would only be updated after a permitted write succeeds)

## Supportability Matrix

| Version | Build | Build Date | backend | Notes |
|---------|-------|------------|---------|-------|
| 2.1.0 | 0.3.8 | 2025-09-15 | `v0.3.8` | |
| 2.1.1 | 0.3.12 | 2025-11-20 | `v0.3.12` | |
| 2.1.3 | 0.3.15 | 2026-07-01 | `v0.3.15` | PROPOSED — image evidence UNRESOLVED |

#### Container Images

| Product Version | Component | Konflux Release Tag | Resolved Release Commit SHA | Image Reference | Image Digest | CPE |
|---|---|---|---|---|---|---|
| 2.1.3 | api-rhel10 | `v0.3.15` | `abcdef0123456789abcdef0123456789abcdef01` | `registry.example.test/trustify/api:2.1.3-rhel10` | `sha256:cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc` | `cpe:2.3:a:example:trustify_api:2.1.3:*:*:*:*:*:*:*` |

<!-- (2.1.3, api-rhel10): UNRESOLVED — NOT VERIFIED — image revision label fedcba98… ≠ release SHA abcdef01… -->
<!-- 2.1.0 / 2.1.1 Container Images rows: no evidence supplied — not proposed -->

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

## 5. Decision

- **Write status:** NOT WRITTEN. No change to the 2.1.x `security-matrix.md`. `Last-Updated` stays `2026-06-28T10:00:00Z`.
- **Reason:** In the `(2.1.3, api-rhel10)` record, the image's `org.opencontainers.image.revision` (`fedcba9876543210fedcba9876543210fedcba98`) does not match the full SHA that `v0.3.15` resolves to (`abcdef0123456789abcdef0123456789abcdef01`). A revision-label mismatch counts as unresolved evidence. No part of the proposal may be written while any image row is unresolved.
- **Triage impact:** 2.1.3 cannot be treated as matrix-verified for TC-8001's version-impact analysis. Do not use the `v0.3.15` lock data or this image as verified evidence for 2.1.3 until the mismatch is resolved.

## 6. Corrected evidence requested from the engineer

1. Confirm the commit that the `v0.3.15` release tag resolves to. Check whether the tag was moved or re-created.
2. Confirm which commit the published `registry.example.test/trustify/api:2.1.3-rhel10@sha256:cccc…cccc` image was actually built from. Either supply a corrected image (reference, digest, and CPE) whose revision label equals the release SHA, or supply corrected release-tag or pin evidence.
3. Supply image evidence (component, tag, resolved SHA, reference, digest, CPE, and revision label) for every shipped component of 2.1.0 and 2.1.1. Also cover any other 2.1.3 components, for example other platform variants.
4. Confirm whether a 2.1.2 release exists.

After all image rows are verified, the complete proposal will be shown again for confirmation. It will then be written only by following Local matrix write safety: re-read and compare against the snapshot, then merge or abort. `Last-Updated` is updated only after that write succeeds.
