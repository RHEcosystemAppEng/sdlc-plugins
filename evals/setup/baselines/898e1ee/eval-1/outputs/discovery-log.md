# Discovery Log

## MCP Tool Discovery

Source: MCP tool listing (simulated from `evals/setup/files/mcp-tools-with-serena.md`)

### Serena Instances Discovered

1. **serena_backend** — discovered from tool prefix `mcp__serena_backend__*` (10 tools found: find_symbol, get_symbols_overview, search_for_pattern, find_referencing_symbols, replace_symbol_body, insert_after_symbol, insert_before_symbol, rename_symbol, get_diagnostics, list_dir)
2. **serena_ui** — discovered from tool prefix `mcp__serena_ui__*` (10 tools found: find_symbol, get_symbols_overview, search_for_pattern, find_referencing_symbols, replace_symbol_body, insert_after_symbol, insert_before_symbol, rename_symbol, get_diagnostics, list_dir)

### Atlassian MCP Discovered

- Atlassian MCP tools found with prefix `mcp__atlassian__jira_*` (6 tools: get_issue, search_issues, edit_issue, transition_issue, add_comment, user_info)

## Repository Mapping (User-Provided)

- **serena_backend** mapped to repository `trustify-backend`, role: Rust backend service, path: `/home/user/trustify-backend`
- **serena_ui** mapped to repository `trustify-ui`, role: TypeScript frontend, path: `/home/user/trustify-ui`

## Jira Configuration (User-Provided)

- Project key: TC
- Cloud ID: 2b9e35e3-6bd3-4cec-b838-f4249ee02432
- Feature issue type ID: 10142
- Git Pull Request custom field: customfield_10875
- GitHub Issue custom field: customfield_10747

## Bug Configuration (Discovered + User-Confirmed)

- Bug issue type ID: 10001 (discovered from Jira metadata)
- Bug template path: docs/bug-template.md (user accepted default)
- Bug-to-Task link type: Blocks (user accepted default)

## Serena Limitations (User-Provided)

- **serena_backend**: No known limitations
- **serena_ui**: No known limitations

## Security Configuration

- User declined to enable security triage for this project — section not included
