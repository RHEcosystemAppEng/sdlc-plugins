# Setup Discovery Log

## MCP Tool Discovery

### Serena Instances

Discovered 2 Serena instances from the MCP tool listing:

- **serena_backend** — tools prefixed `mcp__serena_backend__*` (e.g., `mcp__serena_backend__find_symbol`, `mcp__serena_backend__get_symbols_overview`, etc.)
- **serena_ui** — tools prefixed `mcp__serena_ui__*` (e.g., `mcp__serena_ui__find_symbol`, `mcp__serena_ui__get_symbols_overview`, etc.)

User provided the following details for each instance:

| Instance | Repository | Role | Path |
|---|---|---|---|
| serena_backend | trustify-backend | Rust backend service | /home/user/trustify-backend |
| serena_ui | trustify-ui | TypeScript frontend | /home/user/trustify-ui |

No known limitations were reported for either instance.

### Atlassian MCP

Atlassian MCP tools were available in the session (`mcp__atlassian__jira_*`), confirming Jira integration is active.

## Jira Configuration

Jira configuration was collected from the user:

- Project key: TC
- Cloud ID: 2b9e35e3-6bd3-4cec-b838-f4249ee02432
- Feature issue type ID: 10142
- Git Pull Request custom field: customfield_10875
- GitHub Issue custom field: customfield_10747

## Bug Configuration

Bug issue type ID 10001 was discovered from Jira metadata. User accepted the default bug template path (`docs/bug-template.md`) and the default Bug-to-Task link type (`Blocks`). Bug template file copy was skipped (simulation).

## Security Configuration

The user was offered Security Configuration opt-in (triage-security skill) and declined. No Security Configuration section was added to CLAUDE.md.
