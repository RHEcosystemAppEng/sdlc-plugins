# Setup Discovery Log

## Step 1 — Read Existing Configuration

- Read CLAUDE.md from `evals/setup/files/claude-md-empty.md`
- No `# Project Configuration` section found
- All sections need to be created from scratch

## Step 2 — Discover Serena Instances

Examined available MCP tools from `evals/setup/files/mcp-tools-with-serena.md`.

Discovered 2 Serena instances:
- **serena_backend** — tools: `mcp__serena_backend__find_symbol`, `mcp__serena_backend__get_symbols_overview`, `mcp__serena_backend__search_for_pattern`, `mcp__serena_backend__find_referencing_symbols`, `mcp__serena_backend__replace_symbol_body`, `mcp__serena_backend__insert_after_symbol`, `mcp__serena_backend__insert_before_symbol`, `mcp__serena_backend__rename_symbol`, `mcp__serena_backend__get_diagnostics`, `mcp__serena_backend__list_dir`
- **serena_ui** — tools: `mcp__serena_ui__find_symbol`, `mcp__serena_ui__get_symbols_overview`, `mcp__serena_ui__search_for_pattern`, `mcp__serena_ui__find_referencing_symbols`, `mcp__serena_ui__replace_symbol_body`, `mcp__serena_ui__insert_after_symbol`, `mcp__serena_ui__insert_before_symbol`, `mcp__serena_ui__rename_symbol`, `mcp__serena_ui__get_diagnostics`, `mcp__serena_ui__list_dir`

Also discovered Atlassian MCP tools: `mcp__atlassian__jira_get_issue`, `mcp__atlassian__jira_search_issues`, `mcp__atlassian__jira_edit_issue`, `mcp__atlassian__jira_transition_issue`, `mcp__atlassian__jira_add_comment`, `mcp__atlassian__jira_user_info`

User-provided repository mappings:
- serena_backend -> repository: 'backend', role: 'Rust backend service', path: '/home/user/backend'
- serena_ui -> repository: 'frontend-ui', role: 'TypeScript frontend', path: '/home/user/frontend-ui'

No known limitations reported for either Serena instance.

## Step 3 — Jira Configuration

No existing Jira Configuration found. All fields collected from user input:
- Project key: TC
- Cloud ID: 2b9e35e3-6bd3-4cec-b838-f4249ee02432
- Feature issue type ID: 10142
- Git Pull Request custom field: customfield_10875
- GitHub Issue custom field: customfield_10747

## Step 3.5 — Hierarchy Preferences

User selected default epic grouping strategy: by-sub-feature

## Step 4 — Jira Field Defaults

Skipped — MCP tools not available for priority/fixVersion discovery in simulation mode.

## Step 5 — Code Intelligence

Generated Code Intelligence section documenting the `mcp__<instance>__<tool>` naming convention with a concrete example using `serena_backend`. No limitations reported for either instance.

## Step 9 — Bug Configuration

Bug issue type ID discovered from Jira metadata: 10001
User accepted default bug template path: docs/bug-template.md
User accepted default Bug-to-Task link type: Blocks
Bug template file copy skipped (simulation mode).

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

### Version Streams collected:
| Stream | Konflux Release Repo | Local Path | Security Matrix Path |
|---|---|---|---|
| 2.1.x | git.downstream.example.com/my-org/product-release.2.1.z | /home/user/product-release.2.1.z | security-matrix.md |

### Source Repositories collected:
| Repository | URL | Deployment Context |
|---|---|---|
| backend | https://github.com/example/backend | upstream |
| frontend-ui | https://github.com/example/frontend-ui | upstream |

User declined supportability matrix population.
User skipped security-matrix.md scaffolding.

## Step 11 — Validation

Verified the generated Project Configuration:
- [x] `# Project Configuration` heading exists
- [x] `## Repository Registry` contains table with columns: Repository, Role, Serena Instance, Path
- [x] `## Repository Registry` contains 2 rows (backend, frontend-ui)
- [x] `## Jira Configuration` contains: Project key (TC), Cloud ID, Feature issue type ID (10142)
- [x] `## Jira Configuration` contains optional fields: Git Pull Request custom field, GitHub Issue custom field
- [x] `## Code Intelligence` documents the `mcp__<instance>__<tool>` naming convention
- [x] `## Code Intelligence` has a `### Limitations` subheading
- [x] `## Bug Configuration` contains: Bug issue type ID (10001), Bug template path, Bug-to-Task link type (Blocks)
- [x] `## Security Configuration` contains `### Product Lifecycle` with all required fields
- [x] `## Security Configuration` contains `### Version Streams` with 1 row
- [x] `## Security Configuration` contains `### Source Repositories` with 2 rows
- [x] `## Hierarchy Configuration` contains Default epic grouping strategy (by-sub-feature)
