# Changes Log — /sdlc-workflow:setup (simulated)

Target: CLAUDE.md (input `evals/setup/files/claude-md-empty.md`). Result written to `outputs/claude-md-result.md`.

## Added

A new `# Project Configuration` section was appended at the end of the file. All existing content (title, description, Documentation, Getting Started) was kept unchanged.

| Section | Change | Details |
|---|---|---|
| `## Repository Registry` | Added | Headers-only table (no Serena instances; the user continued without code intelligence) |
| `## Jira Configuration` | Added | Project key `MYPROJ`, Cloud ID `abc123`, Feature issue type ID `10001` (manual entry). No custom field lines, because none were provided |
| `### Jira Field Defaults` | Added | Default priority `none`, fixVersion scope `both`, Prompt for priority `true`, Prompt for fixVersion `true` (defaults, since no discovery was possible) |
| `## Code Intelligence` | Added | Naming convention `mcp__<instance>__<tool>` with a generic example, a note that no Serena servers are configured, and `### Limitations` (none known) |
| `## Bug Configuration` | Added | Bug issue type ID `10001`, Bug template `docs/bug-template.md`, Bug-to-Task link type `Blocks` |

## Not Added / Skipped

| Item | Reason |
|---|---|
| `## Hierarchy Configuration` | The issue type hierarchy couldn't be discovered (no Atlassian MCP, REST fallback declined) and no Epic-level type was provided |
| `## Security Configuration` | The user declined security triage |
| `docs/constraints.md` copy | Simulation: no files written outside outputs/ |
| `docs/bug-template.md` copy | Simulation: skipped as instructed |
| CONVENTIONS.md scaffolding | Repository Registry is empty |

## Modified / Removed

None.
