# Setup Discovery Log

## Step 1 — Read Existing Configuration

- Read CLAUDE.md from `evals/setup/files/claude-md-empty.md`
- No `# Project Configuration` section found — full setup required
- No Repository Registry, Jira Configuration, Code Intelligence, Bug Configuration, Security Configuration, or Hierarchy Configuration sections exist

## Step 2 — Discover Serena Instances

- Examined available MCP tools from `evals/setup/files/mcp-tools-with-serena.md`
- Discovered 2 Serena instances:
  - `serena_backend` — tools: find_symbol, get_symbols_overview, search_for_pattern, find_referencing_symbols, replace_symbol_body, insert_after_symbol, insert_before_symbol, rename_symbol, get_diagnostics, list_dir
  - `serena_ui` — tools: find_symbol, get_symbols_overview, search_for_pattern, find_referencing_symbols, replace_symbol_body, insert_after_symbol, insert_before_symbol, rename_symbol, get_diagnostics, list_dir
- User provided repository details:
  - serena_backend -> repository: 'backend', role: 'Rust backend service', path: '/home/user/backend'
  - serena_ui -> repository: 'frontend-ui', role: 'TypeScript frontend', path: '/home/user/frontend-ui'

## Step 3 — Jira Configuration

- No existing Jira Configuration found
- Atlassian MCP tools detected (mcp__atlassian__jira_get_issue, etc.)
- User provided Jira configuration manually (simulated):
  - Project key: TC
  - Cloud ID: 2b9e35e3-6bd3-4cec-b838-f4249ee02432
  - Feature issue type ID: 10142
  - Git Pull Request custom field: customfield_10875
  - GitHub Issue custom field: customfield_10747

## Step 3.5 — Hierarchy Preferences

- No existing Hierarchy Configuration found
- User selected epic grouping strategy: by-sub-feature

## Step 4 — Jira Field Defaults

- Skipped — MCP tools not available for actual discovery in simulation mode

## Step 5 — Code Intelligence

- No existing Code Intelligence section found
- Generated section documenting `mcp__<instance>__<tool>` naming convention
- Example uses `serena_backend` (first instance from Repository Registry)
- User reported no known limitations for either Serena instance

## Step 7 — Copy Constraints Template

- Skipped — simulation mode (no file writes to project directories)

## Step 8 — Scaffold CONVENTIONS.md

- Skipped — simulation mode (no file writes to project directories)

## Step 9 — Bug Configuration

- No existing Bug Configuration found
- Bug issue type ID: 10001 (discovered from Jira metadata)
- Bug template path: docs/bug-template.md (user accepted default)
- Bug-to-Task link type: Blocks (user accepted default)
- Bug template file copy skipped (simulation)

## Step 10 — Security Configuration

- No existing Security Configuration found
- User accepted when asked whether to enable security triage
- Product Lifecycle fields collected:
  - Product pages URL: https://access.example.com/product-lifecycle
  - Jira version prefix: MYPRODUCT
  - Vulnerability issue type ID: 10200
  - Component label pattern: pscomponent:
  - VEX Justification custom field: customfield_12345
  - Upstream Affected Component custom field: (skipped)
  - PS Component custom field: (skipped)
  - Stream custom field: (skipped)
  - ProdSec contact email: (skipped)
  - ProdSec Jira account ID: (skipped)
  - Embargo policy URL: (skipped)
- Version Streams collected:
  - 2.1.x: Konflux repo=git.downstream.example.com/my-org/product-release.2.1.z, local path=/home/user/product-release.2.1.z, security matrix=security-matrix.md
- Source Repositories collected:
  - backend: https://github.com/example/backend (deployment context: upstream)
  - frontend-ui: https://github.com/example/frontend-ui (deployment context: upstream)
- User declined supportability matrix population
- security-matrix.md scaffolding skipped

## Step 11 — Validation

- `# Project Configuration` heading: present
- `## Repository Registry` table with correct columns (Repository, Role, Serena Instance, Path): present, 2 rows
- `## Jira Configuration` with required fields (Project key, Cloud ID, Feature issue type ID): present
- `## Code Intelligence` with `mcp__<instance>__<tool>` naming convention: present
- `### Limitations` subheading under Code Intelligence: present
- `## Bug Configuration` with all three fields (Bug issue type ID, Bug template, Bug-to-Task link type): present
- `## Security Configuration` with `### Product Lifecycle` and required fields: present
- `### Version Streams` with at least one row: present (1 stream)
- `### Source Repositories` with at least one row: present (2 repositories)
- `## Hierarchy Configuration` with Default epic grouping strategy: present
