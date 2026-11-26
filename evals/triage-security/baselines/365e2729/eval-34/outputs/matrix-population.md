# TC-8001 — On-Demand Matrix Population Review (2.1.x stream)

**Status: PROPOSAL — NOT WRITTEN**
**Decision: BLOCKED — image evidence UNRESOLVED — NOT VERIFIED. No matrix write performed.**

Procedure followed: triage-security `version-impact-analysis.md` → Step 2.1 "On-demand matrix
population" and "Local matrix write safety"; Container Images fields from
`docs/templates/security-matrix.template.md`. Interactive mode (not Fullsend). Only the supplied
synthetic evidence was used. No Jira MCP, `git show`, registry API, or other external calls were made.

## 1. Source snapshot (current matrix, kept unchanged)

- Stream: **2.1.x**, Konflux release repo `git.example.com/rhtpa/rhtpa-release.0.3.z`
- `<!-- Last-Updated: 2026-06-28T10:00:00Z -->`. This is 151 days old on 2026-11-26, which exceeds
  the 14-day staleness threshold in Step 0.3. Refreshing the matrix is the reason for this population run.
- Existing Supportability Matrix rows: 2.1.0 (`v0.3.8`) and 2.1.1 (`v0.3.12`).
- **Gap 1:** released version **2.1.3** has no row.
- **Gap 2:** the `#### Container Images` section is missing, so no `(Product Version, Component)`
  pair exists for any version.
- Ecosystem Mappings (Cargo/backend `release/0.3.z`, RPM), Source Pinning Method (`artifacts.lock.yaml`)
  and Forward Pointer (`2.2.x` at `rhtpa-release.0.4.z`) are present. They are preserved as they are.

## 2. Supplied release/image evidence (values kept separate)

| Evidence item | Value |
|---|---|
| Product version | 2.1.3 |
| Build / Build date | 0.3.15 / 2026-07-01 |
| backend source pin | `v0.3.15` |
| Konflux release tag | `v0.3.15` |
| Resolved release commit SHA (from tag) | `abcdef0123456789abcdef0123456789abcdef01` |
| Component | api-rhel10 |
| Published image reference | `registry.example.test/trustify/api:2.1.3-rhel10` |
| Image digest | `sha256:cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc` |
| CPE | `cpe:2.3:a:example:trustify_api:2.1.3:*:*:*:*:*:*:*` |
| Image `org.opencontainers.image.revision` label | `fedcba9876543210fedcba9876543210fedcba98` |

## 3. Revision-label comparison (reported separately from the Container Images table)

| Product Version | Component | Resolved Release Commit SHA (tag `v0.3.15`) | Image revision label | Result |
|---|---|---|---|---|
| 2.1.3 | api-rhel10 | `abcdef0123456789abcdef0123456789abcdef01` | `fedcba9876543210fedcba9876543210fedcba98` | **MISMATCH — UNRESOLVED — NOT VERIFIED** |

The published image's revision label does not match the commit that the `v0.3.15` release tag
resolves to. So we cannot show that the image at this digest was built from the pinned release
source. Neither SHA was substituted for the other, and neither value was inferred or "corrected".

## 4. Proposed complete matrix (2.1.x). DISPLAY ONLY, NOT WRITTEN

```markdown
<!-- Last-Updated: 2026-06-28T10:00:00Z -->   <!-- unchanged: no write performed -->

# Stream 1: rhtpa-release.0.3.z (2.1.x stream)

## Version Stream

This Konflux release repo covers the **2.1.x** product version stream.

## Supportability Matrix

| Version | Build | Build Date | backend | Notes |
|---------|-------|------------|---------|-------|
| 2.1.0 | 0.3.8 | 2025-09-15 | `v0.3.8` | |
| 2.1.1 | 0.3.12 | 2025-11-20 | `v0.3.12` | |
| 2.1.3 | 0.3.15 | 2026-07-01 | `v0.3.15` | PROPOSED, NOT WRITTEN (image evidence unresolved) |

#### Container Images

| Product Version | Component | Konflux Release Tag | Resolved Release Commit SHA | Image Reference | Image Digest | CPE |
|---|---|---|---|---|---|---|
| 2.1.3 | api-rhel10 | `v0.3.15` | `abcdef0123456789abcdef0123456789abcdef01` | `registry.example.test/trustify/api:2.1.3-rhel10` | `sha256:cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc` | `cpe:2.3:a:example:trustify_api:2.1.3:*:*:*:*:*:*:*` |

<!-- 2.1.3 / api-rhel10: UNRESOLVED — NOT VERIFIED (revision label fedcba98... != release SHA abcdef01...) -->
<!-- 2.1.0, 2.1.1: Container Images rows not proposed — no image evidence supplied (UNRESOLVED) -->

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

- **No 2.1.2 evidence.** The stream goes from 2.1.1 to 2.1.3. Please confirm whether 2.1.2 was
  released (and if so, give its build, date, pin and images) or whether it was skipped. No row
  was invented.
- **Image records for 2.1.0, 2.1.1 and other 2.1.3 components.** No image evidence was supplied
  for 2.1.0 or 2.1.1. The only 2.1.3 component supplied is api-rhel10. Please confirm the full
  list of shipped components per version (for example, other platform variants). Each
  `(Product Version, Component)` pair needs its own row.
- **No Cargo.lock data for `v0.3.15`.** The mock lock data has none, so version impact for 2.1.3
  cannot be checked yet, even after the matrix gap is closed.

## 6. Decision

1. **Matrix write: NOT PERFORMED.** One image record is UNRESOLVED (revision-label mismatch). The
   procedure therefore keeps the current matrix and its `Last-Updated` timestamp (`2026-06-28T10:00:00Z`)
   unchanged and writes no part of the proposal. That includes the 2.1.3 Supportability Matrix row,
   even though its build and pin evidence is consistent. Local matrix write safety (re-read,
   compare, create-if-absent or merge-or-abort) was not reached.
2. **Do not treat 2.1.3 as verified** in version-impact analysis for TC-8001 until the evidence is fixed.
3. **Engineer action requested:** please supply corrected evidence for 2.1.3 / api-rhel10. Either:
   - (a) confirm the correct release tag/commit, if `v0.3.15` was re-pointed or the wrong tag was
     given, so that it resolves to `fedcba9876543210fedcba9876543210fedcba98`; or
   - (b) give the digest/reference of the image actually built from
     `abcdef0123456789abcdef0123456789abcdef01`; or
   - (c) explain the provenance of the mismatch (for example, a rebuild from a different commit).

   Also supply the image evidence for 2.1.0, 2.1.1 and any other 2.1.3 components, and confirm
   the 2.1.2 status.
4. Once every image row is verified, present the full proposal again for confirmation. Then write
   it only under Local matrix write safety, and update `Last-Updated` only after the write succeeds.
