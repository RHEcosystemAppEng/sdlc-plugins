# Changes Log -- Security Matrix Setup (2.1.x Stream)

## Step 10.5: Scaffold Security Matrix

### Discovery

1. Read CLAUDE.md Security Configuration and found:
   - Version Streams table: 2.1.x stream configured at `security-matrix.md`.
   - Source Repositories: `backend` and `frontend-ui`.
   - Konflux Release Repo: `git.downstream.example.com/my-org/product-release.2.1.z`.

2. Checked for existing matrix at `security-matrix.md`: **not found** -- scaffolding required.

3. Identified canonical scaffold source: `docs/templates/security-matrix.template.md`.
   - This is the ONLY canonical scaffold template. `docs/templates/security-matrix.md` was NOT used as a template or fallback.

### Scaffolding Actions

- Expanded the `{stream}` placeholder to `2.1.x`.
- Expanded the Supportability Matrix header from a single `{source-repo-name}` column to two dynamic columns: `backend` and `frontend-ui`, matching the configured Source Repositories.
- The header row, separator row, and data rows all have the same number of cells (6 cells each: Product Version, Build, Build Date, backend, frontend-ui, Notes).
- Expanded Source Pinning Method to one entry per configured repository.
- Expanded Ecosystem Mappings placeholder to accept per-ecosystem rows.

## Step 10.6: Populate Security Matrix

### Evidence Ingested

- **Supportability rows**: 2 product versions (2.1.0, 2.1.1) with build numbers, dates, and per-repository source pins.
- **Container Image rows**: 3 entries (2.1.0/api-rhel9, 2.1.0/api-rhel10, 2.1.1/api-rhel10).
- **Source Pinning Methods**: backend via `artifacts.lock.yaml`, frontend-ui via Git submodule.
- **Ecosystem Mappings**: Cargo/backend and npm/frontend-ui rows preserved from evidence.

### Release Tag Resolution

| Product Version | Component | Tag | Resolved SHA | Status |
|---|---|---|---|---|
| 2.1.0 | api-rhel9 | `v0.3.12` | `0123456789abcdef0123456789abcdef01234567` | Resolved |
| 2.1.0 | api-rhel10 | `v0.3.12` | `0123456789abcdef0123456789abcdef01234567` | Resolved |
| 2.1.1 | api-rhel10 | `v0.3.13` | `89abcdef0123456789abcdef0123456789abcdef` | Resolved |

Note: Konflux release tag (e.g., `v0.3.12`) and resolved full commit SHA (e.g., `0123456789abcdef0123456789abcdef01234567`) are kept as SEPARATE values in the Container Images table.

### OCI Revision Label Verification

| Product Version | Component | OCI Revision Label | Expected (Resolved SHA) | Match |
|---|---|---|---|---|
| 2.1.0 | api-rhel9 | `0123456789abcdef0123456789abcdef01234567` | `0123456789abcdef0123456789abcdef01234567` | YES |
| 2.1.0 | api-rhel10 | `0123456789abcdef0123456789abcdef01234567` | `0123456789abcdef0123456789abcdef01234567` | YES |
| 2.1.1 | api-rhel10 | `fedcba9876543210fedcba9876543210fedcba98` | `89abcdef0123456789abcdef0123456789abcdef` | **NO -- MISMATCH** |

### Image Identity Preservation

- 2.1.0 / api-rhel9: image `registry.example.test/trustify/api:2.1.0-rhel9`, digest `sha256:aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa` -- distinct.
- 2.1.0 / api-rhel10: image `registry.example.test/trustify/api:2.1.0-rhel10`, digest `sha256:bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb` -- distinct.
- 2.1.1 / api-rhel10: image `registry.example.test/trustify/api:2.1.1-rhel10`, digest `sha256:cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc` -- distinct.
- CPE `cpe:2.3:a:example:trustify_api:2.1.0:*:*:*:*:*:*:*` is shared across 2.1.0/api-rhel9 and 2.1.0/api-rhel10 (valid -- CPE may be shared across platforms).

### Population Actions

- Filled Supportability Matrix with 2 version rows, each having `backend` and `frontend-ui` source-pin columns.
- Filled Container Images with 2 verified rows (2.1.0/api-rhel9, 2.1.0/api-rhel10) and 1 flagged row (2.1.1/api-rhel10).
- Filled Source Pinning Method with one entry per configured repository.
- Preserved Ecosystem Mappings rows for Cargo/backend and npm/frontend-ui.

### Flagged Issues

**2.1.1 / api-rhel10 -- OCI revision label mismatch**:
- The published image's `org.opencontainers.image.revision` label is `fedcba9876543210fedcba9876543210fedcba98`.
- The SHA resolved from Konflux release tag `v0.3.13` is `89abcdef0123456789abcdef0123456789abcdef`.
- These do NOT match. This row is FLAGGED and NOT presented as verified data.

### Write Decision

**Matrix NOT written.** The completed matrix was presented for user review, but because the 2.1.1/api-rhel10 OCI revision label mismatch remains unresolved, no matrix file was written to `security-matrix.md`. The matrix will only be written once all container image rows pass revision-label verification.
