# Discovery Log

## Source

MCP tools listing from the current session.

## Serena Instances Discovered

Two Serena instances were identified from the MCP tool listing by scanning for the `mcp__<instance>__<tool>` naming pattern:

1. **serena_backend** -- found 10 tools (find_symbol, get_symbols_overview, search_for_pattern, find_referencing_symbols, replace_symbol_body, insert_after_symbol, insert_before_symbol, rename_symbol, get_diagnostics, list_dir). User confirmed: repository 'trustify-backend', role 'Rust backend service', path '/home/user/trustify-backend'. No known limitations reported.

2. **serena_ui** -- found 10 tools (find_symbol, get_symbols_overview, search_for_pattern, find_referencing_symbols, replace_symbol_body, insert_after_symbol, insert_before_symbol, rename_symbol, get_diagnostics, list_dir). User confirmed: repository 'trustify-ui', role 'TypeScript frontend', path '/home/user/trustify-ui'. No known limitations reported.

## Atlassian MCP Discovered

Atlassian MCP tools were detected (jira_get_issue, jira_search_issues, jira_edit_issue, jira_transition_issue, jira_add_comment, jira_user_info). User provided Jira configuration: Project key=TC, Cloud ID=2b9e35e3-6bd3-4cec-b838-f4249ee02432, Feature issue type ID=10142, Git Pull Request custom field=customfield_10875, GitHub Issue custom field=customfield_10747.

## Built-in Tools

Standard built-in tools confirmed: Bash, Read, Write, Edit, Glob, Grep.
