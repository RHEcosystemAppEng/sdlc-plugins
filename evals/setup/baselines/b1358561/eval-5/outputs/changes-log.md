# Changes Log — /sdlc-workflow:setup (simulated)

Target: CLAUDE.md (input: `evals/setup/files/claude-md-empty.md`)
Result: `outputs/claude-md-result.md`

## Preserved (unchanged)

- The SYNTHETIC TEST DATA comment, `# my-project`, the description, `## Documentation` and `## Getting Started`. I removed nothing and overwrote nothing.

## Added (appended at end of file, since CLAUDE.md had no `# Project Configuration`)

1. `# Project Configuration`
2. `## Repository Registry`, 2 rows:
   - backend | Rust backend service | serena_backend | /home/user/backend
   - frontend-ui | TypeScript frontend | serena_ui | /home/user/frontend-ui
3. `## Jira Configuration`: Project key TC, Cloud ID 2b9e35e3-6bd3-4cec-b838-f4249ee02432, Feature issue type ID 10142, Git Pull Request custom field customfield_10875, GitHub Issue custom field customfield_10747
   - `### Jira Field Defaults`: none / both / true / true (skill defaults, because no input was given)
4. `## Code Intelligence`: explains the naming convention, gives a `serena_backend` find_symbol example, and has a `### Limitations` subsection saying no limitations are known
5. `## Security Configuration`, from `security-config.template.md`, placed right after Code Intelligence:
   - `### Product Lifecycle`: 4 required fields plus the VEX field (customfield_12345). The other optional fields are left blank.
   - `### Version Streams`: 2.1.x row
   - `### Source Repositories`: backend and frontend-ui, both with deployment context `upstream` (the default)
6. `## Bug Configuration`: 10001 / docs/bug-template.md / Blocks
7. `## Hierarchy Configuration`: Default epic grouping strategy `by-repository` (assumed: the recommended option for multi-repo projects, because the eval gave no choice)

## Not written (simulation / user choice)

- `docs/constraints.md` (Step 7): not copied, simulation only
- `CONVENTIONS.md` in backend and frontend-ui (Step 8): not scaffolded
- `docs/bug-template.md` (Step 9.4): copy skipped per instructions
- `security-matrix.md` (Step 10.5): scaffolding skipped by the user
- Supportability Matrix / Container Images population (Step 10.6): declined by the user

No MCP tools were called, no Bash commands were run, and no files outside `outputs/` were changed.
