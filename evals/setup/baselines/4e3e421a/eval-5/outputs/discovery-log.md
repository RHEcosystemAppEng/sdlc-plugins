# Discovery Log — /sdlc-workflow:setup (simulated)

Skill instructions source: `plugins/sdlc-workflow/skills/setup/SKILL.md` (Skill tool reported `sdlc-workflow:setup` as unknown, so the SKILL.md was followed directly). Templates used: `project-config.template.md`, `security-config.template.md`.

No MCP tools were called and no Bash commands were run. All discovery was simulated from `evals/setup/files/mcp-tools-with-serena.md` and the user-provided answers in the task.

## Step 1 — Read Existing Configuration

Source: `evals/setup/files/claude-md-empty.md`

| Item | Status |
|---|---|
| `# Project Configuration` | Missing |
| `## Repository Registry` | Missing (no repositories registered) |
| `## Jira Configuration` | Missing |
| `### Jira Field Defaults` | Missing |
| `## Code Intelligence` | Missing |
| `## Bug Configuration` | Missing |
| `## Security Configuration` | Missing |
| `## Hierarchy Configuration` | Missing |

Conclusion: greenfield. The whole Project Configuration section has to be created and appended to the end of the existing file.

## Step 2 — Discover Serena Instances

I scanned the tool listing for the `mcp__<instance>__<tool>` pattern with Serena tool names (`find_symbol`, `get_symbols_overview`, `search_for_pattern`, `replace_symbol_body`, ...).

| Instance | Evidence | Already registered? |
|---|---|---|
| `serena_backend` | `mcp__serena_backend__find_symbol`, `get_symbols_overview`, `search_for_pattern`, `replace_symbol_body`, `get_diagnostics`, ... (10 tools) | No |
| `serena_ui` | `mcp__serena_ui__find_symbol`, `get_symbols_overview`, `search_for_pattern`, `replace_symbol_body`, `get_diagnostics`, ... (10 tools) | No |

`mcp__atlassian__*` is not a Serena instance and was excluded.

For each new instance, the skill would call `get_diagnostics` or ask for the path. Simulated: the user supplied the details.

| Instance | Repository | Role | Path |
|---|---|---|---|
| serena_backend | backend | Rust backend service | /home/user/backend |
| serena_ui | frontend-ui | TypeScript frontend | /home/user/frontend-ui |

## Step 3 — Jira Configuration

- Atlassian MCP detected (`mcp__atlassian__*` tools are present). The listing has no `getVisibleJiraProjects`, `getAccessibleAtlassianResources` or `getJiraProjectIssueTypesMetadata` tools. No calls were made, as the eval requires.
- Values supplied by the user (manual entry, Step 3.4):
  - Project key: TC
  - Cloud ID: 2b9e35e3-6bd3-4cec-b838-f4249ee02432
  - Feature issue type ID: 10142
  - Git Pull Request custom field: customfield_10875
  - GitHub Issue custom field: customfield_10747
- No REST API fallback was used, and no credentials were collected or stored.

## Step 3.5 — Hierarchy Preferences

- `## Hierarchy Configuration` does not exist.
- Hierarchy metadata could not be discovered, because no metadata tool calls were allowed in the simulation. The eval inputs did not give a grouping strategy.
- **Assumption:** an Epic-level (level 1) type exists in TC, so the grouping question applies. I picked option 1, `by-repository`, which the skill recommends for multi-repo projects. This project has two repositories. The user should confirm this value.

## Step 4 — Jira Field Defaults

- `getJiraIssueTypeMetaWithFields` was not available or called, so priorities and fixVersions were not discovered.
- The skill's stated defaults were applied: Default priority = none, fixVersion scope = both, Prompt for priority = true, Prompt for fixVersion = true.

## Step 5 — Code Intelligence

- The section is new. The example uses the first registry instance, `serena_backend`.
- Limitations: the user reported none for `serena_backend` or `serena_ui`.

## Step 7 — Constraints Template

- The skill would copy `constraints.template.md` to `docs/constraints.md` if it does not exist. Skipped in this simulation (no real files modified).

## Step 8 — CONVENTIONS.md Scaffolding

- The skill would offer to scaffold `CONVENTIONS.md` for `backend` and `frontend-ui`. The eval inputs did not ask for this, so it was not performed (no real files modified).

## Step 9 — Bug Configuration

- Section missing, so all three fields were scaffolded.
- Bug issue type ID: 10001 (simulated discovery from Jira issue type metadata, an issue type named "Bug").
- Bug template path: `docs/bug-template.md` (user accepted the default).
- Bug-to-Task link type: `Blocks` (user accepted the default).
- Bug template file copy (Step 9.4): skipped because this is a simulation.

## Step 10 — Security Configuration

- The section was missing. The user was asked whether to enable security triage and **accepted**.
- Product Lifecycle (Step 10.1):
  - Product pages URL: https://access.example.com/product-lifecycle
  - Jira version prefix: MYPRODUCT
  - Vulnerability issue type ID: 10200 (user-provided)
  - Component label pattern: `pscomponent:`
  - VEX Justification custom field: customfield_12345
  - Upstream Affected Component, PS Component, Stream custom fields: not provided, left blank
  - ProdSec contact email, ProdSec Jira account ID, Embargo policy URL: not provided, left blank
- Version Streams (Step 10.2): one stream
  - 2.1.x | git.downstream.example.com/my-org/product-release.2.1.z | /home/user/product-release.2.1.z | security-matrix.md
- Source Repositories (Step 10.3):
  - backend | https://github.com/example/backend
  - frontend-ui | https://github.com/example/frontend-ui
  - Deployment context was not specified, so both use the skill's default, `upstream`.
- security-matrix.md scaffolding (Step 10.5): the user skipped it.
- Supportability matrix population (Step 10.6): the user declined.
