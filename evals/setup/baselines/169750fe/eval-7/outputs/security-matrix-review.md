# Security Matrix Review -- 2.1.x Stream

## Scaffold Source

Canonical scaffold template: `docs/templates/security-matrix.template.md`

> `docs/templates/security-matrix.md` is a worked example only and was NOT used as a
> template or fallback for this scaffold.

The configured security matrix path `security-matrix.md` does not exist. A new matrix
was scaffolded from the canonical template and populated with the supplied release and
published-image evidence.

---

## Proposed Matrix Content

# Security Matrix -- 2.1.x Stream

## Version Stream

This Konflux release repo covers the **2.1.x** product version stream.

## Supportability Matrix

| Product Version | Build | Build Date | backend | frontend-ui | Notes |
|---|---|---|---|---|---|
| 2.1.0 | 0.3.12 | 2026-06-15 | `v0.3.12` | `bb447eeb` | |
| 2.1.1 | 0.3.13 | 2026-06-20 | `v0.3.13` | `deadbeef` | |

#### Container Images

Each row is keyed by Product Version and Component. The Konflux release tag and the
full commit SHA resolved from that tag are kept as separate values. The published
image reference and the immutable OCI image digest are likewise distinct. The
published image's `org.opencontainers.image.revision` label must equal the resolved
release commit SHA for the row to be considered verified.

| Product Version | Component | Konflux Release Tag | Resolved Release Commit SHA | Image Reference | Image Digest | CPE |
|---|---|---|---|---|---|---|
| 2.1.0 | api-rhel9 | `v0.3.12` | `0123456789abcdef0123456789abcdef01234567` | `registry.example.test/trustify/api:2.1.0-rhel9` | `sha256:aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa` | `cpe:2.3:a:example:trustify_api:2.1.0:*:*:*:*:*:*:*` |
| 2.1.0 | api-rhel10 | `v0.3.12` | `0123456789abcdef0123456789abcdef01234567` | `registry.example.test/trustify/api:2.1.0-rhel10` | `sha256:bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb` | `cpe:2.3:a:example:trustify_api:2.1.0:*:*:*:*:*:*:*` |

### OCI Revision Label Verification (2.1.0 rows)

| Product Version | Component | OCI Revision Label | Resolved Release Commit SHA | Status |
|---|---|---|---|---|
| 2.1.0 | api-rhel9 | `0123456789abcdef0123456789abcdef01234567` | `0123456789abcdef0123456789abcdef01234567` | VERIFIED |
| 2.1.0 | api-rhel10 | `0123456789abcdef0123456789abcdef01234567` | `0123456789abcdef0123456789abcdef01234567` | VERIFIED |

### OCI Revision Label Verification (2.1.1 rows)

> **MISMATCH DETECTED -- 2.1.1 / api-rhel10**
>
> The published image's `org.opencontainers.image.revision` label does NOT match the
> SHA resolved from the Konflux release tag `v0.3.13`.
>
> - OCI revision label: `fedcba9876543210fedcba9876543210fedcba98`
> - Resolved release commit SHA (from tag `v0.3.13`): `89abcdef0123456789abcdef0123456789abcdef`
>
> This row is **FLAGGED** and is excluded from the Container Images table above.
> It MUST NOT be presented as verified data. Corrected evidence is required before
> this row can be added to the matrix.

| Product Version | Component | Konflux Release Tag | Resolved Release Commit SHA | Image Reference | Image Digest | CPE | OCI Revision Label | Status |
|---|---|---|---|---|---|---|---|---|
| 2.1.1 | api-rhel10 | `v0.3.13` | `89abcdef0123456789abcdef0123456789abcdef` | `registry.example.test/trustify/api:2.1.1-rhel10` | `sha256:cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc` | `cpe:2.3:a:example:trustify_api:2.1.1:*:*:*:*:*:*:*` | `fedcba9876543210fedcba9876543210fedcba98` | **MISMATCH** |

### Source Pinning Method

- **backend**: `artifacts.lock.yaml` download URL contains the release tag
- **frontend-ui**: Git submodule at `components/frontend-ui`

## Ecosystem Mappings

| Ecosystem | Repository | Lock File | Check Command | Upstream Branch |
|---|---|---|---|---|
| Cargo | backend | `Cargo.lock` | `git show <tag>:Cargo.lock` | `release/0.3.z` |
| npm | frontend-ui | `package-lock.json` | `git show <commit>:package-lock.json` | `release/0.3.z` |

## Forward Pointer

None

---

## Review Decision

**The matrix CANNOT be written in its current state.**

The 2.1.1 / api-rhel10 image has an unresolved OCI revision label mismatch:
the published `org.opencontainers.image.revision` label (`fedcba9876543210fedcba9876543210fedcba98`)
does not match the commit SHA resolved from the Konflux release tag `v0.3.13`
(`89abcdef0123456789abcdef0123456789abcdef`).

The matrix file will not be written while this mismatch remains unresolved.
Please provide corrected evidence for the 2.1.1 / api-rhel10 image (either an
updated OCI revision label or a corrected release tag resolution) before the
matrix can be finalized and written to disk.
