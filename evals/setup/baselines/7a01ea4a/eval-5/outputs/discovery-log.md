# Setup Discovery Log

## Step 1 -- Read Existing Configuration

- Read CLAUDE.md from: evals/setup/files/claude-md-empty.md
- No `# Project Configuration` section found
- All sections need to be created from scratch

## Step 2 -- Discover Serena Instances

Scanned available MCP tools for Serena instance naming pattern `mcp__<instance>__<tool>`.

Discovered 2 Serena instances:

| Instance Name | Tools Found |
|---|---|
| serena_backend | find_symbol, get_symbols_overview, search_for_pattern, find_referencing_symbols, replace_symbol_body, insert_after_symbol, insert_before_symbol, rename_symbol, get_diagnostics, list_dir |
| serena_ui | find_symbol, get_symbols_overview, search_for_pattern, find_referencing_symbols, replace_symbol_body, insert_after_symbol, insert_before_symbol, rename_symbol, get_diagnostics, list_dir |

User-provided repository details:

- serena_backend: repository='backend', role='Rust backend service', path='/home/user/backend'
- serena_ui: repository='frontend-ui', role='TypeScript frontend', path='/home/user/frontend-ui'

## Step 3 -- Jira Configuration

Atlassian MCP server detected (tools prefixed with `mcp__atlassian__`).

Simulation mode -- MCP tools not called. User provided Jira configuration manually:

- Project key: TC
- Cloud ID: 2b9e35e3-6bd3-4cec-b838-f4249ee02432
- Feature issue type ID: 10142
- Git Pull Request custom field: customfield_10875
- GitHub Issue custom field: customfield_10747

## Step 3.5 -- Hierarchy Preferences

Simulation mode -- could not auto-discover issue type hierarchy via MCP.

User selected default epic grouping strategy: by-sub-feature

## Step 4 -- Jira Field Defaults

Skipped -- cannot auto-discover available priorities and fixVersions without MCP access. Jira Field Defaults can be configured in a subsequent setup run when MCP is available.

## Step 5 -- Code Intelligence

Generated Code Intelligence section documenting:
- Tool naming convention: `mcp__<instance>__<tool>`
- Example using first Serena instance: serena_backend
- Limitations: User confirmed no known limitations for either instance

## Step 6 -- Write Configuration

Composed full Project Configuration section with subsections:
- Repository Registry (2 entries)
- Jira Configuration (5 fields)
- Code Intelligence (with Limitations)
- Bug Configuration (3 fields)
- Security Configuration (Product Lifecycle, Version Streams, Source Repositories)
- Hierarchy Configuration (1 field)

Appended to end of existing CLAUDE.md (no prior Project Configuration section existed).

## Step 7 -- Copy Constraints Template

Simulation mode -- skipped file copy. In a real run, would copy constraints.template.md to docs/constraints.md in the target project.

## Step 8 -- Scaffold CONVENTIONS.md

Simulation mode -- skipped CONVENTIONS.md scaffolding for both repositories:
- backend (/home/user/backend)
- frontend-ui (/home/user/frontend-ui)

## Step 9 -- Bug Configuration

- Bug issue type ID: 10001 (discovered from Jira metadata)
- Bug template path: docs/bug-template.md (user accepted default)
- Bug-to-Task link type: Blocks (user accepted default)
- Bug template file copy: skipped (simulation mode)

## Step 10 -- Security Configuration

User accepted security triage enablement.

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

### Version Streams collected (1 stream):

| Stream | Konflux Release Repo | Local Path | Security Matrix Path |
|---|---|---|---|
| 2.1.x | git.downstream.example.com/my-org/product-release.2.1.z | /home/user/product-release.2.1.z | security-matrix.md |

### Source Repositories collected (2 repositories):

| Repository | URL | Deployment Context |
|---|---|---|
| backend | https://github.com/example/backend | upstream |
| frontend-ui | https://github.com/example/frontend-ui | upstream |

### security-matrix.md scaffolding: skipped (user declined)
### Supportability matrix population: skipped (user declined)

## Step 11 -- Validation

Validation results:
- [PASS] `# Project Configuration` heading exists
- [PASS] `## Repository Registry` contains table with columns: Repository, Role, Serena Instance, Path
- [PASS] `## Jira Configuration` contains: Project key, Cloud ID, Feature issue type ID
- [SKIP] `### Jira Field Defaults` -- not configured (MCP unavailable for discovery)
- [PASS] `## Code Intelligence` documents `mcp__<instance>__<tool>` naming convention
- [PASS] `## Code Intelligence` has `### Limitations` subheading
- [SKIP] `docs/constraints.md` -- simulation mode, file copy skipped
- [PASS] `## Bug Configuration` contains: Bug issue type ID, Bug template path, Bug-to-Task link type
- [SKIP] Bug template file -- simulation mode, file copy skipped
- [PASS] `## Hierarchy Configuration` contains Default epic grouping strategy
- [PASS] `## Security Configuration` contains `### Product Lifecycle` with required fields
- [PASS] `## Security Configuration` contains `### Version Streams` with 1 row
- [PASS] `## Security Configuration` contains `### Source Repositories` with 2 rows
