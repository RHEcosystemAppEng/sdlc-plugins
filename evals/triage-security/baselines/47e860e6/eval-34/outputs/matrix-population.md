# TC-8001: On-Demand Matrix Population Review (2.1.x stream)

**Skill:** triage-security, Step 2.1 (On-demand matrix population). Steps 0.3 and 2.1.1 run first.
**Mode:** Interactive. `FULLSEND_OUTPUT_DIR` is not set, and this eval uses only the release and image evidence supplied in the task.
**Target matrix:** stream `2.1.x` (`git.example.com/rhtpa/rhtpa-release.0.3.z`)
**Decision:** **NOT WRITTEN.** The image evidence for 2.1.3 / api-rhel10 is **UNRESOLVED — NOT VERIFIED** because its revision label does not match the release commit SHA.

---

## 1. Pre-checks

### Step 0.3 Matrix staleness
- `<!-- Last-Updated: 2026-06-28T10:00:00Z -->`. Today is 2026-11-04, so the matrix is **129 days old**. That is well past the 14-day threshold.
- This is consistent with the gap the task describes: the configured 2.1.x matrix stops at 2.1.1 and has no row for the newly released 2.1.3.
- The engineer asked for on-demand population, which counts as the "Refresh now" option. The refresh follows the Step 2.1 on-demand population procedure below.

### Step 2.1.1 Format validation (2.1.x section)
- `## Supportability Matrix`, `### Source Pinning Method`, `## Ecosystem Mappings`, `## Forward Pointer` are all present.
- The Ecosystem Mappings columns match the template: `Ecosystem | Repository | Lock File | Check Command | Upstream Branch`.
- **Gap:** there is no `Container Images` section. On-demand population requires a Container Images row for every `(Product Version, Component)` pair. The existing 2.1.0 and 2.1.1 rows have no image records either.
- Note: the Supportability Matrix header uses `Version` where the template uses `Product Version`. These columns are product-specific, so this is not a validation failure. The existing header is kept as-is.

---

## 2. Gap analysis: required pairs vs. existing coverage

| Product Version | Supportability row | Container Images row(s) | Status |
|---|---|---|---|
| 2.1.0 | Present (`v0.3.8`) | Missing (no section) | Image evidence not supplied |
| 2.1.1 | Present (`v0.3.12`) | Missing (no section) | Image evidence not supplied |
| 2.1.3 | **Missing** | **Missing** (`api-rhel10`) | Evidence supplied, but unresolved (see below) |

(2.1.2 is not in the matrix and was not mentioned in the supplied evidence. I did not invent it. The engineer should confirm whether 2.1.2 was released or skipped.)

---

## 3. Collected evidence for 2.1.3 (as supplied, values kept distinct)

| Field | Value | Source |
|---|---|---|
| Product Version | 2.1.3 | Supplied release evidence |
| Build | 0.3.15 | Supplied release evidence |
| Build Date | 2026-07-01 | Supplied release evidence |
| backend source pin | `v0.3.15` | Supplied release evidence (artifacts.lock.yaml pinning method) |
| Component | api-rhel10 | Supplied image evidence |
| Konflux Release Tag | `v0.3.15` | Supplied release evidence |
| Resolved Release Commit SHA | `abcdef0123456789abcdef0123456789abcdef01` | Supplied tag resolution |
| Image Reference | `registry.example.test/trustify/api:2.1.3-rhel10` | Supplied image evidence |
| Image Digest | `sha256:cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc` | Supplied image evidence |
| CPE | `cpe:2.3:a:example:trustify_api:2.1.3:*:*:*:*:*:*:*` | Supplied image evidence |
| `org.opencontainers.image.revision` label | `fedcba9876543210fedcba9876543210fedcba98` | Supplied image evidence |

## 4. Revision-label comparison (reported separately from Container Images table)

| Product Version | Component | Resolved Release Commit SHA (from `v0.3.15`) | Image `org.opencontainers.image.revision` | Result |
|---|---|---|---|---|
| 2.1.3 | api-rhel10 | `abcdef0123456789abcdef0123456789abcdef01` | `fedcba9876543210fedcba9876543210fedcba98` | **MISMATCH: UNRESOLVED — NOT VERIFIED** |

The published image's revision label does not equal the full SHA that the `v0.3.15` release tag resolves to. So there is no proof that this image was built from the release commit. Either the image was built from a different commit, the tag was moved, or one of the two values is wrong. Neither SHA was inferred or replaced with the other.

---

## 5. Proposed 2.1.x matrix: **NOT WRITTEN** (display only)

> **NOT WRITTEN.** This proposal is for review only. The current
> `security-matrix.md` and its `Last-Updated: 2026-06-28T10:00:00Z` timestamp stay
> **unchanged** while any image row is unresolved.

```markdown
<!-- Last-Updated: 2026-06-28T10:00:00Z -->   (unchanged; would only be bumped after a permitted write)

# Stream 1: rhtpa-release.0.3.z (2.1.x stream)

## Version Stream

This Konflux release repo covers the **2.1.x** product version stream.

## Supportability Matrix

| Version | Build | Build Date | backend | Notes |
|---------|-------|------------|---------|-------|
| 2.1.0 | 0.3.8 | 2025-09-15 | `v0.3.8` | |
| 2.1.1 | 0.3.12 | 2025-11-20 | `v0.3.12` | |
| 2.1.3 | 0.3.15 | 2026-07-01 | `v0.3.15` | PROPOSED: image evidence UNRESOLVED — NOT VERIFIED |

#### Container Images

| Product Version | Component | Konflux Release Tag | Resolved Release Commit SHA | Image Reference | Image Digest | CPE |
|---|---|---|---|---|---|---|
| 2.1.3 | api-rhel10 | `v0.3.15` | `abcdef0123456789abcdef0123456789abcdef01` | `registry.example.test/trustify/api:2.1.3-rhel10` | `sha256:cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc` | `cpe:2.3:a:example:trustify_api:2.1.3:*:*:*:*:*:*:*` |

<!-- 2.1.3 / api-rhel10: UNRESOLVED — NOT VERIFIED (revision label fedcba98... != release SHA abcdef01...) -->
<!-- 2.1.0 and 2.1.1 image rows: evidence not supplied; must be researched before a complete write -->

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

Existing rows, Source Pinning Method, Ecosystem Mappings, and Forward Pointer are kept unchanged. Nothing existing is replaced with partial data. The 2.2.x stream is out of scope for this population and is not touched.

---

## 6. Decision

- **Write status: NOT WRITTEN.** None of the proposal is written, not even the 2.1.3 supportability row on its own. While any image row is unresolved, the procedure forbids writing any part of the proposal.
- **`Last-Updated`: unchanged** (`2026-06-28T10:00:00Z`).
- **Local matrix write safety:** never reached. No snapshot re-read/compare or create-if-absent write was attempted. The proposal's source snapshot is the current matrix content as read (Last-Updated 2026-06-28T10:00:00Z, rows 2.1.0 and 2.1.1).
- **No external calls were made:** no Jira MCP, `git show`, registry API, or cosign.

### Engineer action required (corrected evidence requested)
1. **Resolve the revision mismatch for 2.1.3 / api-rhel10.** Provide one of the following:
   - the correct image (reference plus digest) whose `org.opencontainers.image.revision` equals `abcdef0123456789abcdef0123456789abcdef01`, **or**
   - confirmation that `v0.3.15` actually resolves to `fedcba9876543210fedcba9876543210fedcba98`, meaning the tag resolution was wrong. This would need to come from a corrected tag resolution, not an assumption.
2. **Confirm the full component list for 2.1.3.** Are there other shipped images (for example, other platform variants) that need their own `(2.1.3, Component)` rows?
3. **Provide image evidence for 2.1.0 and 2.1.1.** Each needs release tag, resolved SHA, image reference, digest, CPE, and revision label, so the Container Images section is complete.
4. **Confirm the status of 2.1.2.** Was it released or skipped?

Once all image rows are verified, I will show the complete proposal again for confirmation. After you confirm, it will be written under Local matrix write safety, and `Last-Updated` will be bumped only after the write succeeds.

### Impact on TC-8001 triage
- 2.1.3 cannot be used as verified version-impact evidence yet. Its source pin (`v0.3.15`) has no matching verified image, and the mock lock-file data has no `v0.3.15` entries. In the version impact table, 2.1.3 must be shown as **UNRESOLVED (matrix not verified)**. It must not be marked as affected or unaffected by assumption.
- Triage of TC-8001 for the 2.1.x stream stays blocked on 2.1.3 until the corrected evidence arrives. No Jira mutations (Affects Versions, remediation tasks, closure) are proposed based on unverified 2.1.3 data.
