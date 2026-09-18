# Discovery Log

## Serena Instances

Discovered 2 Serena MCP server instances from the available MCP tool listing:

1. **serena_backend** -- identified from tools prefixed with `mcp__serena_backend__` (10 tools: find_symbol, get_symbols_overview, search_for_pattern, find_referencing_symbols, replace_symbol_body, insert_after_symbol, insert_before_symbol, rename_symbol, get_diagnostics, list_dir)
2. **serena_ui** -- identified from tools prefixed with `mcp__serena_ui__` (10 tools: find_symbol, get_symbols_overview, search_for_pattern, find_referencing_symbols, replace_symbol_body, insert_after_symbol, insert_before_symbol, rename_symbol, get_diagnostics, list_dir)

Source: MCP tool listing in `mcp-tools-with-serena.md`

## Repository Details

Collected from user input for each discovered Serena instance:

1. **serena_backend** -> repository `trustify-backend`, role "Rust backend service", path `/home/user/trustify-backend`
2. **serena_ui** -> repository `trustify-ui`, role "TypeScript frontend", path `/home/user/trustify-ui`

Source: user-provided

## Atlassian MCP

Discovered Atlassian MCP server from tools prefixed with `mcp__atlassian__` (6 tools: jira_get_issue, jira_search_issues, jira_edit_issue, jira_transition_issue, jira_add_comment, jira_user_info).

Source: MCP tool listing in `mcp-tools-with-serena.md`

## Jira Configuration

All Jira fields collected from user input:

- Project key: TC
- Cloud ID: 2b9e35e3-6bd3-4cec-b838-f4249ee02432
- Feature issue type ID: 10142
- Git Pull Request custom field: customfield_10875
- GitHub Issue custom field: customfield_10747

Source: user-provided

## Bug Configuration

- Bug issue type ID: 10001 -- discovered from Jira metadata (issue types listing)
- Bug template path: docs/bug-template.md -- user accepted default
- Bug-to-Task link type: Blocks -- user accepted default

Source: Jira metadata (Bug issue type ID), user-provided defaults (template path, link type)

## Code Intelligence Limitations

- serena_backend: no known limitations (user confirmed)
- serena_ui: no known limitations (user confirmed)

Source: user-provided

## Security Configuration

User declined to enable security triage for this project. Section not created.

Source: user-provided
