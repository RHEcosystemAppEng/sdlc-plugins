# Setup Discovery Log

## Step 1 — Read Existing Configuration

Read CLAUDE.md at `evals/setup/files/claude-md-empty.md`. No `# Project Configuration` section found. All sections need to be created.

## Step 2 — Discover Serena Instances

Examined available MCP tools. Identified two Serena instances:

- **serena_backend** — tools: `mcp__serena_backend__find_symbol`, `mcp__serena_backend__get_symbols_overview`, `mcp__serena_backend__search_for_pattern`, etc.
- **serena_ui** — tools: `mcp__serena_ui__find_symbol`, `mcp__serena_ui__get_symbols_overview`, `mcp__serena_ui__search_for_pattern`, etc.

Also discovered an Atlassian MCP server (`mcp__atlassian__*` tools).

User provided repository details:
- serena_backend: repository name = `backend`, role = `Rust backend service`, path = `/home/user/backend`
- serena_ui: repository name = `frontend-ui`, role = `TypeScript frontend`, path = `/home/user/frontend-ui`

## Step 3 — Jira Configuration

No existing Jira Configuration found. User provided all fields manually:

- Project key: TC
- Cloud ID: 2b9e35e3-6bd3-4cec-b838-f4249ee02432
- Feature issue type ID: 10142
- Git Pull Request custom field: customfield_10875
- GitHub Issue custom field: customfield_10747

## Step 5 — Code Intelligence

No existing Code Intelligence section found. Generated section with:
- Naming convention: `mcp__<instance>__<tool>`
- Example using `serena_backend` instance
- Limitations: No known limitations for either serena_backend or serena_ui

## Step 9 — Bug Configuration

No existing Bug Configuration found. Discovered and collected:
- Bug issue type ID: 10001 (discovered from Jira metadata)
- Bug template: docs/bug-template.md (user accepted default path)
- Bug-to-Task link type: Blocks (user accepted default)
- Bug template file copy skipped (simulation)

## Step 10 — Security Configuration

User was asked whether to enable security triage. **User accepted.**

### Step 10.1 — Product Lifecycle fields collected:
- Product pages URL: https://access.example.com/product-lifecycle
- Jira version prefix: MYPRODUCT
- Vulnerability issue type ID: 10200
- Component label pattern: pscomponent:
- VEX Justification custom field: customfield_12345

### Step 10.2 — Version Streams collected:
- Stream: 2.1.x
  - Konflux Release Repo: git.downstream.example.com/my-org/product-release.2.1.z
  - Local Path: /home/user/product-release.2.1.z
  - Security Matrix Path: security-matrix.md

### Step 10.3 — Source Repositories collected:
- backend: https://github.com/example/backend (deployment context: upstream)
- frontend-ui: https://github.com/example/frontend-ui (deployment context: upstream)

### Step 10.5 — security-matrix.md scaffolding:
User skipped security-matrix.md scaffolding.

### Step 10.6 — Supportability matrix population:
User declined supportability matrix population.
