# Discovery Log

## Source

Simulated MCP tool listing from `mcp-tools-with-serena.md`.

### Serena Instances Discovered

Scanned tool listing for tools matching the `mcp__<instance>__<tool>` naming pattern.

1. **serena_backend** — identified from tool prefix `mcp__serena_backend__*` (10 tools: find_symbol, get_symbols_overview, search_for_pattern, find_referencing_symbols, replace_symbol_body, insert_after_symbol, insert_before_symbol, rename_symbol, get_diagnostics, list_dir)
2. **serena_ui** — identified from tool prefix `mcp__serena_ui__*` (10 tools: find_symbol, get_symbols_overview, search_for_pattern, find_referencing_symbols, replace_symbol_body, insert_after_symbol, insert_before_symbol, rename_symbol, get_diagnostics, list_dir)

Total Serena instances discovered: **2**

### Atlassian MCP

Atlassian MCP tools detected (prefix `mcp__atlassian__`): jira_get_issue, jira_search_issues, jira_edit_issue, jira_transition_issue, jira_add_comment, jira_user_info.

Jira Configuration fields provided by user (simulated):
- Project key: TC
- Cloud ID: 2b9e35e3-6bd3-4cec-b838-f4249ee02432
- Feature issue type ID: 10142
- Git Pull Request custom field: customfield_10875
- GitHub Issue custom field: customfield_10747

### Repository Details (User-Provided)

- serena_backend → repository 'trustify-backend', role 'Rust backend service', path '/home/user/trustify-backend'
- serena_ui → repository 'trustify-ui', role 'TypeScript frontend', path '/home/user/trustify-ui'

### Limitations

User reported no known limitations for either Serena instance.

### Bug Configuration

Bug issue type ID 10001 discovered from Jira metadata. User accepted default bug template path (docs/bug-template.md) and default Bug-to-Task link type (Blocks).

### Security Configuration

User declined to enable security triage for this project.
