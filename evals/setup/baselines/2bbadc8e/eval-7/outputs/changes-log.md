# Changes Log — Security Matrix Setup (2.1.x Stream)

## Scaffold Source

- **Template used**: `docs/templates/security-matrix.template.md` (canonical scaffold)
- **Template NOT used**: `docs/templates/security-matrix.md` (worked example — excluded per SKILL.md Step 10.5)

## Configuration Read

From CLAUDE.md `## Security Configuration`:

- Stream: 2.1.x
- Konflux Release Repo: git.downstream.example.com/my-org/product-release.2.1.z
- Local Path: /home/user/product-release.2.1.z
- Security Matrix Path: security-matrix.md
- Source Repositories: backend, frontend-ui
- Jira version prefix: MYPRODUCT

## Scaffold Expansion

The canonical template's `{source-repo-name}` / `{source-ref}` placeholders were expanded into two dynamic source columns (`backend` and `frontend-ui`) in the Supportability Matrix, with matching separator and data cells aligned across all rows.

### Sections Scaffolded

1. **Version Stream** — set to 2.1.x
2. **Supportability Matrix** — expanded with backend and frontend-ui source columns; populated with 2 product version rows (2.1.0, 2.1.1) from evidence
3. **Container Images** — populated with 2 verified rows (2.1.0/api-rhel9, 2.1.0/api-rhel10); 1 row blocked (2.1.1/api-rhel10 — revision mismatch)
4. **Source Pinning Method** — 2 entries: backend (artifacts.lock.yaml), frontend-ui (Git submodule)
5. **Ecosystem Mappings** — preserved 2 rows from evidence: Cargo/backend, npm/frontend-ui
6. **Forward Pointer** — set to None

## Population Details

### Verified Image Rows (2)

| Product Version | Component | Status |
|---|---|---|
| 2.1.0 | api-rhel9 | ✅ Verified — OCI revision matches resolved SHA |
| 2.1.0 | api-rhel10 | ✅ Verified — OCI revision matches resolved SHA |

### Blocked Image Rows (1)

| Product Version | Component | Status | Reason |
|---|---|---|---|
| 2.1.1 | api-rhel10 | ❌ Blocked | `org.opencontainers.image.revision` (`fedcba9876543210fedcba9876543210fedcba98`) does not match resolved release commit SHA from tag v0.3.13 (`89abcdef0123456789abcdef0123456789abcdef`) |

## User Actions

- User confirmed scaffolding the missing matrix: **Yes**
- User requested population from evidence: **Yes**
- User declined optional supportability matrix population: No (population was requested)

## Write Status

**No project file was written.** The proposed matrix is presented for review only. The 2.1.1/api-rhel10 revision mismatch must be resolved with corrected evidence before the matrix can be finalized. Once resolved, a final confirmation is required before writing to `security-matrix.md`.
