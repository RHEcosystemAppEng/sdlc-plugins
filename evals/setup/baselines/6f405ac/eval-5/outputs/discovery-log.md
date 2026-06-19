# Setup Discovery Log

## Step 1 -- Read Existing Configuration

Read CLAUDE.md (from `evals/setup/files/claude-md-empty.md`). No `# Project Configuration` section found. All sections need to be created.

## Step 2 -- Discover Serena Instances

Examined available MCP tools listing. Discovered two Serena instances:

- **serena_backend** -- tools: `mcp__serena_backend__find_symbol`, `mcp__serena_backend__get_symbols_overview`, `mcp__serena_backend__search_for_pattern`, `mcp__serena_backend__find_referencing_symbols`, `mcp__serena_backend__replace_symbol_body`, `mcp__serena_backend__insert_after_symbol`, `mcp__serena_backend__insert_before_symbol`, `mcp__serena_backend__rename_symbol`, `mcp__serena_backend__get_diagnostics`, `mcp__serena_backend__list_dir`
- **serena_ui** -- tools: `mcp__serena_ui__find_symbol`, `mcp__serena_ui__get_symbols_overview`, `mcp__serena_ui__search_for_pattern`, `mcp__serena_ui__find_referencing_symbols`, `mcp__serena_ui__replace_symbol_body`, `mcp__serena_ui__insert_after_symbol`, `mcp__serena_ui__insert_before_symbol`, `mcp__serena_ui__rename_symbol`, `mcp__serena_ui__get_diagnostics`, `mcp__serena_ui__list_dir`

Also discovered Atlassian MCP server (`mcp__atlassian__*` tools).

User provided repository details:
- serena_backend: repository name = "backend", role = "Rust backend service", path = `/home/user/backend`
- serena_ui: repository name = "frontend-ui", role = "TypeScript frontend", path = `/home/user/frontend-ui`

## Step 3 -- Jira Configuration

No existing Jira Configuration found. User provided all fields manually:
- Project key: TC
- Cloud ID: 2b9e35e3-6bd3-4cec-b838-f4249ee02432
- Feature issue type ID: 10142
- Git Pull Request custom field: customfield_10875
- GitHub Issue custom field: customfield_10747

## Step 4 -- Code Intelligence

No existing Code Intelligence section found. Generated section with:
- Tool naming convention explanation using `serena_backend` as the example instance
- Limitations subsection: user confirmed no known limitations for either instance

## Step 8 -- Bug Configuration

No existing Bug Configuration found. Discovered Bug issue type ID from Jira metadata:
- Bug issue type ID: 10001 (discovered from Jira issue type listing)
- Bug template path: user accepted default `docs/bug-template.md`
- Bug-to-Task link type: user accepted default `Blocks`
- Bug template file copy skipped (simulation mode)

## Step 9 -- Security Configuration

No existing Security Configuration found. User was asked whether to enable security triage -- user accepted.

### Step 9.1 -- Product Lifecycle fields collected from user:
- Product pages URL: https://access.example.com/product-lifecycle
- Jira version prefix: MYPRODUCT
- Vulnerability issue type ID: 10200
- Component label pattern: pscomponent:
- VEX Justification custom field: customfield_12345

### Step 9.2 -- Version Streams collected from user:
- Stream: 2.1.x
  - Konflux Release Repo: git.downstream.example.com/my-org/product-release.2.1.z
  - Local Path: /home/user/product-release.2.1.z
  - Security Matrix Path: security-matrix.md

### Step 9.3 -- Source Repositories collected from user:
- backend: https://github.com/example/backend
- frontend-ui: https://github.com/example/frontend-ui

### Step 9.5 -- Security matrix scaffolding skipped (user declined)

### Step 9.6 -- Supportability matrix population skipped (user declined)
