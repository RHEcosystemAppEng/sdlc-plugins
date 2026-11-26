# Discovery Log — /sdlc-workflow:setup (simulated)

## Step 1 – Read Existing Configuration

- Source: `evals/setup/files/claude-md-empty.md`
- Found: `# my-project` heading, description, `## Documentation`, `## Getting Started`.
- Not found: `# Project Configuration`, `## Repository Registry`, `## Jira Configuration`,
  `### Jira Field Defaults`, `## Code Intelligence`, `## Bug Configuration`,
  `## Security Configuration`, `## Hierarchy Configuration`.
- Conclusion: everything in the Project Configuration needs to be created (greenfield).

## Step 2 – Discover Serena Instances

- Source: `evals/setup/files/mcp-tools-with-serena.md` (simulated MCP tool listing; no MCP tools called).
- Pattern matched: `mcp__<instance>__<tool>` with Serena tool names (`find_symbol`,
  `get_symbols_overview`, `search_for_pattern`, `replace_symbol_body`, `get_diagnostics`, ...).
- Discovered instances:
  - `serena_backend` (10 tools, includes `get_diagnostics`)
  - `serena_ui` (10 tools, includes `get_diagnostics`)
- `mcp__atlassian__*` tools were recognized as Atlassian MCP, not Serena.
- Neither instance was already in a Repository Registry (none existed).
- Repository details (user-provided; `get_diagnostics` not called per simulation rules):

| Serena instance | Repository | Role | Path | Source |
|---|---|---|---|---|
| serena_backend | trustify-backend | Rust backend service | /home/user/trustify-backend | User |
| serena_ui | trustify-ui | TypeScript frontend | /home/user/trustify-ui | User |

## Step 3 – Jira Configuration

- Atlassian MCP detected (`mcp__atlassian__jira_get_issue`, `jira_search_issues`, `jira_edit_issue`,
  `jira_transition_issue`, `jira_add_comment`, `jira_user_info`). The listing does not expose
  `getVisibleJiraProjects`, `getAccessibleAtlassianResources`, or `getJiraProjectIssueTypesMetadata`,
  and MCP calls are disallowed in this simulation, so values came from the user (manual entry path).

| Field | Value | Source |
|---|---|---|
| Project key | TC | User |
| Cloud ID | 2b9e35e3-6bd3-4cec-b838-f4249ee02432 | User |
| Feature issue type ID | 10142 | User |
| Git Pull Request custom field | customfield_10875 | User |
| GitHub Issue custom field | customfield_10747 | User |

## Step 3.5 – Hierarchy Preferences

- No issue type hierarchy data was available (no MCP calls; no hierarchy info supplied in the
  scenario), so no Epic-level type could be confirmed and no grouping strategy was chosen.
- Result: `## Hierarchy Configuration` was not created. Re-run setup with Jira access to add it.

## Step 4 – Jira Field Defaults

- Priority and fixVersion lists could not be fetched (`getJiraIssueTypeMetaWithFields` not called).
- No user preferences were given, so the skill's documented defaults were used:
  - Default priority: none (no default pre-selection)
  - fixVersion scope: both (skill default)
  - Prompt for priority: true (skill default)
  - Prompt for fixVersion: true (skill default)

## Step 5 – Code Intelligence

- Example instance: `serena_backend` (first entry in the Repository Registry).
- Limitations: user reported none for `serena_backend` or `serena_ui`.

## Step 7 – Constraints Template

- Skipped (simulation: only write to outputs/). Normally `constraints.template.md` would be copied to
  `docs/constraints.md` if it does not already exist.

## Step 8 – CONVENTIONS.md Scaffolding

- Skipped (simulation: no writes outside outputs/; repository paths are not real).

## Step 9 – Bug Configuration

| Field | Value | Source |
|---|---|---|
| Bug issue type ID | 10001 | Jira metadata (issue type named "Bug"), as given in scenario |
| Bug template | docs/bug-template.md | User accepted default |
| Bug-to-Task link type | Blocks | User accepted default |

- Bug template file copy (from plugin `docs/templates/bug-template.md`): skipped as instructed.

## Step 10 – Security Configuration

- No `## Security Configuration` existed. User was asked whether to enable security triage and declined.
- Result: section not created; Steps 10.1–10.6 skipped.
