# Discovery Log — /sdlc-workflow:setup (simulated)

## Step 1 – Read Existing Configuration

- Source: `evals/setup/files/claude-md-empty.md`
- Found: `# my-project` title, intro paragraph, `## Documentation`, `## Getting Started`.
- `# Project Configuration`: not present. Therefore Repository Registry, Jira Configuration, Jira Field Defaults, Code Intelligence, Bug Configuration, Security Configuration and Hierarchy Configuration are all absent — everything must be created.

## Step 2 – Serena Instance Discovery

- Source: `evals/setup/files/mcp-tools-with-serena.md` (simulated tool listing; no MCP tools were called).
- Method: matched tools against the pattern `mcp__<instance>__<tool>` with Serena tool names (`find_symbol`, `get_symbols_overview`, `search_for_pattern`, `replace_symbol_body`, ...).
- Discovered instances:
  | Instance | Evidence | Tools |
  |---|---|---|
  | `serena_backend` | `mcp__serena_backend__find_symbol`, `get_symbols_overview`, `search_for_pattern`, `replace_symbol_body`, `get_diagnostics`, ... | 10 |
  | `serena_ui` | `mcp__serena_ui__find_symbol`, `get_symbols_overview`, `search_for_pattern`, `replace_symbol_body`, `get_diagnostics`, ... | 10 |
- `mcp__atlassian__*` tools were recognized as the Atlassian MCP server, not Serena.
- Neither instance was in the (non-existent) Repository Registry, so both are new.
- Repository details (path via `get_diagnostics` would be possible, but simulated as user-provided):
  - `serena_backend` → repository `trustify-backend`, role `Rust backend service`, path `/home/user/trustify-backend` (user-provided)
  - `serena_ui` → repository `trustify-ui`, role `TypeScript frontend`, path `/home/user/trustify-ui` (user-provided)

## Step 3 – Jira Configuration

- Atlassian MCP detected (`mcp__atlassian__jira_get_issue`, `jira_search_issues`, `jira_edit_issue`, `jira_transition_issue`, `jira_add_comment`, `jira_user_info`).
- The listing does not include `getVisibleJiraProjects`, `getAccessibleAtlassianResources` or `getJiraProjectIssueTypesMetadata`; per eval instructions no MCP calls were made. Values were taken as user-provided:
  - Project key: `TC`
  - Cloud ID: `2b9e35e3-6bd3-4cec-b838-f4249ee02432`
  - Feature issue type ID: `10142`
  - Git Pull Request custom field: `customfield_10875`
  - GitHub Issue custom field: `customfield_10747`

## Step 3.5 – Hierarchy Preferences

- No issue type hierarchy metadata was supplied in the simulation and no grouping strategy was provided by the user. Hierarchy discovery could not be performed without calling MCP, so `## Hierarchy Configuration` was **not** created (it can be added on a later run; setup is incremental).

## Step 4 – Jira Field Defaults

- No priority/fixVersion metadata was available (no MCP calls). The skill's documented defaults were applied: Default priority `none` (no pre-selection), fixVersion scope `both`, Prompt for priority `true`, Prompt for fixVersion `true`.

## Step 5 – Code Intelligence

- Naming convention example uses the first registry instance: `serena_backend`.
- Limitations: user reported none for `serena_backend` and `serena_ui`.

## Step 7 – Constraints Template

- Simulation only: `docs/constraints.md` would be created from `constraints.template.md` if absent. No file written.

## Step 8 (CONVENTIONS.md scaffold)

- Simulation only: not performed; no repository files written.

## Bug Configuration

- Bug issue type ID: `10001` — discovered from Jira metadata (simulated; issue type named "Bug").
- Bug template path: `docs/bug-template.md` — user accepted default.
- Bug-to-Task link type: `Blocks` — user accepted default.
- Bug template file copy: skipped (simulation).

## Security Configuration

- User asked whether to enable security triage → **declined**. `## Security Configuration` not created; no security-matrix scaffolding.

## Validation (against generated output)

- `# Project Configuration` heading: present
- Repository Registry table with Repository/Role/Serena Instance/Path columns: present (2 rows)
- Jira Configuration with Project key, Cloud ID, Feature issue type ID: present
- Jira Field Defaults: present, all four fields populated
- Code Intelligence documents `mcp__<instance>__<tool>`: present
- Code Intelligence `### Limitations`: present
- Bug Configuration with all three fields: present
- Security Configuration: not scaffolded (declined)
- Hierarchy Configuration: not scaffolded (no input available)
- `docs/constraints.md` / bug template file: not created (simulation)
