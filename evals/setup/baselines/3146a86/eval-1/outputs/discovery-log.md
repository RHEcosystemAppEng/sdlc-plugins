# Discovery Log

## Source

- MCP tools listing: `evals/setup/files/mcp-tools-with-serena.md`
- Existing CLAUDE.md: `evals/setup/files/claude-md-empty.md`

## Serena Instances Discovered

Parsed MCP tool names matching the pattern `mcp__<instance>__<tool>` from the tools listing.

1. **serena_backend** -- discovered from tools prefixed with `mcp__serena_backend__` (10 tools: find_symbol, get_symbols_overview, search_for_pattern, find_referencing_symbols, replace_symbol_body, insert_after_symbol, insert_before_symbol, rename_symbol, get_diagnostics, list_dir)
   - User provided: repository = `trustify-backend`, role = `Rust backend service`, path = `/home/user/trustify-backend`
   - No known limitations reported.

2. **serena_ui** -- discovered from tools prefixed with `mcp__serena_ui__` (10 tools: find_symbol, get_symbols_overview, search_for_pattern, find_referencing_symbols, replace_symbol_body, insert_after_symbol, insert_before_symbol, rename_symbol, get_diagnostics, list_dir)
   - User provided: repository = `trustify-ui`, role = `TypeScript frontend`, path = `/home/user/trustify-ui`
   - No known limitations reported.

## Other MCP Tools Discovered

- **Atlassian MCP** -- 6 tools for Jira integration (jira_get_issue, jira_search_issues, jira_edit_issue, jira_transition_issue, jira_add_comment, jira_user_info)

## Jira Configuration

User provided the following Jira configuration values:
- Project key: TC
- Cloud ID: 2b9e35e3-6bd3-4cec-b838-f4249ee02432
- Feature issue type ID: 10142
- Git Pull Request custom field: customfield_10875
- GitHub Issue custom field: customfield_10747

## Existing CLAUDE.md

The existing CLAUDE.md (`claude-md-empty.md`) contains no Project Configuration section. It has basic project documentation (project name, documentation links, getting started instructions).
