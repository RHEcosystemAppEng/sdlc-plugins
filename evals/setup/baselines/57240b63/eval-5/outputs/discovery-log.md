# Setup Discovery Log

## Step 1 -- Read Existing Configuration

Read `claude-md-empty.md`. No `# Project Configuration` section found. All sections need to be created from scratch.

Pre-existing content preserved:
- `# my-project` heading and description
- `## Documentation` section with architecture and API links
- `## Getting Started` section with setup instructions

## Step 2 -- Discover Serena Instances

Examined available MCP tools for Serena instances. Discovered 2 Serena instances:

1. **serena_backend** -- Tools: find_symbol, get_symbols_overview, search_for_pattern, find_referencing_symbols, replace_symbol_body, insert_after_symbol, insert_before_symbol, rename_symbol, get_diagnostics, list_dir
   - User provided: repository name = `backend`, role = `Rust backend service`, path = `/home/user/backend`

2. **serena_ui** -- Tools: find_symbol, get_symbols_overview, search_for_pattern, find_referencing_symbols, replace_symbol_body, insert_after_symbol, insert_before_symbol, rename_symbol, get_diagnostics, list_dir
   - User provided: repository name = `frontend-ui`, role = `TypeScript frontend`, path = `/home/user/frontend-ui`

## Step 3 -- Jira Configuration

Atlassian MCP server detected (tools prefixed with `mcp__atlassian__`).

User provided the following Jira configuration fields:
- Project key: TC
- Cloud ID: 2b9e35e3-6bd3-4cec-b838-f4249ee02432
- Feature issue type ID: 10142
- Git Pull Request custom field: customfield_10875
- GitHub Issue custom field: customfield_10747

## Step 5 -- Code Intelligence

Generated Code Intelligence section with:
- Naming convention: `mcp__<instance>__<tool>`
- Example using `serena_backend` instance
- Limitations: User reported no known limitations for either instance

## Step 9 -- Bug Configuration

Bug Configuration was scaffolded with all three required fields:
- Bug issue type ID: 10001 (discovered from Jira metadata)
- Bug template: docs/bug-template.md (user accepted default path)
- Bug-to-Task link type: Blocks (user accepted default)

Bug template file copy skipped (simulation mode).

## Step 10 -- Security Configuration

User was asked whether to enable security triage and **accepted**.

### Product Lifecycle fields collected:
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

### Version Streams collected:
1. Stream `2.1.x`:
   - Konflux release repo URL: git.downstream.example.com/my-org/product-release.2.1.z
   - Local path: /home/user/product-release.2.1.z
   - Security matrix path: security-matrix.md

### Source Repositories collected:
1. `backend` -- https://github.com/example/backend (deployment context: upstream)
2. `frontend-ui` -- https://github.com/example/frontend-ui (deployment context: upstream)

### Supportability matrix population:
User declined optional supportability matrix population.

### Security matrix scaffolding:
User skipped security-matrix.md scaffolding.

## Step 11 -- Validation

All required sections present and populated:
- Repository Registry: 2 entries (backend, frontend-ui)
- Jira Configuration: all 5 fields populated
- Code Intelligence: naming convention documented, Limitations subsection present
- Bug Configuration: all 3 fields populated
- Security Configuration: Product Lifecycle (5 required + VEX optional fields), Version Streams (1 row), Source Repositories (2 rows)
