# Discovery Log

## MCP Tool Discovery

Scanned available MCP tools in the current session.

### Serena Instances

- **serena_backend**: Discovered via `mcp__serena_backend__*` tool prefix. 10 tools available (find_symbol, get_symbols_overview, search_for_pattern, find_referencing_symbols, replace_symbol_body, insert_after_symbol, insert_before_symbol, rename_symbol, get_diagnostics, list_dir).
- **serena_ui**: Discovered via `mcp__serena_ui__*` tool prefix. 10 tools available (find_symbol, get_symbols_overview, search_for_pattern, find_referencing_symbols, replace_symbol_body, insert_after_symbol, insert_before_symbol, rename_symbol, get_diagnostics, list_dir).

### Atlassian MCP

- Discovered Atlassian/Jira integration via `mcp__atlassian__jira_*` tool prefix. 6 tools available (get_issue, search_issues, edit_issue, transition_issue, add_comment, user_info).

## Repository Registry

User provided repository details for each Serena instance:

- **serena_backend** -> repository: backend, role: Rust backend service, path: /home/user/backend
- **serena_ui** -> repository: frontend-ui, role: TypeScript frontend, path: /home/user/frontend-ui

## Jira Configuration

User provided Jira configuration:

- Project key: TC
- Cloud ID: 2b9e35e3-6bd3-4cec-b838-f4249ee02432
- Feature issue type ID: 10142
- Git Pull Request custom field: customfield_10875
- GitHub Issue custom field: customfield_10747

## Code Intelligence Limitations

User confirmed no known limitations for either Serena instance.

## Bug Configuration

- Bug issue type ID: 10001 (discovered from Jira metadata)
- Bug template path: docs/bug-template.md (user accepted default)
- Bug-to-Task link type: Blocks (user accepted default)
- Bug template file copy skipped (simulation mode)

## Security Configuration

- User opted in to security triage configuration when asked.
- Product Lifecycle fields collected from user:
  - Product pages URL: https://access.example.com/product-lifecycle
  - Jira version prefix: MYPRODUCT
  - Vulnerability issue type ID: 10200
  - Component label pattern: pscomponent:
  - VEX Justification custom field: customfield_12345
- Version Streams: 1 stream configured (2.1.x)
  - Konflux release repo: git.downstream.example.com/my-org/product-release.2.1.z
  - Local path: /home/user/product-release.2.1.z
  - Security matrix path: security-matrix.md
- Source Repositories: 2 repos configured (backend, frontend-ui)
  - backend: https://github.com/example/backend (deployment context: upstream)
  - frontend-ui: https://github.com/example/frontend-ui (deployment context: upstream)
- User declined optional supportability matrix population.
- security-matrix.md scaffolding skipped per user request.
