# Discovery Log

## MCP Tool Discovery

Source: MCP tool listing (evals/setup/files/mcp-tools-with-serena.md)

### Serena Instances Discovered

1. **serena_backend** — 10 tools detected (find_symbol, get_symbols_overview, search_for_pattern, find_referencing_symbols, replace_symbol_body, insert_after_symbol, insert_before_symbol, rename_symbol, get_diagnostics, list_dir)
2. **serena_ui** — 10 tools detected (find_symbol, get_symbols_overview, search_for_pattern, find_referencing_symbols, replace_symbol_body, insert_after_symbol, insert_before_symbol, rename_symbol, get_diagnostics, list_dir)

### Atlassian MCP Discovered

- Jira tools detected: jira_get_issue, jira_search_issues, jira_edit_issue, jira_transition_issue, jira_add_comment, jira_user_info

## User-Provided Configuration

### Repository Mappings

- serena_backend: repository 'trustify-backend', role 'Rust backend service', path '/home/user/trustify-backend'
- serena_ui: repository 'trustify-ui', role 'TypeScript frontend', path '/home/user/trustify-ui'

### Jira Configuration

- Project key: TC (user-provided)
- Cloud ID: 2b9e35e3-6bd3-4cec-b838-f4249ee02432 (user-provided)
- Feature issue type ID: 10142 (user-provided)
- Git Pull Request custom field: customfield_10875 (user-provided)
- GitHub Issue custom field: customfield_10747 (user-provided)

### Bug Configuration

- Bug issue type ID: 10001 (discovered from Jira metadata)
- Bug template: docs/bug-template.md (user accepted default)
- Bug-to-Task link type: Blocks (user accepted default)

### Serena Limitations

- serena_backend: No known limitations (user-provided)
- serena_ui: No known limitations (user-provided)

### Security Configuration

- User declined to enable security triage — section not generated.
