# Discovery Log

## Source

MCP tools listing from the current session.

## Serena Instances Discovered

### serena_backend (already configured)

- Found via MCP tool prefix: `mcp__serena_backend__*`
- Tools detected: find_symbol, get_symbols_overview, search_for_pattern, find_referencing_symbols, replace_symbol_body, insert_after_symbol, insert_before_symbol, rename_symbol, get_diagnostics, list_dir
- Status: Already present in Repository Registry as `trustify-backend` (Rust backend service) at `/home/user/trustify-backend`
- Action: No changes needed; preserved existing entry.

### serena_ui (newly discovered)

- Found via MCP tool prefix: `mcp__serena_ui__*`
- Tools detected: find_symbol, get_symbols_overview, search_for_pattern, find_referencing_symbols, replace_symbol_body, insert_after_symbol, insert_before_symbol, rename_symbol, get_diagnostics, list_dir
- Status: Not present in the existing Repository Registry.
- User-provided details: repository `trustify-ui`, role `TypeScript frontend`, path `/home/user/trustify-ui`, no known limitations.
- Action: Added to Repository Registry and Code Intelligence sections.

## Other MCP Servers Detected

### Atlassian MCP

- Tools detected: jira_get_issue, jira_search_issues, jira_edit_issue, jira_transition_issue, jira_add_comment, jira_user_info
- Status: Jira Configuration already present in Project Configuration.
- Action: No changes needed; preserved existing Jira Configuration.
