# Changes Log — /sdlc-workflow:setup (simulated)

Target: `evals/setup/files/claude-md-empty.md` (not modified; the result is in `outputs/claude-md-result.md`).

## Preserved (unchanged)

- HTML comment header (`<!-- SYNTHETIC TEST DATA ... -->`)
- `# my-project` heading and its description
- `## Documentation` section (2 links)
- `## Getting Started` section (3 steps)

## Added (appended at end of file)

- `# Project Configuration` heading
- `## Repository Registry` with 2 rows:
  - trustify-backend | Rust backend service | serena_backend | /home/user/trustify-backend
  - trustify-ui | TypeScript frontend | serena_ui | /home/user/trustify-ui
- `## Jira Configuration`: Project key TC, Cloud ID 2b9e35e3-6bd3-4cec-b838-f4249ee02432, Feature issue type ID 10142, Git Pull Request custom field customfield_10875, GitHub Issue custom field customfield_10747
- `### Jira Field Defaults`: Default priority none, fixVersion scope both, Prompt for priority true, Prompt for fixVersion true (skill defaults; the scenario gave no values)
- `## Code Intelligence`: naming convention, `serena_backend` find_symbol example, `### Limitations` (no known limitations for either instance)
- `## Bug Configuration`: Bug issue type ID 10001, Bug template docs/bug-template.md, Bug-to-Task link type Blocks

## Not added

- `## Security Configuration` — user declined security triage.
- `## Hierarchy Configuration` — Jira issue-type hierarchy could not be discovered (no MCP calls) and the scenario gave no grouping strategy, so the skill's conditional scaffold was not triggered.

## Removed / overwritten

- None.

## Side-effect files (skipped in simulation)

- `docs/constraints.md` (from constraints.template.md) — not created
- `docs/bug-template.md` (bug template copy) — skipped as instructed
- `CONVENTIONS.md` in trustify-backend / trustify-ui — not scaffolded
