# Discovery Log

## Source: MCP Tool Listing (mcp-tools-with-serena.md)

### Serena Instances Discovered

1. **serena_backend** -- identified from tools prefixed with `mcp__serena_backend__` (find_symbol, get_symbols_overview, search_for_pattern, find_referencing_symbols, replace_symbol_body, insert_after_symbol, insert_before_symbol, rename_symbol, get_diagnostics, list_dir)
2. **serena_ui** -- identified from tools prefixed with `mcp__serena_ui__` (find_symbol, get_symbols_overview, search_for_pattern, find_referencing_symbols, replace_symbol_body, insert_after_symbol, insert_before_symbol, rename_symbol, get_diagnostics, list_dir)

### Atlassian MCP Discovered

- Atlassian MCP server detected from tools prefixed with `mcp__atlassian__` (jira_get_issue, jira_search_issues, jira_edit_issue, jira_transition_issue, jira_add_comment, jira_user_info)

## Source: User Input

### Repository Details (per Serena instance)

- **serena_backend**: repository name = 'trustify-backend', role = 'Rust backend service', path = '/home/user/trustify-backend'
- **serena_ui**: repository name = 'trustify-ui', role = 'TypeScript frontend', path = '/home/user/trustify-ui'

### Jira Configuration

- Project key: TC (user-provided)
- Cloud ID: 2b9e35e3-6bd3-4cec-b838-f4249ee02432 (user-provided)
- Feature issue type ID: 10142 (user-provided)
- Git Pull Request custom field: customfield_10875 (user-provided)
- GitHub Issue custom field: customfield_10747 (user-provided)

### Serena Limitations

- No known limitations reported by user for either serena_backend or serena_ui.

## Source: Existing CLAUDE.md (claude-md-empty.md)

- No `# Project Configuration` section found -- greenfield setup required.
- No `## Repository Registry` found.
- No `## Jira Configuration` found.
- No `## Code Intelligence` found.
