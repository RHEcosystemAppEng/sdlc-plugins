# Changes Log — /sdlc-workflow:setup (simulated)

Target: CLAUDE.md (input `claude-md-empty.md`). It had no `# Project Configuration`, so the whole section is **appended at the end of the file** (Step 6). Existing content (title, Documentation, Getting Started) is kept unchanged.

The result is written to `outputs/claude-md-result.md`. No real project files were modified.

## Added

| Section | Change |
|---|---|
| `# Project Configuration` | New heading appended |
| `## Repository Registry` | 2 rows added: `backend` (Rust backend service, serena_backend, /home/user/backend) and `frontend-ui` (TypeScript frontend, serena_ui, /home/user/frontend-ui) |
| `## Jira Configuration` | Project key TC, Cloud ID 2b9e35e3-6bd3-4cec-b838-f4249ee02432, Feature issue type ID 10142, Git PR field customfield_10875, GitHub Issue field customfield_10747 |
| `### Jira Field Defaults` | Default priority none, fixVersion scope both, Prompt for priority true, Prompt for fixVersion true (skill defaults) |
| `## Code Intelligence` | `mcp__<instance>__<tool>` naming convention, example using `serena_backend`, and a `### Limitations` subsection (no known limitations) |
| `## Security Configuration` | Added from `security-config.template.md`, placed right after Code Intelligence (Step 10.4). Contains Product Lifecycle (4 required fields plus the VEX field set, other optional fields empty), Version Streams (1 row: 2.1.x), Source Repositories (backend and frontend-ui, both `upstream`) |
| `## Bug Configuration` | Bug issue type ID 10001, Bug template docs/bug-template.md, Bug-to-Task link type Blocks |

## Not added / skipped

- `## Hierarchy Configuration`: not created, because the issue type hierarchy could not be discovered in the simulation and no grouping strategy was provided.
- `docs/constraints.md` copy (Step 7): skipped. The task only allows writes to `outputs/`.
- CONVENTIONS.md scaffolding (Step 8): skipped. The task gives no instruction for it and only allows writes to `outputs/`.
- Bug template copy to `docs/bug-template.md` (Step 9.4): skipped, as the task instructs.
- security-matrix.md scaffolding (Step 10.5): the user skipped it.
- Supportability Matrix / Container Images population (Step 10.6): the user declined.

## Validation (Step 11, against outputs/claude-md-result.md)

- [x] `# Project Configuration` heading exists
- [x] Repository Registry table has the columns Repository, Role, Serena Instance, Path
- [x] Jira Configuration has Project key, Cloud ID, Feature issue type ID
- [x] Jira Field Defaults has valid values (no placeholders)
- [x] Code Intelligence documents `mcp__<instance>__<tool>`
- [x] Code Intelligence has a `### Limitations` subheading
- [ ] `docs/constraints.md` exists: not verified, because file writes outside outputs/ are not allowed
- [x] Bug Configuration has Bug issue type ID, Bug template path, Bug-to-Task link type
- [ ] Bug template file exists at docs/bug-template.md: the copy was skipped
- [n/a] Hierarchy Configuration: not scaffolded
- [x] Security Configuration has `### Product Lifecycle` with all four required fields (VEX also set)
- [x] Security Configuration has `### Version Streams` with at least one row
- [x] Security Configuration has `### Source Repositories` with at least one row
- [x] No `{{placeholder}}` markers remain
