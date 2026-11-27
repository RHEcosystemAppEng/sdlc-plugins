# Security Matrix Review — 2.1.x Stream (Proposal, NOT written)

Status: **Awaiting user review — write BLOCKED by an unresolved image revision mismatch (2.1.1 / api-rhel10).**

No project file has been created or modified. `security-matrix.md` remains absent.

## Context

- Configured stream: `2.1.x`
  - Konflux Release Repo: `git.downstream.example.com/my-org/product-release.2.1.z`
  - Local Path: `/home/user/product-release.2.1.z`
  - Security Matrix Path: `security-matrix.md`
- Configured Source Repositories: `backend`, `frontend-ui`
- Step 10.5 existence check: `security-matrix.md` **missing** (simulated) → user confirmed scaffolding.
- Scaffold source: **`docs/templates/security-matrix.template.md` (plugin root) — the sole canonical scaffold.**
  `docs/templates/security-matrix.md` is a worked example only and was NOT used as a template or fallback.
- Template expansion: `{source-repo-name}` / `{source-ref}` and their matching separator cells were expanded in
  lockstep into one column per configured source repository (`backend`, `frontend-ui`), and one Source Pinning
  Method entry per repository. Fixed columns, the Container Images table, Ecosystem Mappings, and Forward Pointer
  sections are retained from the template.
- Step 10.6: user asked to populate from the supplied evidence (`security-matrix-image-identity.md`).
- Source snapshot of target at proposal time: **absent** (no prior contents). At write time the target must still
  be absent and will be created with create-if-absent semantics; if it has appeared, it will not be overwritten.

## Revision Checks (`org.opencontainers.image.revision` vs. SHA resolved from Konflux release tag)

| Product Version | Component | Konflux Release Tag | Resolved Release Commit SHA | Published Revision Label | Result |
|---|---|---|---|---|---|
| 2.1.0 | api-rhel9 | `v0.3.12` | `0123456789abcdef0123456789abcdef01234567` | `0123456789abcdef0123456789abcdef01234567` | MATCH — verified |
| 2.1.0 | api-rhel10 | `v0.3.12` | `0123456789abcdef0123456789abcdef01234567` | `0123456789abcdef0123456789abcdef01234567` | MATCH — verified |
| 2.1.1 | api-rhel10 | `v0.3.13` | `89abcdef0123456789abcdef0123456789abcdef` | `fedcba9876543210fedcba9876543210fedcba98` | **MISMATCH — BLOCKED / unresolved** |

### Blocked: 2.1.1 / api-rhel10

The published image `registry.example.test/trustify/api:2.1.1-rhel10`
(`sha256:cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc`) carries revision label
`fedcba9876543210fedcba9876543210fedcba98`, but tag `v0.3.13` resolves to
`89abcdef0123456789abcdef0123456789abcdef`. This is **not** a verified mapping and is **not** included in the
proposed Container Images table below.

Corrected evidence requested from the user (any one of):
1. The correct published image/digest for 2.1.1 api-rhel10 whose revision label equals `89abcdef0123456789abcdef0123456789abcdef`; or
2. Corrected release-tag resolution showing which tag/commit 2.1.1 api-rhel10 was actually built from; or
3. Confirmation that the image was rebuilt/retagged, with evidence reconciling the two SHAs.

Per Step 10.6, the matrix stays unchanged (not written) until this is verified.

### Other gaps (asking rather than inferring)

- **2.1.1 / api-rhel9**: no release-tag or published-image evidence was supplied. No row is proposed; please
  supply evidence if a 2.1.1 rhel9 image was shipped, or confirm none exists.
- **Forward Pointer**: only one stream (`2.1.x`) is configured; please confirm whether this should be `None`
  (latest stream) or point to a next stream (name + Konflux release repo).
- **frontend-ui `deadbeef` for 2.1.1**: taken as-is from the supplied supportability evidence; no retag note was
  supplied, so the Notes cell is left blank.

## Complete Proposed Matrix (`security-matrix.md`)

The block below is the full file that would be written once the user confirms and the mismatch above is resolved
(or the user explicitly confirms writing without the blocked row). The first line timestamp will be set to the
current UTC time only at the moment of the actual write.

````markdown
<!-- Last-Updated: <set to current UTC ISO-8601 time at write> -->
# Security Matrix — 2.1.x Stream

<!-- Canonical template for security matrix files. Copy this file to the path
     specified in your Security Configuration's Version Streams table
     (e.g., docs/security-matrix-2.2.x.md) and replace placeholders with
     concrete values. The triage-security skill validates existing matrices
     against this structure. -->

## Version Stream

<!-- Identifies which product version stream this matrix covers. -->

This Konflux release repo covers the **2.1.x** product version stream.

## Supportability Matrix

<!-- One row per product version built from this release stream. Expand
     {source-repo-name} and its matching separator/value cells in lockstep into
     one column per repository in Security Configuration > Source Repositories.
     Each source column contains that repository's tag or commit pinned in Konflux. -->

| Product Version | Build | Build Date | backend | frontend-ui | Notes |
|---|---|---|---|---|---|
| 2.1.0 | 0.3.12 | 2026-06-15 | `v0.3.12` | `bb447eeb` | |
| 2.1.1 | 0.3.13 | 2026-06-20 | `v0.3.13` | `deadbeef` | |

#### Container Images

<!-- Add one row for every unique product-version/component pair. Keep the
     Konflux release tag, the full commit SHA resolved from that tag, the
     published image reference, and the immutable OCI image digest distinct.
     The published image's org.opencontainers.image.revision label must equal
     the resolved release commit SHA. Do not mark an image row verified when
     evidence is missing or those values do not match. -->

| Product Version | Component | Konflux Release Tag | Resolved Release Commit SHA | Image Reference | Image Digest | CPE |
|---|---|---|---|---|---|---|
| 2.1.0 | api-rhel9 | `v0.3.12` | `0123456789abcdef0123456789abcdef01234567` | `registry.example.test/trustify/api:2.1.0-rhel9` | `sha256:aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa` | `cpe:2.3:a:example:trustify_api:2.1.0:*:*:*:*:*:*:*` |
| 2.1.0 | api-rhel10 | `v0.3.12` | `0123456789abcdef0123456789abcdef01234567` | `registry.example.test/trustify/api:2.1.0-rhel10` | `sha256:bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb` | `cpe:2.3:a:example:trustify_api:2.1.0:*:*:*:*:*:*:*` |

### Source Pinning Method

<!-- Repeat one entry per configured Source Repositories row, using the same
     repository short name. Describe how its commit or tag is pinned in Konflux;
     common methods include git submodules, artifacts.lock.yaml, or build-config tags. -->

- **backend**: `artifacts.lock.yaml` download URL contains the release tag
- **frontend-ui**: Git submodule at `components/frontend-ui`

## Ecosystem Mappings

<!-- One row per tracked ecosystem:
     - Repository: configured short name, or — when not applicable
     - Lock File: file name within that repository, blank when none exists
     - Check Command: inspect a dependency at the pinned ref (e.g., git show
       <commit>:<lock-file>)
     - Upstream Branch: branch used to check whether a fix is available upstream
     triage-security uses these mappings for released-version and fix checks. -->

| Ecosystem | Repository | Lock File | Check Command | Upstream Branch |
|---|---|---|---|---|
| Cargo | backend | `Cargo.lock` | `git show <tag>:Cargo.lock` | `release/0.3.z` |
| npm | frontend-ui | `package-lock.json` | `git show <commit>:package-lock.json` | `release/0.3.z` |

## Forward Pointer

<!-- Points to the next version stream's matrix, or "None" for the latest
     development stream. Helps navigation across streams. -->

<PENDING USER CONFIRMATION — "None" if 2.1.x is the latest stream, otherwise the next stream and its release repo>
````

Notes on the proposed content:
- Container Images rows are keyed by **Product Version + Component**; 2.1.0 api-rhel9 and api-rhel10 are separate
  rows with distinct image references and distinct `sha256` digests.
- Both 2.1.0 rows use the fixture's CPE `cpe:2.3:a:example:trustify_api:2.1.0:*:*:*:*:*:*:*` exactly as supplied.
  A single CPE identifying the same product version across platforms is acceptable; no platform-specific CPEs
  were invented.
- Release tag, resolved full commit SHA, image reference, image digest, and CPE are kept as distinct values.
- The Ecosystem Mappings Check Command values are taken verbatim from the supplied evidence (`<tag>` / `<commit>`
  are the ref pattern to substitute with the version's pinned ref from the Supportability Matrix).
- The Forward Pointer must be resolved by the user before writing — no placeholder will be written.

## Write Gate (none of these are satisfied yet)

1. Resolve the 2.1.1 api-rhel10 revision mismatch with corrected evidence (or explicit user decision to omit it).
2. Answer the 2.1.1 api-rhel9 and Forward Pointer questions.
3. User confirms the complete (possibly updated) proposal.
4. Immediately before writing, re-read `security-matrix.md` and compare with the proposal's source snapshot
   (absent). If it now exists, do not overwrite — preserve it, build a merged proposal, and request fresh
   confirmation (or abort).
5. Create with create-if-absent semantics and set `<!-- Last-Updated: ... -->` to the current UTC time.
