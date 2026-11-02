# Security Matrix — 2.1.x Stream

> **Scaffold source:** `docs/templates/security-matrix.template.md` (sole canonical template; `docs/templates/security-matrix.md` is a worked example and was NOT used)

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

**Revision verification for 2.1.0 rows:**
- api-rhel9: `org.opencontainers.image.revision` = `0123456789abcdef0123456789abcdef01234567` matches resolved release commit SHA `0123456789abcdef0123456789abcdef01234567` — **verified**
- api-rhel10: `org.opencontainers.image.revision` = `0123456789abcdef0123456789abcdef01234567` matches resolved release commit SHA `0123456789abcdef0123456789abcdef01234567` — **verified**

> **BLOCKED — 2.1.1 / api-rhel10:**
> The published image's `org.opencontainers.image.revision` label is `fedcba9876543210fedcba9876543210fedcba98`, but the SHA resolved from Konflux release tag `v0.3.13` is `89abcdef0123456789abcdef0123456789abcdef`. These values do **not** match. This row is **not** presented as verified data and is excluded from the Container Images table above. Corrected evidence is required before this mapping can be added.

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

This is the complete proposed matrix presented for user review. **No matrix file is written** until:

1. The 2.1.1 / api-rhel10 revision mismatch is resolved with corrected evidence.
2. The user confirms the final proposal after mismatch resolution.
