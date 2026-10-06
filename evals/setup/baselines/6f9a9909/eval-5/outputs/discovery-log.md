# Setup Discovery Log

## Step 1 -- Read Existing Configuration

- Read CLAUDE.md from `evals/setup/files/claude-md-empty.md`
- No `# Project Configuration` section found
- All sections need to be created from scratch

## Step 2 -- Discover Serena Instances

- Examined available MCP tools from `evals/setup/files/mcp-tools-with-serena.md`
- Discovered 2 Serena instances:
  - `serena_backend` -- tools: find_symbol, get_symbols_overview, search_for_pattern, find_referencing_symbols, replace_symbol_body, insert_after_symbol, insert_before_symbol, rename_symbol, get_diagnostics, list_dir
  - `serena_ui` -- tools: find_symbol, get_symbols_overview, search_for_pattern, find_referencing_symbols, replace_symbol_body, insert_after_symbol, insert_before_symbol, rename_symbol, get_diagnostics, list_dir
- User provided repository details:
  - serena_backend: repository='backend', role='Rust backend service', path='/home/user/backend'
  - serena_ui: repository='frontend-ui', role='TypeScript frontend', path='/home/user/frontend-ui'

## Step 3 -- Jira Configuration

- Detected Atlassian MCP server (tools prefixed with `mcp__atlassian__`)
- Simulated MCP discovery -- used user-provided values:
  - Project key: TC
  - Cloud ID: 2b9e35e3-6bd3-4cec-b838-f4249ee02432
  - Feature issue type ID: 10142
  - Git Pull Request custom field: customfield_10875
  - GitHub Issue custom field: customfield_10747

## Step 3.5 -- Hierarchy Preferences

- Simulated hierarchy discovery (MCP not called in simulation mode)
- User selected epic grouping strategy: by-sub-feature

## Step 4 -- Jira Field Defaults

- Skipped: MCP discovery not available in simulation mode
- Jira Field Defaults section not scaffolded (requires MCP or REST API to discover available priorities and fixVersions)

## Step 5 -- Code Intelligence

- Generated Code Intelligence section documenting the `mcp__<instance>__<tool>` naming convention
- Used `serena_backend` as the example instance
- User confirmed no known limitations for either Serena instance

## Step 7 -- Constraints Template

- Simulation mode: would copy `constraints.template.md` to `docs/constraints.md` in target project
- Skipped actual file write per simulation instructions

## Step 8 -- CONVENTIONS.md Scaffolding

- Simulation mode: would offer to scaffold CONVENTIONS.md for each repository
- Skipped actual file writes per simulation instructions

## Step 9 -- Bug Configuration

- Discovered Bug issue type ID: 10001 (from Jira metadata)
- User accepted default bug template path: docs/bug-template.md
- User accepted default Bug-to-Task link type: Blocks
- Skipped bug template file copy per simulation instructions

## Step 10 -- Security Configuration

- User accepted enabling security triage
- Collected Product Lifecycle fields:
  - Product pages URL: https://access.example.com/product-lifecycle
  - Jira version prefix: MYPRODUCT
  - Vulnerability issue type ID: 10200
  - Component label pattern: pscomponent:
  - VEX Justification custom field: customfield_12345
  - Upstream Affected Component custom field: (not provided)
  - PS Component custom field: (not provided)
  - Stream custom field: (not provided)
  - ProdSec contact email: (not provided)
  - ProdSec Jira account ID: (not provided)
  - Embargo policy URL: (not provided)
- Collected 1 version stream:
  - 2.1.x: Konflux repo=git.downstream.example.com/my-org/product-release.2.1.z, local path=/home/user/product-release.2.1.z, security matrix=security-matrix.md
- Collected 2 source repositories:
  - backend: https://github.com/example/backend (deployment context: upstream)
  - frontend-ui: https://github.com/example/frontend-ui (deployment context: upstream)
- User declined supportability matrix population
- Skipped security-matrix.md scaffolding

## Step 11 -- Validation

- Verified `# Project Configuration` heading exists
- Verified `## Repository Registry` contains table with correct columns (Repository, Role, Serena Instance, Path) and 2 rows
- Verified `## Jira Configuration` contains all required fields (Project key, Cloud ID, Feature issue type ID) plus optional fields
- Verified `## Code Intelligence` documents `mcp__<instance>__<tool>` naming convention with example
- Verified `## Code Intelligence` has `### Limitations` subheading
- Verified `## Bug Configuration` contains all three required fields (Bug issue type ID, Bug template, Bug-to-Task link type)
- Verified `## Hierarchy Configuration` contains Default epic grouping strategy
- Verified `## Security Configuration` contains `### Product Lifecycle` with all required fields
- Verified `## Security Configuration` contains `### Version Streams` with 1 row
- Verified `## Security Configuration` contains `### Source Repositories` with 2 rows
- All validation checks passed
