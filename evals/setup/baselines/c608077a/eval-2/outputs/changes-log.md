# Changes Log

## Added

| Section | Change |
|---|---|
| `## Repository Registry` | New row: `\| trustify-ui \| TypeScript frontend \| serena_ui \| /home/user/trustify-ui \|` |
| `## Code Intelligence` > `### Limitations` | New bullet: `` `serena_ui`: No known limitations `` |

## Kept unchanged

| Section | Notes |
|---|---|
| Content outside Project Configuration (`# trustify-backend`, `## Documentation`) | Not touched |
| `## Repository Registry`: `trustify-backend` row | Kept exactly as it was |
| `## Jira Configuration` (all 5 fields) | Already filled in. Not changed or asked again |
| `## Code Intelligence`: naming convention text and `serena_backend` example | Kept exactly as it was (the example still uses the first Registry instance) |
| `### Limitations`: `serena_backend` entry | Kept exactly as it was |
| `## Bug Configuration` (all 3 fields) | Already filled in. Not changed |

## Not added

| Section | Reason |
|---|---|
| `## Security Configuration` | User declined security triage |
| `### Jira Field Defaults` | Missing from the existing file. It needs MCP discovery of priorities and fixVersions plus user choices, and neither was available in this eval. No values were made up. Run setup again in a live session to add it |
| `## Hierarchy Configuration` | Missing from the existing file. It needs MCP discovery of the issue-type hierarchy plus a user choice of grouping strategy, and neither was available. No values were made up. Pending a live run |

## Removed or overwritten

None.
