# Changes Log — /sdlc-workflow:setup (simulated)

Target: `evals/setup/files/claude-md-empty.md`. The real file was not modified. The result is in `outputs/claude-md-result.md`.

Write mode: CLAUDE.md exists but has no `# Project Configuration`, so the section is **appended at the end of the file** (Step 6).

## Preserved (unchanged)

- HTML comment header (synthetic test data marker)
- `# my-project` heading and description ("A web application for managing inventory.")
- `## Documentation`: both links (docs/architecture.md, docs/api.md)
- `## Getting Started`: all 3 steps

No existing content was removed, reordered or rewritten.

## Added

| Section | Content | Source |
|---|---|---|
| `# Project Configuration` | New top-level heading | Template |
| `## Repository Registry` | 2 rows: trustify-backend / Rust backend service / serena_backend / /home/user/trustify-backend; trustify-ui / TypeScript frontend / serena_ui / /home/user/trustify-ui | Serena discovery + user input |
| `## Jira Configuration` | Project key TC; Cloud ID 2b9e35e3-6bd3-4cec-b838-f4249ee02432; Feature issue type ID 10142; Git PR field customfield_10875; GitHub Issue field customfield_10747 | User input |
| `### Jira Field Defaults` | Default priority: none; fixVersion scope: both; Prompt for priority: true; Prompt for fixVersion: true | Skill defaults (nothing discovered) |
| `## Code Intelligence` | `mcp__<instance>__<tool>` convention, example with `serena_backend`, `### Limitations` (none known for either instance) | Template + user input |
| `## Bug Configuration` | Bug issue type ID 10001; Bug template docs/bug-template.md; Bug-to-Task link type Blocks | Jira metadata (simulated) + accepted defaults |

## Not added

- `## Security Configuration`: the user declined security triage.
- `## Hierarchy Configuration`: no issue type hierarchy data was available in the simulation, so no Epic level could be confirmed and no grouping strategy was chosen. A later setup run with Jira access can add it.
- `### REST API Credentials (MCP Fallback)`: REST fallback was not used.

## Side-effect files (skipped in simulation)

- `docs/bug-template.md`: copy from the plugin's `docs/templates/bug-template.md` skipped
- `docs/constraints.md`: not created
- `CONVENTIONS.md` in trustify-backend / trustify-ui: not scaffolded
- security-matrix.md: not applicable (security declined)
