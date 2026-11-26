# Changes Log

## Added

| Section | Change |
|---|---|
| `## Repository Registry` | New row: `\| trustify-ui \| TypeScript frontend \| serena_ui \| /home/user/trustify-ui \|` |
| `## Code Intelligence` > `### Limitations` | New line: `` - `serena_ui`: No known limitations `` |

## Preserved (unchanged)

- The content before `# Project Configuration`: the `# trustify-backend` heading and the `## Documentation` links.
- Repository Registry row: `trustify-backend | Rust backend service | serena_backend | /home/user/trustify-backend`.
- Jira Configuration: Project key TC, Cloud ID 2b9e35e3-6bd3-4cec-b838-f4249ee02432, Feature issue type ID 10142, Git Pull Request custom field customfield_10875, GitHub Issue custom field customfield_10747.
- Code Intelligence: the naming-convention text and the `serena_backend` find_symbol example.
- Code Intelligence > Limitations: `serena_backend`: rust-analyzer may take 30-60 seconds to index on first use.
- Bug Configuration: Bug issue type ID 10001, template docs/bug-template.md, link type Blocks.

## Not added

| Section | Reason |
|---|---|
| `## Security Configuration` | The user declined to enable security triage. |
| `### Jira Field Defaults` | Missing from the input. Setting it up needs `getJiraIssueTypeMetaWithFields`, which is not in the tool list and is not allowed to be called here. The task also gives no user answers. Deferred, with no values made up. |
| `## Hierarchy Configuration` | Missing from the input. Setting it up needs `getJiraProjectIssueTypesMetadata` plus a grouping strategy from the user, and neither is available. Deferred, with no values made up. |

## Removed / Overwritten

None.
