# Changes Log — Project Configuration

## Added

| Section | Change |
|---|---|
| `## Repository Registry` | New row: `\| trustify-ui \| TypeScript frontend \| serena_ui \| /home/user/trustify-ui \|` |
| `## Code Intelligence` > `### Limitations` | New line: `` `serena_ui`: no known limitations `` |

## Preserved (unchanged, word for word)

| Section | Content kept |
|---|---|
| Content outside Project Configuration | `# trustify-backend` heading and `## Documentation` links (not rewritten; only the Project Configuration section is shown in the result file) |
| `## Repository Registry` | Existing `trustify-backend` / Rust backend service / `serena_backend` / `/home/user/trustify-backend` row |
| `## Jira Configuration` | Project key TC, Cloud ID 2b9e35e3-6bd3-4cec-b838-f4249ee02432, Feature issue type ID 10142, Git Pull Request field customfield_10875, GitHub Issue field customfield_10747 |
| `## Code Intelligence` | Naming-convention text and the `mcp__serena_backend__find_symbol(...)` example (still uses the first Registry instance) |
| `### Limitations` | `serena_backend`: rust-analyzer may take 30-60 seconds to index on first use |
| `## Bug Configuration` | Bug issue type ID 10001, Bug template docs/bug-template.md, Bug-to-Task link type Blocks |

## Not added

| Section | Reason |
|---|---|
| `## Security Configuration` | The user declined to enable security triage (Step 10 of SKILL.md; the task brief calls it "Step 9"). |
| `## Hierarchy Configuration` | Missing from the existing config. Discovery needs `getJiraProjectIssueTypesMetadata`, which is not in the MCP tool listing, and MCP calls are not allowed in this eval. No user answer for the grouping strategy was given, so no value was made up. Run setup again with Jira access to configure it. |
| `### Jira Field Defaults` | Missing from the existing config. Discovery needs `getJiraIssueTypeMetaWithFields`, which is not available, and no user answers for the defaults were given. Left out instead of guessing. Run setup again to configure it. |

## Removed / Overwritten

None. No existing entry was removed or changed.

## Summary

Incremental update. 1 Serena instance was newly discovered (`serena_ui`) and registered. 1 existing instance (`serena_backend`) was preserved. Jira and Bug Configuration are up to date. Security triage was declined.
