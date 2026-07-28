# Discovery Log

## Serena Instances

Discovered 2 Serena instances from MCP tool listing:

1. **serena_backend** -- identified by tools matching pattern `mcp__serena_backend__*` (10 tools: find_symbol, get_symbols_overview, search_for_pattern, find_referencing_symbols, replace_symbol_body, insert_after_symbol, insert_before_symbol, rename_symbol, get_diagnostics, list_dir)
2. **serena_ui** -- identified by tools matching pattern `mcp__serena_ui__*` (10 tools: find_symbol, get_symbols_overview, search_for_pattern, find_referencing_symbols, replace_symbol_body, insert_after_symbol, insert_before_symbol, rename_symbol, get_diagnostics, list_dir)

## Atlassian MCP

Discovered Atlassian MCP server from tool listing -- tools matching pattern `mcp__atlassian__*` (6 tools: jira_get_issue, jira_search_issues, jira_edit_issue, jira_transition_issue, jira_add_comment, jira_user_info).

## Repository Mapping (from user)

- serena_backend -> repository 'trustify-backend', role 'Rust backend service', path '/home/user/trustify-backend'
- serena_ui -> repository 'trustify-ui', role 'TypeScript frontend', path '/home/user/trustify-ui'

## Jira Configuration (from user)

- Project key: TC
- Cloud ID: 2b9e35e3-6bd3-4cec-b838-f4249ee02432
- Feature issue type ID: 10142
- Git Pull Request custom field: customfield_10875
- GitHub Issue custom field: customfield_10747

## Bug Configuration

- Bug issue type ID: 10001 (discovered from Jira metadata)
- Bug template path: docs/bug-template.md (user accepted default)
- Bug-to-Task link type: Blocks (user accepted default)

## Code Intelligence Limitations

- No known limitations reported for either Serena instance.

## Security Configuration

- User declined to enable security triage for this project. Section not created.
