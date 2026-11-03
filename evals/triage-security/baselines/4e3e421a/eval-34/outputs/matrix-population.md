# TC-8001 — On-Demand Matrix Population Review (2.1.x stream)

**Status: PROPOSAL — NOT WRITTEN.** One or more image records are **UNRESOLVED — NOT VERIFIED**.
The current 2.1.x `security-matrix.md` and its `Last-Updated` timestamp (`2026-06-28T10:00:00Z`) remain unchanged.

Procedure followed: `triage-security` Step 2.1 → *On-demand matrix population*
(`version-impact-analysis.md`), interactive mode. Evidence source: only the synthetic
release/image evidence supplied with the task. No Jira MCP, `git show`, registry API, or
other external call was made. No project file was modified.

## 1. Gap detection

Stream `2.1.x` (Konflux repo `git.example.com/rhtpa/rhtpa-release.0.3.z`), source snapshot =
the 2.1.x section of `security-matrix-mock.md` as read (Last-Updated `2026-06-28T10:00:00Z`).

| Gap | Detail |
|---|---|
| Missing released-version row | `2.1.3` (build 0.3.15, released 2026-07-01 — after the matrix's Last-Updated) is absent from the Supportability Matrix. |
| Missing section | `#### Container Images` section does not exist in the 2.1.x matrix. |
| Missing `(Product Version, Component)` pairs | `(2.1.3, api-rhel10)` — evidence supplied. `(2.1.0, *)` and `(2.1.1, *)` — no image evidence supplied; components unknown. |

Template format check (2.1.1): required headings `## Supportability Matrix`, `## Ecosystem Mappings`,
`### Source Pinning Method`, `## Forward Pointer` are present; Ecosystem Mappings columns match the
template. Pass (no auto-repair needed). The missing Container Images section is handled by population.

## 2. Supplied evidence for 2.1.3

| Field | Value |
|---|---|
| Product Version | 2.1.3 |
| Build | 0.3.15 |
| Build Date | 2026-07-01 |
| backend source pin | `v0.3.15` (artifacts.lock.yaml method, unchanged) |
| Konflux Release Tag | `v0.3.15` |
| Resolved Release Commit SHA (from tag) | `abcdef0123456789abcdef0123456789abcdef01` |
| Component | `api-rhel10` |
| Image Reference | `registry.example.test/trustify/api:2.1.3-rhel10` |
| Image Digest | `sha256:cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc` |
| CPE | `cpe:2.3:a:example:trustify_api:2.1.3:*:*:*:*:*:*:*` |
| Image `org.opencontainers.image.revision` label | `fedcba9876543210fedcba9876543210fedcba98` |

## 3. Revision-label comparison (reported separately from the Container Images table)

| Product Version | Component | Resolved Release Commit SHA (tag `v0.3.15`) | Image revision label | Result |
|---|---|---|---|---|
| 2.1.3 | api-rhel10 | `abcdef0123456789abcdef0123456789abcdef01` | `fedcba9876543210fedcba9876543210fedcba98` | **MISMATCH — UNRESOLVED — NOT VERIFIED** |

The published image claims to be built from a commit different from the one the `v0.3.15` release
tag resolves to. Neither SHA is inferred, substituted, or preferred: the release-tag SHA is kept in
the Resolved Release Commit SHA column exactly as resolved, and the label value is recorded only here.
It is therefore not established that the shipped `api-rhel10` image contains the `v0.3.15` lock-file
contents, so 2.1.3 cannot be used as verified evidence for version impact analysis.

## 4. Proposed 2.1.x matrix (complete) — NOT WRITTEN

<!-- Last-Updated: 2026-06-28T10:00:00Z  (unchanged — proposal not written) -->

```markdown
# Stream 1: rhtpa-release.0.3.z (2.1.x stream)

## Version Stream

This Konflux release repo covers the **2.1.x** product version stream.

## Supportability Matrix

| Version | Build | Build Date | backend | Notes |
|---------|-------|------------|---------|-------|
| 2.1.0 | 0.3.8 | 2025-09-15 | `v0.3.8` | |
| 2.1.1 | 0.3.12 | 2025-11-20 | `v0.3.12` | |
| 2.1.3 | 0.3.15 | 2026-07-01 | `v0.3.15` | UNRESOLVED — NOT VERIFIED: api-rhel10 image revision label mismatch |

#### Container Images

| Product Version | Component | Konflux Release Tag | Resolved Release Commit SHA | Image Reference | Image Digest | CPE |
|---|---|---|---|---|---|---|
| 2.1.3 | api-rhel10 | `v0.3.15` | `abcdef0123456789abcdef0123456789abcdef01` | `registry.example.test/trustify/api:2.1.3-rhel10` | `sha256:cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc` | `cpe:2.3:a:example:trustify_api:2.1.3:*:*:*:*:*:*:*` |

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

Image record status:

| Product Version | Component | Status | Reason |
|---|---|---|---|
| 2.1.3 | api-rhel10 | **UNRESOLVED — NOT VERIFIED** | `org.opencontainers.image.revision` (`fedcba98…fedcba98`) ≠ tag-resolved SHA (`abcdef01…abcdef01`) |
| 2.1.0 | (unknown components) | **UNRESOLVED — NOT VERIFIED** | No release-tag resolution, image reference, digest, CPE, or revision label supplied |
| 2.1.1 | (unknown components) | **UNRESOLVED — NOT VERIFIED** | No release-tag resolution, image reference, digest, CPE, or revision label supplied |

Preservation: existing Supportability Matrix rows (2.1.0, 2.1.1), the `backend` source column,
Source Pinning Method, Ecosystem Mappings, and Forward Pointer are kept verbatim; nothing is
replaced with partial release data. Note: no 2.1.2 release was included in the supplied
evidence; if one exists, its row is also needed.

## 5. Decision

- **Do not write.** Because at least one image record is unresolved (revision-label mismatch for
  `(2.1.3, api-rhel10)`, plus missing image evidence for 2.1.0/2.1.1), no part of this proposal is
  written. The local 2.1.x `security-matrix.md` is left exactly as-is, and `Last-Updated` is not bumped.
- No Local-matrix-write-safety re-read/compare is performed, since no write is permitted.
- Triage of TC-8001 must not treat 2.1.3 as verified matrix coverage; 2.1.3 impact remains
  **unverified** until corrected evidence is provided.

## 6. Request to engineer — corrected evidence needed

1. For `(2.1.3, api-rhel10)`: confirm which commit the published image was actually built from.
   Either (a) supply the correct published image (reference + digest + CPE) whose
   `org.opencontainers.image.revision` equals `abcdef0123456789abcdef0123456789abcdef01`, or
   (b) confirm the correct release tag/SHA if `v0.3.15` → `abcdef01…` is wrong (e.g., re-tag), or
   (c) explain the `fedcba98…` commit (e.g., rebuild from a different commit) so the source pin can be corrected.
2. Confirm the full list of shipped image components for 2.1.3 (only `api-rhel10` was supplied —
   are there other platforms/components such as rhel9 variants?).
3. Provide image evidence (component, release tag + resolved SHA, image reference, digest, CPE,
   revision label) for 2.1.0 and 2.1.1, and confirm whether a 2.1.2 release exists.

Once all image records verify, the complete proposal will be re-presented for confirmation and
written only via Local matrix write safety (re-read/compare against the snapshot above, merge-or-abort),
after which `Last-Updated` will be updated.
