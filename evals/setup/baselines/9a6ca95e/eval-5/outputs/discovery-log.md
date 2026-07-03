# Setup Discovery Log

## Step 1 — Read Existing Configuration

- Read CLAUDE.md from `evals/setup/files/claude-md-empty.md`
- No `# Project Configuration` section found
- No `## Repository Registry` found
- No `## Jira Configuration` found
- No `## Code Intelligence` found
- No `## Bug Configuration` found
- No `## Security Configuration` found
- No `## Hierarchy Configuration` found
- Result: All sections need to be created from scratch

## Step 2 — Discover Serena Instances

- Examined MCP tool listing from `evals/setup/files/mcp-tools-with-serena.md`
- Discovered 2 Serena instances by scanning for `mcp__<instance>__<tool>` naming pattern:
  - `serena_backend` — tools: find_symbol, get_symbols_overview, search_for_pattern, find_referencing_symbols, replace_symbol_body, insert_after_symbol, insert_before_symbol, rename_symbol, get_diagnostics, list_dir
  - `serena_ui` — tools: find_symbol, get_symbols_overview, search_for_pattern, find_referencing_symbols, replace_symbol_body, insert_after_symbol, insert_before_symbol, rename_symbol, get_diagnostics, list_dir
- User provided repository details:
  - serena_backend: repository='backend', role='Rust backend service', path='/home/user/backend'
  - serena_ui: repository='frontend-ui', role='TypeScript frontend', path='/home/user/frontend-ui'

## Step 3 — Jira Configuration

- Detected Atlassian MCP server (tools prefixed with `mcp__atlassian__`)
- Simulated discovery — used user-provided values:
  - Project key: TC
  - Cloud ID: 2b9e35e3-6bd3-4cec-b838-f4249ee02432
  - Feature issue type ID: 10142
  - Git Pull Request custom field: customfield_10875
  - GitHub Issue custom field: customfield_10747

## Step 3.5 — Hierarchy Preferences

- Simulated hierarchy discovery via Atlassian MCP
- User selected grouping strategy: by-sub-feature

## Step 4 — Jira Field Defaults

- Skipped: MCP discovery not available in simulation mode and no user inputs provided for priority/fixVersion defaults

## Step 5 — Code Intelligence

- Generated Code Intelligence section for 2 Serena instances: serena_backend, serena_ui
- Tool naming convention documented: `mcp__<instance>__<tool>`
- Example uses first Serena instance: serena_backend
- User confirmed no known limitations for either instance

## Step 9 — Bug Configuration

- Bug issue type ID discovered from Jira metadata (simulated): 10001
- User accepted default bug template path: docs/bug-template.md
- User accepted default Bug-to-Task link type: Blocks
- Bug template file copy skipped (simulation mode)

## Step 10 — Security Configuration

- User accepted security triage enablement
- Product Lifecycle fields collected:
  - Product pages URL: https://access.example.com/product-lifecycle
  - Jira version prefix: MYPRODUCT
  - Vulnerability issue type ID: 10200
  - Component label pattern: pscomponent:
  - VEX Justification custom field: customfield_12345
  - Upstream Affected Component custom field: skipped
  - PS Component custom field: skipped
  - Stream custom field: skipped
  - ProdSec contact email: skipped
  - ProdSec Jira account ID: skipped
  - Embargo policy URL: skipped
- Version Streams collected (1 stream):
  - 2.1.x: Konflux repo=git.downstream.example.com/my-org/product-release.2.1.z, local=/home/user/product-release.2.1.z, matrix=security-matrix.md
- Source Repositories collected (2 repos):
  - backend: https://github.com/example/backend (upstream)
  - frontend-ui: https://github.com/example/frontend-ui (upstream)
- User declined supportability matrix population
- security-matrix.md scaffolding skipped
