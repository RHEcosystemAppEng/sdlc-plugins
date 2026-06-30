# Discovery Log

## MCP Tool Scan

Scanned available MCP tools to discover Serena instances by matching the
`mcp__serena_*` prefix pattern.

### Serena Instances Discovered

| Instance | Tools Found | Status |
|---|---|---|
| serena_backend | 10 | Already configured in Repository Registry |
| serena_ui | 10 | NEW — not yet in Repository Registry |

### serena_backend (already configured)

Tools detected:
- mcp__serena_backend__find_symbol
- mcp__serena_backend__get_symbols_overview
- mcp__serena_backend__search_for_pattern
- mcp__serena_backend__find_referencing_symbols
- mcp__serena_backend__replace_symbol_body
- mcp__serena_backend__insert_after_symbol
- mcp__serena_backend__insert_before_symbol
- mcp__serena_backend__rename_symbol
- mcp__serena_backend__get_diagnostics
- mcp__serena_backend__list_dir

Existing Registry entry found — no action needed.

### serena_ui (new)

Tools detected:
- mcp__serena_ui__find_symbol
- mcp__serena_ui__get_symbols_overview
- mcp__serena_ui__search_for_pattern
- mcp__serena_ui__find_referencing_symbols
- mcp__serena_ui__replace_symbol_body
- mcp__serena_ui__insert_after_symbol
- mcp__serena_ui__insert_before_symbol
- mcp__serena_ui__rename_symbol
- mcp__serena_ui__get_diagnostics
- mcp__serena_ui__list_dir

No existing Registry entry — user provided configuration:
- Repository: trustify-ui
- Role: TypeScript frontend
- Path: /home/user/trustify-ui
- Limitations: None known

### Other MCP Servers Detected

| Server | Status |
|---|---|
| Atlassian MCP | Present (Jira tools available — Jira Configuration already exists) |
