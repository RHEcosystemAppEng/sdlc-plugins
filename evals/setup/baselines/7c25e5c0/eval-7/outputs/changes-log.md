# Changes Log — Security Matrix Setup (Eval 7)

## Scaffold Source

- Canonical scaffold: `docs/templates/security-matrix.template.md`
- `docs/templates/security-matrix.md` is a worked example and was **not** used as a template or fallback

## Configuration Source

- CLAUDE.md: `evals/setup/files/claude-md-configured-with-security.md`
- Version Stream: 2.1.x
- Security Matrix Path: `security-matrix.md`
- Source Repositories: backend, frontend-ui

## Supportability Matrix

- Populated from supplied evidence with dynamic source columns for **backend** and **frontend-ui**
- 2 product version rows added: 2.1.0 and 2.1.1
- Source Pinning Methods documented for both repositories:
  - backend: `artifacts.lock.yaml` download URL contains the release tag
  - frontend-ui: Git submodule at `components/frontend-ui`

## Ecosystem Mappings

- Preserved from supplied evidence:
  - Cargo / backend: `Cargo.lock` via `git show <tag>:Cargo.lock`, upstream branch `release/0.3.z`
  - npm / frontend-ui: `package-lock.json` via `git show <commit>:package-lock.json`, upstream branch `release/0.3.z`

## Container Images — Revision Verification

### Verified rows (added to proposed matrix)

| Product Version | Component | Status | Details |
|---|---|---|---|
| 2.1.0 | api-rhel9 | **Verified** | OCI revision `0123456789abcdef0123456789abcdef01234567` matches resolved SHA from `v0.3.12` |
| 2.1.0 | api-rhel10 | **Verified** | OCI revision `0123456789abcdef0123456789abcdef01234567` matches resolved SHA from `v0.3.12` |

### Unverified rows (excluded from proposed matrix)

| Product Version | Component | Status | Details |
|---|---|---|---|
| 2.1.1 | api-rhel10 | **BLOCKED** | OCI revision label `fedcba9876543210fedcba9876543210fedcba98` does NOT match SHA `89abcdef0123456789abcdef0123456789abcdef` resolved from tag `v0.3.13`. Corrected evidence required. |

## Write Status

- No matrix file written — the proposed matrix is presented for review only
- The 2.1.1 / api-rhel10 revision mismatch must be resolved before the matrix can be finalized
- A confirmed write will set `<!-- Last-Updated: <ISO-8601-timestamp> -->` to the current UTC time
