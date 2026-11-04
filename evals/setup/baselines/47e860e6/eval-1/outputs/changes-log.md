# Changes Log — /sdlc-workflow:setup (simulation)

The target CLAUDE.md (`claude-md-empty.md`) had no `# Project Configuration` section. Under Step 6, the new section was **appended at the end of the file**. Nothing already in the file was changed or removed.

## Preserved (unchanged, pre-existing content)

- HTML comment header (synthetic test data marker)
- `# my-project` heading and its description ("A web application for managing inventory.")
- `## Documentation` section (links to docs/architecture.md and docs/api.md)
- `## Getting Started` section (3 steps)

## Added (new)

| Section | Status | Details |
|---|---|---|
| `# Project Configuration` | Added | New top-level heading appended at the end of the file |
| `## Repository Registry` | Added | 2 rows: `trustify-backend` (Rust backend service, serena_backend, /home/user/trustify-backend) and `trustify-ui` (TypeScript frontend, serena_ui, /home/user/trustify-ui) |
| `## Jira Configuration` | Added | All 5 fields: Project key TC, Cloud ID 2b9e35e3-6bd3-4cec-b838-f4249ee02432, Feature issue type ID 10142, Git Pull Request custom field customfield_10875, GitHub Issue custom field customfield_10747 |
| `### Jira Field Defaults` | Added | The skill's defaults: priority none, fixVersion scope both, prompt for priority true, prompt for fixVersion true |
| `## Code Intelligence` | Added | `mcp__<instance>__<tool>` naming convention, a `find_symbol` example on `serena_backend`, and a `### Limitations` subsection saying no limitations are known for serena_backend or serena_ui |
| `## Bug Configuration` | Added | Bug issue type ID 10001, Bug template docs/bug-template.md, Bug-to-Task link type Blocks |

## Not added / skipped

| Item | Reason |
|---|---|
| `## Security Configuration` | The skill showed the opt-in prompt and the user **declined** |
| `## Hierarchy Configuration` | No issue type hierarchy metadata was available (no MCP calls allowed, and no Epic-level type or grouping strategy was provided), so the section was not created |
| Bug template file copy (`docs/bug-template.md`) | Skipped, as the task instructed for this simulation |
| `docs/constraints.md` (Step 7) | Not written. This is a simulation and only `outputs/` could be written |
| `CONVENTIONS.md` scaffolding (Step 8) | Not done. This is a simulation and only `outputs/` could be written |

## Modified

- None. No existing entries were overwritten or removed.
