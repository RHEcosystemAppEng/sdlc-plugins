# Setup Discovery Log

## Step 1 — Read Existing Configuration

- Read CLAUDE.md from `evals/setup/files/claude-md-empty.md`
- No `# Project Configuration` section found
- All sections need to be created from scratch

## Step 2 — Discover Serena Instances

- Examined available MCP tools listing from `evals/setup/files/mcp-tools-with-serena.md`
- Discovered 2 Serena instances:
  - `serena_backend` — tools: find_symbol, get_symbols_overview, search_for_pattern, find_referencing_symbols, replace_symbol_body, insert_after_symbol, insert_before_symbol, rename_symbol, get_diagnostics, list_dir
  - `serena_ui` — tools: find_symbol, get_symbols_overview, search_for_pattern, find_referencing_symbols, replace_symbol_body, insert_after_symbol, insert_before_symbol, rename_symbol, get_diagnostics, list_dir
- User provided repository details:
  - `serena_backend` -> repository: backend, role: Rust backend service, path: /home/user/backend
  - `serena_ui` -> repository: frontend-ui, role: TypeScript frontend, path: /home/user/frontend-ui

## Step 3 — Jira Configuration

- Atlassian MCP server detected (tools prefixed with `mcp__atlassian__`)
- Simulated: skipping actual MCP calls per eval instructions
- User provided Jira configuration manually:
  - Project key: TC
  - Cloud ID: 2b9e35e3-6bd3-4cec-b838-f4249ee02432
  - Feature issue type ID: 10142
  - Git Pull Request custom field: customfield_10875
  - GitHub Issue custom field: customfield_10747

## Step 3.5 — Hierarchy Preferences

- No existing Hierarchy Configuration found
- Simulated: hierarchy discovery skipped (no actual MCP calls)
- Default epic grouping strategy set to: by-sub-feature

## Step 4 — Jira Field Defaults

- Skipped: MCP calls not available in simulation mode
- Jira Field Defaults subsection not scaffolded (requires MCP or REST API discovery of available priorities and fixVersions)

## Step 5 — Code Intelligence

- Generated Code Intelligence section for 2 Serena instances
- Example uses `serena_backend` (first instance in Repository Registry)
- User confirmed no known limitations for either instance

## Step 7 — Copy Constraints Template

- Simulated: would copy `constraints.template.md` to `docs/constraints.md` in target project
- Skipped file write per eval instructions (simulation only)

## Step 8 — Scaffold CONVENTIONS.md

- Simulated: would offer to scaffold CONVENTIONS.md for each repository
  - backend at /home/user/backend/CONVENTIONS.md
  - frontend-ui at /home/user/frontend-ui/CONVENTIONS.md
- Skipped file write per eval instructions (simulation only)

## Step 9 — Bug Configuration

- Bug issue type ID: 10001 (discovered from Jira metadata)
- Bug template path: docs/bug-template.md (user accepted default)
- Bug-to-Task link type: Blocks (user accepted default)
- Bug template file copy skipped per eval instructions (simulation)

## Step 10 — Security Configuration

- User accepted security triage enablement
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
- Version Streams:
  - 2.1.x: Konflux repo=git.downstream.example.com/my-org/product-release.2.1.z, local path=/home/user/product-release.2.1.z, security matrix=security-matrix.md
- Source Repositories:
  - backend: https://github.com/example/backend
  - frontend-ui: https://github.com/example/frontend-ui
- User declined supportability matrix population
- User skipped security-matrix.md scaffolding

## Step 11 — Validation

- `# Project Configuration` heading: present
- `## Repository Registry` table: present with 2 rows (backend, frontend-ui)
- `## Jira Configuration`: present with all required fields (Project key, Cloud ID, Feature issue type ID) plus optional fields
- `## Code Intelligence`: present with `mcp__<instance>__<tool>` naming convention documented
- `### Limitations` subheading: present under Code Intelligence
- `## Bug Configuration`: present with all three fields (Bug issue type ID, Bug template, Bug-to-Task link type)
- `## Security Configuration`: present
  - `### Product Lifecycle`: present with all required fields
  - `### Version Streams`: present with 1 row
  - `### Source Repositories`: present with 2 rows
- `## Hierarchy Configuration`: present with Default epic grouping strategy
