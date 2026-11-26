# Changes Log — /sdlc-workflow:setup (simulated)

Target: CLAUDE.md (simulated from `evals/setup/files/claude-md-empty.md`)
Result file: `outputs/claude-md-result.md`

## CLAUDE.md

The existing content was kept unchanged (title, description, Documentation, Getting Started). A new `# Project Configuration` section was **added at the end of the file**.

### Added

1. `## Repository Registry`: table with 2 rows
   - backend | Rust backend service | serena_backend | /home/user/backend
   - frontend-ui | TypeScript frontend | serena_ui | /home/user/frontend-ui
2. `## Jira Configuration`
   - Project key: TC
   - Cloud ID: 2b9e35e3-6bd3-4cec-b838-f4249ee02432
   - Feature issue type ID: 10142
   - Git Pull Request custom field: customfield_10875
   - GitHub Issue custom field: customfield_10747
3. `### Jira Field Defaults` (skill defaults)
   - Default priority: none, fixVersion scope: both, Prompt for priority: true, Prompt for fixVersion: true
4. `## Code Intelligence`: naming convention, a `serena_backend` find_symbol example, and `### Limitations` (none known for either instance)
5. `## Security Configuration`: placed directly after Code Intelligence, as Step 10.4 requires, using `security-config.template.md`
   - `### Product Lifecycle`: the 4 required fields, plus VEX Justification custom field `customfield_12345`. Other optional fields are left blank.
   - `### Version Streams`: 1 row (2.1.x)
   - `### Source Repositories`: 2 rows (backend, frontend-ui), Deployment Context `upstream` (default)
6. `## Bug Configuration`
   - Bug issue type ID: 10001
   - Bug template: docs/bug-template.md
   - Bug-to-Task link type: Blocks

### Not added

- `## Hierarchy Configuration`: the simulation had no issue-type hierarchy data and the user gave no grouping strategy. Re-run `/setup` once Jira metadata is available.

### Modified / Removed

- None. Nothing existing was changed or removed.

## Other files (not written: simulation)

| File | Action in a real run | Action taken |
|---|---|---|
| `docs/constraints.md` | Create from `constraints.template.md` if missing | Skipped (no file modifications allowed) |
| `/home/user/backend/CONVENTIONS.md` | Offer scaffold if missing | Skipped (no file modifications allowed) |
| `/home/user/frontend-ui/CONVENTIONS.md` | Offer scaffold if missing | Skipped (no file modifications allowed) |
| `docs/bug-template.md` | Copy from `docs/templates/bug-template.md` | Skipped, as the task instructs |
| `security-matrix.md` | Scaffold from `docs/templates/security-matrix.template.md` | Skipped at the user's request |
| Supportability Matrix / Container Images | Optional population | The user declined |

No MCP tools were called. No Bash commands were run. Only files under `outputs/` were written.
