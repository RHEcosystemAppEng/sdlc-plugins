# Setup Changes Log

## Security Matrix Setup — 2.1.x Stream

### Discovery (Simulated)

1. **Read existing CLAUDE.md** (`claude-md-configured-with-security.md`):
   - `# Project Configuration` heading: present
   - `## Repository Registry`: 2 repositories (backend, frontend-ui) with Serena instances
   - `## Jira Configuration`: fully populated (Project key: TC, Cloud ID, Feature issue type ID: 10142)
   - `## Code Intelligence`: fully populated with serena_backend and serena_ui
   - `## Bug Configuration`: fully populated (Bug issue type ID: 10001, template: docs/bug-template.md, link type: Blocks)
   - `## Security Configuration`: fully populated, no `{{placeholder}}` markers
   - `## Hierarchy Configuration`: not present (not configured)

2. **Serena instance discovery** (from `mcp-tools-with-serena.md`):
   - `serena_backend`: 10 tools available
   - `serena_ui`: 10 tools available
   - Both already in Repository Registry -- no changes needed

3. **Security Configuration assessment**:
   - All required fields populated, no placeholders
   - Version Streams: 1 stream (2.1.x) configured
   - Source Repositories: 2 repos (backend, frontend-ui)
   - Status: **up to date**

### Steps Completed

| Step | Description | Status |
|---|---|---|
| Step 1 | Read existing configuration | Complete -- all sections present |
| Step 2 | Discover Serena instances | Skipped -- Repository Registry up to date |
| Step 3 | Jira Configuration | Skipped -- already fully populated |
| Step 3.5 | Hierarchy Preferences | Not present -- would require user interaction |
| Step 4 | Jira Field Defaults | Skipped -- would require MCP/user interaction |
| Step 5 | Code Intelligence | Skipped -- already up to date |
| Step 6 | Write Configuration | No changes needed |
| Step 7 | Copy Constraints Template | Simulated -- skipped (no filesystem writes) |
| Step 8 | Scaffold CONVENTIONS.md | Simulated -- skipped (no filesystem writes) |
| Step 9 | Bug Configuration | Skipped -- already fully populated |
| Step 10 | Security Configuration | Already fully populated -- up to date |
| Step 10.5 | Scaffold security-matrix.md | **Scaffolded** for 2.1.x stream at `security-matrix.md` |
| Step 10.6 | Populate supportability and image identity | **Completed with findings** (see below) |

### Step 10.5 — Security Matrix Scaffolding

- Stream: **2.1.x**
- Configured path: `security-matrix.md`
- File status: **missing** (simulated)
- Action: Scaffolded from `docs/templates/security-matrix.template.md`
- Source repo columns expanded: `backend`, `frontend-ui` (one column per Source Repositories entry)
- Source Pinning Method entries expanded: `backend`, `frontend-ui`

### Step 10.6 — Supportability and Image Identity Population

#### Supportability Matrix

Populated 2 rows from release evidence:

| Product Version | Build | Build Date | backend | frontend-ui |
|---|---|---|---|---|
| 2.1.0 | 0.3.12 | 2026-06-15 | `v0.3.12` | `bb447eeb` |
| 2.1.1 | 0.3.13 | 2026-06-20 | `v0.3.13` | `deadbeef` |

#### Container Images

Populated 2 verified rows. 1 row withheld due to revision mismatch.

**Verified rows:**

| Product Version | Component | Status |
|---|---|---|
| 2.1.0 | api-rhel9 | Verified -- revision label matches resolved SHA (`0123456789abcdef0123456789abcdef01234567`) |
| 2.1.0 | api-rhel10 | Verified -- revision label matches resolved SHA (`0123456789abcdef0123456789abcdef01234567`) |

**Unresolved rows:**

| Product Version | Component | Issue |
|---|---|---|
| 2.1.1 | api-rhel10 | MISMATCH -- `org.opencontainers.image.revision` is `fedcba9876543210fedcba9876543210fedcba98` but resolved release commit SHA is `89abcdef0123456789abcdef0123456789abcdef`. Row withheld from matrix pending corrected evidence. |

#### Source Pinning Methods

Populated from evidence:

- **backend**: `artifacts.lock.yaml` download URL contains the release tag
- **frontend-ui**: Git submodule at `components/frontend-ui`

#### Ecosystem Mappings

Populated from evidence:

| Ecosystem | Repository | Lock File | Check Command | Upstream Branch |
|---|---|---|---|---|
| Cargo | backend | `Cargo.lock` | `git show <tag>:Cargo.lock` | `release/0.3.z` |
| npm | frontend-ui | `package-lock.json` | `git show <commit>:package-lock.json` | `release/0.3.z` |

### Validation Summary

- Security Configuration in CLAUDE.md: fully populated, all required fields present
- Version Streams table: 1 stream configured (2.1.x)
- Source Repositories table: 2 repos configured (backend, frontend-ui)
- Security matrix scaffolded at configured path with populated data
- Image identity verification: 2 of 3 images verified; 1 unresolved mismatch flagged
- No actual project files were modified (simulation only)
