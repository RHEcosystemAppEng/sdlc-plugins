# Setup Discovery Log

## Step 1 — Read Existing Configuration

- Read CLAUDE.md from `evals/setup/files/claude-md-empty.md`
- No `# Project Configuration` section found
- All sections need to be created from scratch

## Step 2 — Discover Serena Instances

Examined MCP tool listing from `evals/setup/files/mcp-tools-with-serena.md`.

Discovered 2 Serena instances:

1. **serena_backend** — tools: find_symbol, get_symbols_overview, search_for_pattern, find_referencing_symbols, replace_symbol_body, insert_after_symbol, insert_before_symbol, rename_symbol, get_diagnostics, list_dir
2. **serena_ui** — tools: find_symbol, get_symbols_overview, search_for_pattern, find_referencing_symbols, replace_symbol_body, insert_after_symbol, insert_before_symbol, rename_symbol, get_diagnostics, list_dir

User-provided repository details:
- serena_backend: repository='backend', role='Rust backend service', path='/home/user/backend'
- serena_ui: repository='frontend-ui', role='TypeScript frontend', path='/home/user/frontend-ui'
- No known limitations reported for either instance.

## Step 3 — Jira Configuration

Atlassian MCP server detected (tools prefixed with `mcp__atlassian__`). Simulation mode — using user-provided values.

User-provided Jira fields:
- Project key: TC
- Cloud ID: 2b9e35e3-6bd3-4cec-b838-f4249ee02432
- Feature issue type ID: 10142
- Git Pull Request custom field: customfield_10875
- GitHub Issue custom field: customfield_10747

## Step 3.5 — Hierarchy Preferences

Simulation mode — MCP not called for hierarchy discovery. User selected default epic grouping strategy: `by-sub-feature`.

## Step 4 — Jira Field Defaults

Skipped — MCP not available for priority/fixVersion discovery in simulation mode, and no manual values provided.

## Step 5 — Code Intelligence

Generated Code Intelligence section with:
- Tool naming convention: `mcp__<instance>__<tool>`
- Example using first Serena instance: `serena_backend`
- Limitations: None reported for either instance

## Step 7 — Constraints Template

Simulation mode — `docs/constraints.md` copy skipped (would copy from `constraints.template.md`).

## Step 8 — CONVENTIONS.md Scaffold

Simulation mode — CONVENTIONS.md scaffolding skipped for both repositories.

## Step 9 — Bug Configuration

- Bug issue type ID: 10001 (discovered from Jira metadata)
- Bug template path: docs/bug-template.md (user accepted default)
- Bug-to-Task link type: Blocks (user accepted default)
- Bug template file copy: Skipped (simulation mode)

## Step 10 — Security Configuration

User accepted security triage enablement.

### Product Lifecycle fields collected:
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

### Version Streams collected (1 stream):
- 2.1.x: Konflux release repo=git.downstream.example.com/my-org/product-release.2.1.z, local path=/home/user/product-release.2.1.z, security matrix path=security-matrix.md

### Source Repositories collected (2 repos):
- backend: https://github.com/example/backend (deployment context: upstream)
- frontend-ui: https://github.com/example/frontend-ui (deployment context: upstream)

### Optional steps:
- Supportability matrix population: Declined by user
- security-matrix.md scaffolding: Skipped by user
