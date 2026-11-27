# Discovery Log — /sdlc-workflow:setup (simulated)

## Step 1 – Read Existing Configuration

- Source: `evals/setup/files/claude-md-empty.md`
- Found: `# my-project` heading, description, `## Documentation`, `## Getting Started`.
- `# Project Configuration`: **not present**. Therefore Repository Registry, Jira Configuration,
  Jira Field Defaults, Code Intelligence, Bug Configuration, Security Configuration and
  Hierarchy Configuration all need to be created.

## Step 2 – Discover Serena Instances

- Source: `evals/setup/files/mcp-tools-with-serena.md` (simulated MCP tool listing; no MCP tools were called).
- Pattern matched: `mcp__<instance>__<tool>` with Serena tool names (`find_symbol`,
  `get_symbols_overview`, `search_for_pattern`, `replace_symbol_body`, `get_diagnostics`, ...).
- Discovered instances (2):
  | Instance | Evidence | Repository (user) | Role (user) | Path (user) |
  |---|---|---|---|---|
  | serena_backend | 10 tools, e.g. `mcp__serena_backend__find_symbol`, `mcp__serena_backend__get_diagnostics` | trustify-backend | Rust backend service | /home/user/trustify-backend |
  | serena_ui | 10 tools, e.g. `mcp__serena_ui__find_symbol`, `mcp__serena_ui__get_diagnostics` | trustify-ui | TypeScript frontend | /home/user/trustify-ui |
- Paths: `get_diagnostics` is available on both instances, but per the simulation it was not
  called; paths were provided by the user.
- `mcp__atlassian__*` tools are not Serena tools and were excluded.

## Step 3 – Jira Configuration

- Atlassian MCP detected in tool listing (`mcp__atlassian__jira_get_issue`, `jira_search_issues`,
  `jira_edit_issue`, `jira_transition_issue`, `jira_add_comment`, `jira_user_info`).
- Not called (simulation). Values provided by the user:
  - Project key: TC
  - Cloud ID: 2b9e35e3-6bd3-4cec-b838-f4249ee02432
  - Feature issue type ID: 10142
  - Git Pull Request custom field: customfield_10875
  - GitHub Issue custom field: customfield_10747
- No REST API fallback used; no credentials stored.

## Step 3.5 – Hierarchy Preferences

- Issue type hierarchy (Epic-level type and grouping strategy) was not provided in the
  scenario and could not be discovered without calling MCP. Hierarchy Configuration was
  **not** written; re-run setup with Jira access to configure it.

## Step 4 – Jira Field Defaults

- Priorities/fixVersions not discovered (no MCP calls). Skill defaults applied:
  Default priority = none, fixVersion scope = both, Prompt for priority = true,
  Prompt for fixVersion = true.

## Step 5 – Code Intelligence

- Naming convention documented; example uses first registry instance `serena_backend`.
- Limitations: user reported none for `serena_backend` and `serena_ui`.

## Step 7 – Constraints template / Step 8 – CONVENTIONS.md

- Not performed (simulation: no files outside outputs/ may be written). In a real run,
  `docs/constraints.md` would be created from `constraints.template.md` if missing, and the
  user would be offered CONVENTIONS.md scaffolding for trustify-backend and trustify-ui.

## Step 9 – Bug Configuration

- Bug issue type ID: 10001 — discovered from Jira issue type metadata (simulated).
- Bug template path: `docs/bug-template.md` — user accepted default.
- Bug-to-Task link type: Blocks — user accepted default.
- Bug template file copy: skipped (simulation).

## Step 10 – Security Configuration

- `## Security Configuration` not present; user was asked whether to enable security
  triage and **declined**. Section not created; no security-matrix scaffolding.
