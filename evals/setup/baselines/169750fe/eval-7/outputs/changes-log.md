# Changes Log -- Security Matrix Setup for 2.1.x Stream

## Configuration Source

- CLAUDE.md: `evals/setup/files/claude-md-configured-with-security.md`
- Security Configuration found: fully populated (no placeholders)
- Version Stream: 2.1.x
- Konflux Release Repo: `git.downstream.example.com/my-org/product-release.2.1.z`
- Local Path: `/home/user/product-release.2.1.z`
- Security Matrix Path: `security-matrix.md`
- Configured Source Repositories: backend, frontend-ui

## Step 10.5 -- Scaffold security-matrix.md

### Discovery

- Checked configured path `security-matrix.md`: file does NOT exist.
- Canonical scaffold template identified: `docs/templates/security-matrix.template.md`
- `docs/templates/security-matrix.md` is the worked EXAMPLE only -- it was NOT used as a template or fallback.

### Scaffold Actions

1. Read `docs/templates/security-matrix.template.md` as the sole canonical scaffold.
2. Expanded `{stream}` placeholder to `2.1.x`.
3. Expanded `{source-repo-name}` in the Supportability Matrix header into two dynamic
   columns (`backend`, `frontend-ui`) matching the configured Source Repositories.
   Separator row cells and data-row cells were expanded in lockstep to maintain
   consistent column counts (6 columns: Product Version, Build, Build Date, backend,
   frontend-ui, Notes).
4. Expanded Source Pinning Method section to two entries, one per configured source
   repository (backend, frontend-ui).
5. Retained Container Images and Ecosystem Mappings table structures from the template
   with placeholder rows.
6. User confirmed scaffolding the missing matrix.

## Step 10.6 -- Populate Supportability and Image Identity

### Supportability Matrix Population

- Added 2 rows from the supplied evidence:
  - 2.1.0: Build 0.3.12, Date 2026-06-15, backend `v0.3.12`, frontend-ui `bb447eeb`
  - 2.1.1: Build 0.3.13, Date 2026-06-20, backend `v0.3.13`, frontend-ui `deadbeef`

### Container Images Population

- Processed 3 image entries from the supplied evidence, keyed by Product Version AND Component.

#### Verified rows (OCI revision label matches resolved SHA):

| Product Version | Component | Konflux Release Tag | Resolved SHA | OCI Revision Label | Status |
|---|---|---|---|---|---|
| 2.1.0 | api-rhel9 | `v0.3.12` | `0123456789abcdef0123456789abcdef01234567` | `0123456789abcdef0123456789abcdef01234567` | VERIFIED |
| 2.1.0 | api-rhel10 | `v0.3.12` | `0123456789abcdef0123456789abcdef01234567` | `0123456789abcdef0123456789abcdef01234567` | VERIFIED |

Both 2.1.0 rows carry the same CPE (`cpe:2.3:a:example:trustify_api:2.1.0:*:*:*:*:*:*:*`),
which is correct -- the same CPE applies across platform variants (rhel9 and rhel10).

#### Flagged row (OCI revision label MISMATCH):

| Product Version | Component | Konflux Release Tag | Resolved SHA | OCI Revision Label | Status |
|---|---|---|---|---|---|
| 2.1.1 | api-rhel10 | `v0.3.13` | `89abcdef0123456789abcdef0123456789abcdef` | `fedcba9876543210fedcba9876543210fedcba98` | **MISMATCH** |

The published image's `org.opencontainers.image.revision` label
(`fedcba9876543210fedcba9876543210fedcba98`) does NOT match the commit SHA resolved
from Konflux release tag `v0.3.13` (`89abcdef0123456789abcdef0123456789abcdef`).
This row is flagged and excluded from the verified Container Images table. It must
not be presented as verified data.

### Source Pinning Method Population

- **backend**: `artifacts.lock.yaml` download URL contains the release tag (from evidence)
- **frontend-ui**: Git submodule at `components/frontend-ui` (from evidence)

### Ecosystem Mappings Population

- Cargo / backend: Lock File `Cargo.lock`, Check Command `git show <tag>:Cargo.lock`, Upstream Branch `release/0.3.z`
- npm / frontend-ui: Lock File `package-lock.json`, Check Command `git show <commit>:package-lock.json`, Upstream Branch `release/0.3.z`

## Write Decision

**Matrix NOT written.** The 2.1.1 / api-rhel10 image has an unresolved OCI revision
label mismatch. Per Step 10.6 rules, the matrix file remains unchanged until corrected
evidence is provided and the mismatch is resolved. The complete proposed matrix has
been presented for review in `outputs/security-matrix-review.md`.
