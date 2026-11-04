# Changes Log

Applies to the `# Project Configuration` section of the CLAUDE.md in `claude-md-configured.md`. Everything above that section (the `# trustify-backend` heading and the `## Documentation` links) is kept unchanged.

## Added

| Section | Change |
|---|---|
| `## Repository Registry` | New row: `trustify-ui` / `TypeScript frontend` / `serena_ui` / `/home/user/trustify-ui` |
| `## Code Intelligence` > `### Limitations` | New bullet: `` `serena_ui`: No known limitations `` |

## Kept unchanged

| Section | What was kept |
|---|---|
| `## Repository Registry` | The `trustify-backend` row (Rust backend service, `serena_backend`, `/home/user/trustify-backend`) |
| `## Jira Configuration` | All 5 fields: Project key TC, Cloud ID 2b9e35e3-6bd3-4cec-b838-f4249ee02432, Feature issue type ID 10142, Git Pull Request custom field customfield_10875, GitHub Issue custom field customfield_10747 |
| `## Code Intelligence` | Naming-convention text and the `serena_backend` `find_symbol` example. I kept the existing example and did not switch it to the new instance |
| `### Limitations` | `serena_backend`: rust-analyzer may take 30-60 seconds to index on first use |
| `## Bug Configuration` | Bug issue type ID 10001, Bug template docs/bug-template.md, Bug-to-Task link type Blocks |

Nothing was removed or overwritten.

## Not added (skipped on purpose)

| Section | Reason |
|---|---|
| `## Security Configuration` | The user declined to enable security triage |
| `### Jira Field Defaults` | Absent from the existing config. Filling it needs Jira metadata discovery (MCP calls are not allowed here) and user choices that were not provided. Run setup again with Jira access |
| `## Hierarchy Configuration` | Absent from the existing config. Filling it needs Jira issue-type hierarchy discovery and a grouping-strategy choice that was not provided. Run setup again with Jira access |
| `docs/constraints.md`, `CONVENTIONS.md`, bug template file | Writing files is limited to `outputs/`. Steps 7, 8 and 9.4 were not performed |

## Summary

- Sections changed: 2 (Repository Registry, Code Intelligence > Limitations)
- Sections up to date: Jira Configuration, Bug Configuration
- Entries added: 2. Entries removed: 0. Values overwritten: 0
