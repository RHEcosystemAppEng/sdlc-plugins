# Discovery Log

## Serena Instance Discovery

Examined the available MCP tools listing (`mcp-tools-with-serena.md`) for Serena instances using the `mcp__<instance>__<tool>` naming pattern.

**Discovered 2 Serena instances:**

1. **serena_backend** — identified from tools prefixed with `mcp__serena_backend__` (find_symbol, get_symbols_overview, search_for_pattern, etc.)
   - User-provided repository name: `backend`
   - Role: Rust backend service
   - Path: `/home/user/backend`
   - Limitations: None known

2. **serena_ui** — identified from tools prefixed with `mcp__serena_ui__` (find_symbol, get_symbols_overview, search_for_pattern, etc.)
   - User-provided repository name: `frontend-ui`
   - Role: TypeScript frontend
   - Path: `/home/user/frontend-ui`
   - Limitations: None known

## Atlassian MCP Discovery

Atlassian MCP tools were detected in the tool listing (prefixed with `mcp__atlassian__`). Jira configuration fields were provided by the user.

## Jira Configuration

All five Jira fields provided by the user:
- Project key: TC
- Cloud ID: 2b9e35e3-6bd3-4cec-b838-f4249ee02432
- Feature issue type ID: 10142
- Git Pull Request custom field: customfield_10875
- GitHub Issue custom field: customfield_10747

## Bug Configuration

Bug issue type ID (10001) discovered from Jira metadata. User accepted default bug template path (`docs/bug-template.md`) and default Bug-to-Task link type (`Blocks`).

## Security Configuration

Security Configuration was **opted in** by the user when prompted.

Fields collected:
- **Product Lifecycle**: Product pages URL, Jira version prefix (MYPRODUCT), Vulnerability issue type ID (10200), Component label pattern (pscomponent:), VEX Justification custom field (customfield_12345)
- **Version Streams**: 1 stream configured — 2.1.x with Konflux release repo at git.downstream.example.com/my-org/product-release.2.1.z
- **Source Repositories**: 2 repositories configured — backend (https://github.com/example/backend) and frontend-ui (https://github.com/example/frontend-ui)
- User declined optional supportability matrix population
- User skipped security-matrix.md scaffolding
