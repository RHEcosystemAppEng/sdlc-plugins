# Changes Log — /sdlc-workflow:setup (simulated)

Target: CLAUDE.md (input: `evals/setup/files/claude-md-empty.md`). Result written to `outputs/claude-md-result.md`; no real project files were modified.

## Preserved (unchanged)

- `# my-project` heading and description
- `## Documentation`
- `## Getting Started`

## Added (appended at end of file — no prior `# Project Configuration` existed)

| Section | Change | Details |
|---|---|---|
| `# Project Configuration` | Added | New top-level heading |
| `## Repository Registry` | Added | Empty table (headers only) — no Serena instances; user chose to continue without code intelligence |
| `## Jira Configuration` | Added | Project key `MYPROJ`, Cloud ID `abc123`, Feature issue type ID `10001` (manual entry). Git Pull Request / GitHub Issue custom fields omitted (none provided) |
| `### Jira Field Defaults` | Added | Default priority: none; fixVersion scope: both; Prompt for priority: true; Prompt for fixVersion: true (defaults; discovery unavailable without Atlassian MCP) |
| `## Code Intelligence` | Added | Naming convention `mcp__<instance>__<tool>` with generic example; note that no Serena servers are configured |
| `### Limitations` | Added | "No limitations known — no Serena instances configured." |
| `## Bug Configuration` | Added | Bug issue type ID `10001`; Bug template `docs/bug-template.md`; Bug-to-Task link type `Blocks` |

## Not added / skipped

| Item | Reason |
|---|---|
| `## Hierarchy Configuration` | Issue type hierarchy could not be discovered (no Atlassian MCP, REST declined) and no Epic-level type was confirmed; section not created |
| `## Security Configuration` | User declined security triage |
| `docs/constraints.md` | Would be copied from `constraints.template.md` in a real run; skipped in simulation |
| `docs/bug-template.md` | Would be copied from `docs/templates/bug-template.md` in a real run; skipped per instructions |
| `CONVENTIONS.md` scaffolding | Repository Registry is empty — no repositories to scaffold |
| REST API credentials | Not collected — user chose manual entry |

## External interactions

- MCP tool calls: none
- Bash / REST API calls: none
