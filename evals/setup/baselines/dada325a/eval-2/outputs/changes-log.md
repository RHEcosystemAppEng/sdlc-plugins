# Changes Log — Project Configuration update

The update was incremental and idempotent. Nothing existing was removed or overwritten.

## Added

| Section | Change |
|---|---|
| `## Repository Registry` | New row: `\| trustify-ui \| TypeScript frontend \| serena_ui \| /home/user/trustify-ui \|` |
| `## Code Intelligence` > `### Limitations` | New line: `` - `serena_ui`: No known limitations `` |

## Preserved (unchanged)

| Section | Content kept |
|---|---|
| File preamble | `# trustify-backend` heading and the `## Documentation` links (architecture.md, api.md) |
| `## Repository Registry` | Existing `trustify-backend` / Rust backend service / `serena_backend` / `/home/user/trustify-backend` row |
| `## Jira Configuration` | Project key TC, Cloud ID 2b9e35e3-6bd3-4cec-b838-f4249ee02432, Feature issue type ID 10142, Git Pull Request custom field customfield_10875, GitHub Issue custom field customfield_10747 |
| `## Code Intelligence` | Naming-convention text and the `serena_backend` `find_symbol` example |
| `### Limitations` | `serena_backend`: rust-analyzer may take 30-60 seconds to index on first use |
| `## Bug Configuration` | Bug issue type ID 10001, Bug template docs/bug-template.md, Bug-to-Task link type Blocks |

## Not added

| Section | Reason |
|---|---|
| `## Security Configuration` | The user declined to enable security triage (Step 10) |
| `### Jira Field Defaults` | Missing from the existing config, but setting it up needs Jira metadata discovery (MCP calls forbidden here) and no user answers were provided. Deferred to a later setup run with Jira access. |
| `## Hierarchy Configuration` | Missing from the existing config, but setting it up needs issue-type hierarchy discovery (MCP calls forbidden here) and no grouping strategy was provided. Deferred to a later setup run with Jira access. |

## Summary

- Sections modified: 2 (Repository Registry, Code Intelligence > Limitations)
- Sections unchanged: Jira Configuration, Bug Configuration, Code Intelligence body, file preamble
- Lines removed or overwritten: 0
