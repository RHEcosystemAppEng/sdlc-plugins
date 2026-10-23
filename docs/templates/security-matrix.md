<!-- SYNTHETIC WORKED EXAMPLE — all product, release, image, digest, revision-label, and CPE values are fictional. This file is reference only; the canonical scaffold is docs/templates/security-matrix.template.md. -->

# Worked Example: RHTPA 2.2.x Security Matrix

This fictional completed example illustrates a 2.2.x product stream.
`triage-security` reads completed matrix files to determine which versions
ship a dependency. This file is reference only; Setup reads
`docs/templates/security-matrix.template.md` when creating a new matrix.

## Version Stream

This Konflux release repo covers the **2.2.x** product version stream.

## Supportability Matrix

| Version | Build | Build Date | backend | frontend-ui | Notes |
|---------|-------|------------|---------|-------------|-------|
| 2.2.0 | 0.4.5 | 2025-12-03 | `v0.4.5` | `bb447eeb` | |
| 2.2.1 | 0.4.8 | 2026-02-05 | `v0.4.8` | `40874efb` | |
| 2.2.2 | 0.4.9 | 2026-02-23 | `v0.4.9` | `40874efb` | frontend-ui retag of 2.2.1 |
| 2.2.3 | 0.4.11 | 2026-03-23 | `v0.4.11` | `bf9fc536` | |
| 2.2.4 | 0.4.12 | 2026-05-04 | `v0.4.12` | `9e03dca1` | |

#### Container Images

Each row is keyed by product version and component, so images for different
platforms remain distinct. For both 2.2.4 images below, the published
`org.opencontainers.image.revision` label equals the resolved release commit
SHA. The OCI digests identify the immutable images; they are not release tags
or Git commit IDs.

| Product Version | Component | Konflux Release Tag | Resolved Release Commit SHA | Image Reference | Image Digest | CPE |
|---|---|---|---|---|---|---|
| 2.2.4 | backend-rhel9 | `v0.4.12` | `1234567890abcdef1234567890abcdef12345678` | `registry.example.test/rhtpa/backend:2.2.4-rhel9` | `sha256:1111111111111111111111111111111111111111111111111111111111111111` | `cpe:2.3:a:example:rhtpa_backend_rhel9:2.2.4:*:*:*:*:*:*:*` |
| 2.2.4 | backend-rhel10 | `v0.4.12` | `1234567890abcdef1234567890abcdef12345678` | `registry.example.test/rhtpa/backend:2.2.4-rhel10` | `sha256:2222222222222222222222222222222222222222222222222222222222222222` | `cpe:2.3:a:example:rhtpa_backend_rhel10:2.2.4:*:*:*:*:*:*:*` |

### Source Pinning Method

- **backend**: `artifacts.lock.yaml` (download URL contains tag, e.g., `v0.4.12`)
- **frontend-ui**: git submodule at `components/frontend-ui`

## Ecosystem Mappings

These entries show the repository, lock file, inspection command, and upstream
branch that `triage-security` uses for dependency and fix checks.

| Ecosystem | Repository | Lock File | Check Command | Upstream Branch |
|-----------|------------|-----------|---------------|-----------------|
| Cargo | backend | `Cargo.lock` | `git show v0.4.12:Cargo.lock` | `release/0.4.z` |
| npm | frontend-ui | `package-lock.json` | `git show 9e03dca1:package-lock.json` | `release/0.4.z` |

## Forward Pointer

Next stream: `3.0.x` at `git.downstream.example.com/my-org/product-release.0.5.z`
