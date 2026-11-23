# Changes Log — /sdlc-workflow:setup

## Added

### Repository Registry — new row
```
| trustify-ui | TypeScript frontend | serena_ui | /home/user/trustify-ui |
```
Source: `serena_ui` discovered in MCP tool listing, not previously in the Registry.

### Code Intelligence > Limitations — new entry
```
- `serena_ui`: No known limitations
```

## Preserved (unchanged)

- File preamble: synthetic-data comment, `# trustify-backend` heading, `## Documentation` links
- Repository Registry row: `trustify-backend | Rust backend service | serena_backend | /home/user/trustify-backend`
- Jira Configuration: Project key `TC`, Cloud ID `2b9e35e3-6bd3-4cec-b838-f4249ee02432`,
  Feature issue type ID `10142`, Git PR field `customfield_10875`, GitHub Issue field `customfield_10747`
- Code Intelligence: naming convention text and `serena_backend` find_symbol example
- Limitations entry: `serena_backend`: rust-analyzer may take 30-60 seconds to index on first use
- Bug Configuration: Bug issue type ID `10001`, template `docs/bug-template.md`, link type `Blocks`

## Not Added

- `## Security Configuration` — user declined security triage (Step 10, labelled Step 9 in the task)
- `### Jira Field Defaults` — missing from existing config; discovery needs Jira MCP
  metadata calls (prohibited here) and no user values were provided. Deferred.
- `## Hierarchy Configuration` — missing from existing config; same reason. Deferred.

## Removed / Overwritten

None.
