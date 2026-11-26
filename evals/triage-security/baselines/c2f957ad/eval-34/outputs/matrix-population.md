# TC-8001: On-Demand Matrix Population Review (2.1.x stream)

**Skill:** `/sdlc-workflow:triage-security`. Procedure: `version-impact-analysis.md`, Step 2.1 "On-demand matrix population"
**Mode:** Interactive (no `FULLSEND_OUTPUT_DIR`). Only the synthetic release/image evidence in the task was used. No Jira MCP, `git show`, registry, or other external calls were made.
**Decision:** **NOT WRITTEN.** The 2.1.3 / api-rhel10 image record is **UNRESOLVED — NOT VERIFIED** because its OCI revision label does not match the resolved release SHA. The existing 2.1.x `security-matrix.md` and its `Last-Updated` timestamp stay exactly as they are.

---

## 1. Configuration and Snapshot

| Item | Value |
|---|---|
| Stream | 2.1.x |
| Konflux release repo | `git.example.com/rhtpa/rhtpa-release.0.3.z` (local: `/home/dev/repos/rhtpa-release.0.3.z`) |
| Source repository | rhtpa-backend (`backend` column) |
| Source snapshot | `security-matrix-mock.md`, Stream 1 section, as read (`Last-Updated: 2026-06-28T10:00:00Z`) |
| Staleness (Step 0.3) | 151 days old on 2026-11-26, which is over the 14-day threshold. The engineer chose to refresh by asking for on-demand population. |

### Coverage gaps found

| Gap | Detail |
|---|---|
| Missing released-version row | 2.1.3 (build 0.3.15, 2026-07-01, backend `v0.3.15`) is not in the Supportability Matrix |
| Missing `#### Container Images` section | The 2.1.x matrix has no Container Images table, which the canonical template (`docs/templates/security-matrix.template.md`) requires |
| Missing `(Product Version, Component)` pair | `(2.1.3, api-rhel10)`: evidence was supplied (see below) |
| Missing pairs for existing versions | `(2.1.0, *)` and `(2.1.1, *)`: no image evidence was supplied, so their components, digests, CPEs, and revision labels are unknown |

---

## 2. Supplied Evidence for (2.1.3, api-rhel10)

Each value is kept in its own field, as required.

| Field | Supplied value |
|---|---|
| Product Version | 2.1.3 |
| Build / Build Date | 0.3.15 / 2026-07-01 |
| Backend source pin | `v0.3.15` |
| Component | api-rhel10 |
| Konflux Release Tag | `v0.3.15` |
| Resolved Release Commit SHA (from tag) | `abcdef0123456789abcdef0123456789abcdef01` |
| Image Reference | `registry.example.test/trustify/api:2.1.3-rhel10` |
| Image Digest | `sha256:cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc` |
| CPE | `cpe:2.3:a:example:trustify_api:2.1.3:*:*:*:*:*:*:*` |
| `org.opencontainers.image.revision` label | `fedcba9876543210fedcba9876543210fedcba98` |

---

## 3. Revision-Label Comparison (separate from the Container Images table)

| Product Version | Component | Konflux Release Tag | Resolved Release Commit SHA | OCI `org.opencontainers.image.revision` | Match? | Status |
|---|---|---|---|---|---|---|
| 2.1.3 | api-rhel10 | `v0.3.15` | `abcdef0123456789abcdef0123456789abcdef01` | `fedcba9876543210fedcba9876543210fedcba98` | **NO (MISMATCH)** | **UNRESOLVED — NOT VERIFIED** |

**Conflict:** The full SHA resolved from release tag `v0.3.15` (`abcdef01…ef01`) does not equal the revision label on the published image (`fedcba98…ba98`). The two SHAs share no common prefix. There are three possible explanations:

- the image was built from a different commit than the tagged release,
- the tag was moved or re-pointed after the build, or
- the wrong image or digest was attributed to 2.1.3.

The supplied evidence cannot tell these apart. I have not picked either SHA, guessed between them, or substituted one for the other. Neither SHA is treated as authoritative.

### Other pairs

| Product Version | Component | Status | Missing evidence |
|---|---|---|---|
| 2.1.0 | (unknown) | **UNRESOLVED — NOT VERIFIED** | Component list, release-tag resolution, image reference, digest, CPE, revision label |
| 2.1.1 | (unknown) | **UNRESOLVED — NOT VERIFIED** | Component list, release-tag resolution, image reference, digest, CPE, revision label |
| 2.1.3 | other components besides api-rhel10 (if any) | **UNRESOLVED — NOT VERIFIED** | Confirmation of the full set of shipped image components for 2.1.3 |

---

## 4. Proposed Complete Matrix (2.1.x): **DRAFT, NOT WRITTEN**

> **NOT WRITTEN.** This draft is shown for review only. It must not be saved while any image row is unresolved. Existing supportability rows, the Source Pinning Method, Ecosystem Mappings, and Forward Pointer are kept as they are. Only additions are proposed. The 2.1.3 row is source-pin metadata copied from the supplied release evidence. It is **not** verified lock-file or image evidence.

```markdown
<!-- Last-Updated: 2026-06-28T10:00:00Z -->   <!-- unchanged: not updated, because nothing was written -->

# Stream 1: rhtpa-release.0.3.z (2.1.x stream)

## Version Stream

This Konflux release repo covers the **2.1.x** product version stream.

## Supportability Matrix

| Version | Build | Build Date | backend | Notes |
|---------|-------|------------|---------|-------|
| 2.1.0 | 0.3.8 | 2025-09-15 | `v0.3.8` | |
| 2.1.1 | 0.3.12 | 2025-11-20 | `v0.3.12` | |
| 2.1.3 | 0.3.15 | 2026-07-01 | `v0.3.15` | PROPOSED — image evidence UNRESOLVED (revision-label mismatch) |

#### Container Images

| Product Version | Component | Konflux Release Tag | Resolved Release Commit SHA | Image Reference | Image Digest | CPE |
|---|---|---|---|---|---|---|
| 2.1.3 | api-rhel10 | `v0.3.15` | `abcdef0123456789abcdef0123456789abcdef01` | `registry.example.test/trustify/api:2.1.3-rhel10` | `sha256:cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc` | `cpe:2.3:a:example:trustify_api:2.1.3:*:*:*:*:*:*:*` |
<!-- 2.1.3/api-rhel10: UNRESOLVED — NOT VERIFIED. OCI revision label
     fedcba9876543210fedcba9876543210fedcba98 != resolved release SHA
     abcdef0123456789abcdef0123456789abcdef01. -->
<!-- 2.1.0 and 2.1.1 image rows: UNRESOLVED — no evidence supplied; not filled. -->

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

The 2.2.x stream matrix is unaffected and is not part of this proposal.

---

## 5. Decision and Effect on Triage

1. **No write.** Under Step 2.1 item 6, a proposal with any unresolved image row must not be written, even in part. The current 2.1.x `security-matrix.md` stays exactly as read, and `Last-Updated` stays `2026-06-28T10:00:00Z`. The Local matrix write safety procedure (re-read and compare, create-if-absent) was not run because no write is permitted.
2. **Not used as version-impact evidence.** The 2.1.3 / api-rhel10 record is **not** authoritative for TC-8001's version impact analysis. 2.1.3 cannot be reported as affected or not affected from this evidence, and no lock file was read at either SHA. Until the conflict is resolved, 2.1.3 stays an open coverage gap in the version impact table and is not assumed to be a retag of any other version.
3. **No project files changed and no external tools called.** This review is the only output.

## 6. Corrected Evidence Needed from the Engineer

Please provide corrected, verifiable evidence for **2.1.3 / api-rhel10**:

1. Confirm what release tag `v0.3.15` resolves to in `rhtpa-release.0.3.z` (full SHA), and whether the tag has been moved.
2. Confirm the correct published image reference and immutable digest for 2.1.3 api-rhel10, and the `org.opencontainers.image.revision` label on **that** digest.
3. If the image really was built from `fedcba9876543210fedcba9876543210fedcba98`, explain how that commit relates to the 2.1.3 release (for example, a rebuild or a different source pin), so the Supportability Matrix source pin can be corrected.
4. Give the full list of image components shipped in 2.1.3, plus image evidence (component, release tag, resolved SHA, reference, digest, CPE, revision label) for 2.1.0 and 2.1.1, so the Container Images table can be completed.

Once every `(Product Version, Component)` row has matching revision-label and resolved-SHA evidence, I will present the complete proposal again for confirmation. Only then will I write it under Local matrix write safety and update `Last-Updated`.
