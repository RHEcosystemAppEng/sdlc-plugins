# Security Matrix Review -- 2.1.x Stream

## Discovery Summary

- **CLAUDE.md Security Configuration**: Found Version Streams table configuring the **2.1.x** stream at local path `security-matrix.md` with Konflux release repo `git.downstream.example.com/my-org/product-release.2.1.z`.
- **Source Repositories**: Two configured -- `backend` (https://github.com/example/backend) and `frontend-ui` (https://github.com/example/frontend-ui).
- **Existing matrix at `security-matrix.md`**: Not found. Scaffolding required.
- **Canonical scaffold source**: `docs/templates/security-matrix.template.md` (the ONLY canonical template used; `docs/templates/security-matrix.md` is NOT used as a template or fallback).

## Proposed Security Matrix

The following matrix was scaffolded from `docs/templates/security-matrix.template.md` and populated with the supplied release and published-image evidence.

---

### Version Stream

This Konflux release repo covers the **2.1.x** product version stream.

### Supportability Matrix

| Product Version | Build | Build Date | backend | frontend-ui | Notes |
|---|---|---|---|---|---|
| 2.1.0 | 0.3.12 | 2026-06-15 | `v0.3.12` | `bb447eeb` | |
| 2.1.1 | 0.3.13 | 2026-06-20 | `v0.3.13` | `deadbeef` | |

#### Container Images

| Product Version | Component | Konflux Release Tag | Resolved Release Commit SHA | Image Reference | Image Digest | CPE |
|---|---|---|---|---|---|---|
| 2.1.0 | api-rhel9 | `v0.3.12` | `0123456789abcdef0123456789abcdef01234567` | `registry.example.test/trustify/api:2.1.0-rhel9` | `sha256:aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa` | `cpe:2.3:a:example:trustify_api:2.1.0:*:*:*:*:*:*:*` |
| 2.1.0 | api-rhel10 | `v0.3.12` | `0123456789abcdef0123456789abcdef01234567` | `registry.example.test/trustify/api:2.1.0-rhel10` | `sha256:bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb` | `cpe:2.3:a:example:trustify_api:2.1.0:*:*:*:*:*:*:*` |
| 2.1.1 | api-rhel10 | **FLAGGED -- SEE BELOW** | | | | |

> **MISMATCH FLAG -- 2.1.1 / api-rhel10**: The published OCI image's `org.opencontainers.image.revision` label is `fedcba9876543210fedcba9876543210fedcba98`, but the SHA resolved from Konflux release tag `v0.3.13` is `89abcdef0123456789abcdef0123456789abcdef`. These values do NOT match. This row cannot be marked as verified. The raw evidence is preserved below for reference but is excluded from the verified matrix.
>
> | Field | Value |
> |---|---|
> | Product Version | 2.1.1 |
> | Component | api-rhel10 |
> | Konflux Release Tag | `v0.3.13` |
> | Resolved Release Commit SHA | `89abcdef0123456789abcdef0123456789abcdef` |
> | Image Reference | `registry.example.test/trustify/api:2.1.1-rhel10` |
> | Image Digest | `sha256:cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc` |
> | CPE | `cpe:2.3:a:example:trustify_api:2.1.1:*:*:*:*:*:*:*` |
> | OCI revision label | `fedcba9876543210fedcba9876543210fedcba98` |
> | Expected (from tag) | `89abcdef0123456789abcdef0123456789abcdef` |

### Source Pinning Method

- **backend**: `artifacts.lock.yaml` download URL contains the release tag
- **frontend-ui**: Git submodule at `components/frontend-ui`

### Ecosystem Mappings

| Ecosystem | Repository | Lock File | Check Command | Upstream Branch |
|---|---|---|---|---|
| Cargo | backend | `Cargo.lock` | `git show <tag>:Cargo.lock` | `release/0.3.z` |
| npm | frontend-ui | `package-lock.json` | `git show <commit>:package-lock.json` | `release/0.3.z` |

### Forward Pointer

None (latest configured stream).

---

## Validation Result

**STATUS: BLOCKED -- matrix will NOT be written.**

The 2.1.1 / api-rhel10 container image row has a revision-label mismatch: the OCI `org.opencontainers.image.revision` label (`fedcba9876543210fedcba9876543210fedcba98`) does not equal the commit SHA resolved from Konflux release tag `v0.3.13` (`89abcdef0123456789abcdef0123456789abcdef`). Until this discrepancy is investigated and resolved, the security matrix file will not be written to `security-matrix.md`.

### Verified rows (would be written once mismatch is resolved)

- 2.1.0 / api-rhel9 -- OCI revision `0123456789abcdef0123456789abcdef01234567` matches resolved SHA. Verified.
- 2.1.0 / api-rhel10 -- OCI revision `0123456789abcdef0123456789abcdef01234567` matches resolved SHA. Verified.

### Unverified rows (blocking write)

- 2.1.1 / api-rhel10 -- OCI revision `fedcba9876543210fedcba9876543210fedcba98` does NOT match resolved SHA `89abcdef0123456789abcdef0123456789abcdef`. **MISMATCH. Not verified.**

### Next steps

1. Investigate why the 2.1.1 / api-rhel10 image was built from a different commit than the one resolved from tag `v0.3.13`.
2. Once the mismatch is resolved (either the image is rebuilt or the tag is corrected), re-run population to produce a fully verified matrix.
3. The matrix will be written to `security-matrix.md` only after all container image rows pass revision-label verification.
