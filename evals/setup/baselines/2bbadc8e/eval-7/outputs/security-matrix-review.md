# Security Matrix Review — 2.1.x Stream

## Scaffold Source

Scaffolded from the canonical template `docs/templates/security-matrix.template.md`.
`docs/templates/security-matrix.md` is a worked example and was **not** used as a template or fallback.

## Configuration Context

From `## Security Configuration` in CLAUDE.md:

- **Stream**: 2.1.x
- **Konflux Release Repo**: git.downstream.example.com/my-org/product-release.2.1.z
- **Security Matrix Path**: security-matrix.md
- **Source Repositories**: backend, frontend-ui
- **Jira version prefix**: MYPRODUCT

---

## Proposed Security Matrix

<!-- Last-Updated: (will be set on confirmed write) -->

# Security Matrix — 2.1.x Stream

## Version Stream

This Konflux release repo covers the **2.1.x** product version stream.

## Supportability Matrix

| Product Version | Build | Build Date | backend | frontend-ui | Notes |
|---|---|---|---|---|---|
| 2.1.0 | 0.3.12 | 2026-06-15 | `v0.3.12` | `bb447eeb` | |
| 2.1.1 | 0.3.13 | 2026-06-20 | `v0.3.13` | `deadbeef` | |

#### Container Images

| Product Version | Component | Konflux Release Tag | Resolved Release Commit SHA | Image Reference | Image Digest | CPE |
|---|---|---|---|---|---|---|
| 2.1.0 | api-rhel9 | `v0.3.12` | `0123456789abcdef0123456789abcdef01234567` | `registry.example.test/trustify/api:2.1.0-rhel9` | `sha256:aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa` | `cpe:2.3:a:example:trustify_api:2.1.0:*:*:*:*:*:*:*` |
| 2.1.0 | api-rhel10 | `v0.3.12` | `0123456789abcdef0123456789abcdef01234567` | `registry.example.test/trustify/api:2.1.0-rhel10` | `sha256:bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb` | `cpe:2.3:a:example:trustify_api:2.1.0:*:*:*:*:*:*:*` |

> **⚠ BLOCKED — 2.1.1 / api-rhel10**: The published image's `org.opencontainers.image.revision` label is `fedcba9876543210fedcba9876543210fedcba98`, but the SHA resolved from Konflux release tag `v0.3.13` is `89abcdef0123456789abcdef0123456789abcdef`. These values **do not match**. This row is not included as verified data. Corrected evidence is required before this mapping can be added to the matrix.

| Product Version | Component | Konflux Release Tag | Resolved Release Commit SHA | Image Reference | Image Digest | CPE | Status |
|---|---|---|---|---|---|---|---|
| 2.1.1 | api-rhel10 | `v0.3.13` | `89abcdef0123456789abcdef0123456789abcdef` | `registry.example.test/trustify/api:2.1.1-rhel10` | `sha256:cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc` | `cpe:2.3:a:example:trustify_api:2.1.1:*:*:*:*:*:*:*` | **BLOCKED — revision mismatch** |

### OCI Revision Verification

| Product Version | Component | Resolved Release Commit SHA | `org.opencontainers.image.revision` | Match |
|---|---|---|---|---|
| 2.1.0 | api-rhel9 | `0123456789abcdef0123456789abcdef01234567` | `0123456789abcdef0123456789abcdef01234567` | ✅ Match |
| 2.1.0 | api-rhel10 | `0123456789abcdef0123456789abcdef01234567` | `0123456789abcdef0123456789abcdef01234567` | ✅ Match |
| 2.1.1 | api-rhel10 | `89abcdef0123456789abcdef0123456789abcdef` | `fedcba9876543210fedcba9876543210fedcba98` | ❌ **Mismatch** |

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

## Review Status

This is a **proposed** matrix presented for review. **No project file will be written** while the 2.1.1 / api-rhel10 revision mismatch remains unresolved. Please provide corrected evidence for the 2.1.1 image (either a corrected OCI revision label or a corrected resolved commit SHA) before the matrix can be finalized and written to `security-matrix.md`.

Only the two verified 2.1.0 rows (api-rhel9 and api-rhel10) are included as confirmed Container Images entries. The 2.1.1 row is shown separately as blocked and will not be written until the mismatch is resolved.
