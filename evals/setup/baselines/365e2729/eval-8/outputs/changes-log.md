# Changes Log: /sdlc-workflow:setup (security matrix scaffold)

## Discovery (simulated, no MCP tools, external services or shell commands used)

| Step | Finding | Action |
|---|---|---|
| 1. Read existing configuration | Read the input file `claude-md-configured-with-non-rhtpa-security.md`. It has a `# Project Configuration` section with Repository Registry, Jira Configuration, Code Intelligence, Bug Configuration and Security Configuration. | None |
| 2. Serena discovery | Found `serena_backend` and `serena_ui` in `mcp-tools-with-serena.md`. Both are already in the Repository Registry. | Repository Registry is up to date |
| 3. Jira Configuration | Project key, Cloud ID and Feature issue type ID are all populated. | Jira Configuration is up to date |
| 5. Code Intelligence | Covers both Serena instances and has a Limitations section. | Code Intelligence is up to date |
| 9. Bug Configuration | All three fields are populated. | Bug Configuration is up to date |
| 10. Security Configuration | Fully populated. Jira version prefix is `MYPRODUCT`. One stream: `2.1.x` at `security-matrix.md`. Source repos: `backend`, `frontend-ui`. | Security Configuration is up to date. No changes to CLAUDE.md. |
| 10.5. Matrix existence check | `security-matrix.md` for stream 2.1.x is missing. | Asked the user to scaffold it. User confirmed. |
| 10.6. Optional population | Asked whether to populate the Supportability Matrix and Container Images. | User declined, step skipped |

Out of scope for this matrix-focused task: the input CLAUDE.md has no `## Hierarchy Configuration` section and no `### Jira Field Defaults` subsection (Steps 3.5 and 4). Its Source Repositories table also has no Deployment context column. These were not changed or prompted for here.

## Proposed changes

| # | Target | Change | Status |
|---|---|---|---|
| 1 | `security-matrix.md` (stream 2.1.x) | Create a new scaffold from `docs/templates/security-matrix.template.md`. `{source-repo-name}`, `{source-ref}` and their matching separator cells were expanded into a `backend` and a `frontend-ui` column. Two Source Pinning Method entries were added (backend, frontend-ui). Fixed headings, fixed columns, Container Images, Ecosystem Mappings, Forward Pointer, comments and all other placeholders are unchanged. | Proposed and user-confirmed. NOT written to the project (eval mode). Would be written with create-if-absent semantics after a re-read. |

## Files not modified

- CLAUDE.md: no changes, since every relevant section was already configured
- `docs/constraints.md`, `CONVENTIONS.md`, bug template: not touched
- No actual project files were created or modified

## Eval output files

- `/tmp/setup-eval-baseline/eval-8/outputs/security-matrix-review.md`: the full proposed scaffold and the review
- `/tmp/setup-eval-baseline/eval-8/outputs/changes-log.md`: this file
