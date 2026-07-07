# Discovery Log

## MCP Tool Discovery

Scanned the available MCP tools in the session. Discovered the following:

### Serena Instances

- **serena_backend** — detected from `mcp__serena_backend__*` tools (10 tools: find_symbol, get_symbols_overview, search_for_pattern, find_referencing_symbols, replace_symbol_body, insert_after_symbol, insert_before_symbol, rename_symbol, get_diagnostics, list_dir)
- **serena_ui** — detected from `mcp__serena_ui__*` tools (10 tools: find_symbol, get_symbols_overview, search_for_pattern, find_referencing_symbols, replace_symbol_body, insert_after_symbol, insert_before_symbol, rename_symbol, get_diagnostics, list_dir)

### Atlassian MCP

- Detected Atlassian/Jira MCP tools: jira_get_issue, jira_search_issues, jira_edit_issue, jira_transition_issue, jira_add_comment, jira_user_info

## Repository Discovery

User provided repository details for each Serena instance:

- **serena_backend**: repository name 'backend', role 'Rust backend service', path '/home/user/backend'
- **serena_ui**: repository name 'frontend-ui', role 'TypeScript frontend', path '/home/user/frontend-ui'

No known limitations reported for either Serena instance.

## Jira Configuration

User provided the following Jira configuration:

- Project key: TC
- Cloud ID: 2b9e35e3-6bd3-4cec-b838-f4249ee02432
- Feature issue type ID: 10142
- Git Pull Request custom field: customfield_10875
- GitHub Issue custom field: customfield_10747

## Bug Configuration

- Bug issue type ID: 10001 (discovered from Jira metadata)
- Bug template path: docs/bug-template.md (user accepted default)
- Bug-to-Task link type: Blocks (user accepted default)

## Security Configuration

User opted in to Security Configuration when asked.

### Product Lifecycle

User provided the following product lifecycle metadata:

- Product pages URL: https://access.example.com/product-lifecycle
- Jira version prefix: MYPRODUCT
- Vulnerability issue type ID: 10200
- Component label pattern: pscomponent:
- VEX Justification custom field: customfield_12345

### Version Streams

User provided one version stream:

- Stream 2.1.x: Konflux release repo at git.downstream.example.com/my-org/product-release.2.1.z, local path /home/user/product-release.2.1.z, security matrix path security-matrix.md

### Source Repositories

User provided two source repositories:

- backend: https://github.com/example/backend
- frontend-ui: https://github.com/example/frontend-ui

User declined optional supportability matrix population and skipped security-matrix.md scaffolding.
