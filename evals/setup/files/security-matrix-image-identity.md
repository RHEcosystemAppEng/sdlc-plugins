<!-- SYNTHETIC TEST DATA — fictional Konflux tags, release commits, published OCI image references, digests, revision labels, and CPEs for Setup evals. -->

# Supportability and Ecosystem Evidence

| Product Version | Build | Build Date | backend | frontend-ui | Notes |
|---|---|---|---|---|---|
| 2.1.0 | 0.3.12 | 2026-06-15 | `v0.3.12` | `bb447eeb` | |
| 2.1.1 | 0.3.13 | 2026-06-20 | `v0.3.13` | `deadbeef` | |

| Repository | Source Pinning Method |
|---|---|
| backend | `artifacts.lock.yaml` download URL contains the release tag |
| frontend-ui | Git submodule at `components/frontend-ui` |

| Ecosystem | Repository | Lock File | Check Command | Upstream Branch |
|---|---|---|---|---|
| Cargo | backend | `Cargo.lock` | `git show <tag>:Cargo.lock` | `release/0.3.z` |
| npm | frontend-ui | `package-lock.json` | `git show <commit>:package-lock.json` | `release/0.3.z` |

# Release Tag Resolution Evidence

| Product Version | Component | Konflux Release Tag | Resolved Release Commit SHA |
|---|---|---|---|
| 2.1.0 | api-rhel9 | `v0.3.12` | `0123456789abcdef0123456789abcdef01234567` |
| 2.1.0 | api-rhel10 | `v0.3.12` | `0123456789abcdef0123456789abcdef01234567` |
| 2.1.1 | api-rhel10 | `v0.3.13` | `89abcdef0123456789abcdef0123456789abcdef` |

# Published OCI Image Evidence

The revision label below is the published image's
`org.opencontainers.image.revision` value.

| Product Version | Component | Image Reference | Immutable Image Digest | CPE | `org.opencontainers.image.revision` |
|---|---|---|---|---|---|
| 2.1.0 | api-rhel9 | `registry.example.test/trustify/api:2.1.0-rhel9` | `sha256:aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa` | `cpe:2.3:a:example:trustify_api:2.1.0:*:*:*:*:*:*:*` | `0123456789abcdef0123456789abcdef01234567` |
| 2.1.0 | api-rhel10 | `registry.example.test/trustify/api:2.1.0-rhel10` | `sha256:bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb` | `cpe:2.3:a:example:trustify_api:2.1.0:*:*:*:*:*:*:*` | `0123456789abcdef0123456789abcdef01234567` |
| 2.1.1 | api-rhel10 | `registry.example.test/trustify/api:2.1.1-rhel10` | `sha256:cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc` | `cpe:2.3:a:example:trustify_api:2.1.1:*:*:*:*:*:*:*` | `fedcba9876543210fedcba9876543210fedcba98` |
