# Discovery Log — /sdlc-workflow:setup (simulated)

Skill source: `plugins/sdlc-workflow/skills/setup/SKILL.md` (the Skill tool reported `sdlc-workflow:setup` as unknown, so the SKILL.md was followed directly). Templates used: `project-config.template.md`, `security-config.template.md`.

No MCP tools were called and no Bash commands were run. All discovery below is simulated from the input files and the answers supplied in the task.

## Step 1 – Read Existing Configuration

Input: `evals/setup/files/claude-md-empty.md`

| Item | Found? |
|---|---|
| `# Project Configuration` heading | No |
| `## Repository Registry` | No |
| `## Jira Configuration` | No |
| `### Jira Field Defaults` | No |
| `## Code Intelligence` | No |
| `## Bug Configuration` | No |
| `## Security Configuration` | No |
| `## Hierarchy Configuration` | No |

Result: the file exists but has no Project Configuration, so every section has to be created and appended to the end of the file.

## Step 2 – Discover Serena Instances

Input: `evals/setup/files/mcp-tools-with-serena.md`

Matched the pattern `mcp__<instance>__<tool>` against Serena tool names (`find_symbol`, `get_symbols_overview`, `search_for_pattern`, `replace_symbol_body`, ...):

| Instance | Evidence (sample tools) | Already in registry? |
|---|---|---|
| `serena_backend` | find_symbol, get_symbols_overview, search_for_pattern, replace_symbol_body, get_diagnostics (10 tools) | No |
| `serena_ui` | find_symbol, get_symbols_overview, search_for_pattern, replace_symbol_body, get_diagnostics (10 tools) | No |

`mcp__atlassian__*` was not counted as a Serena instance because its tools are Jira operations, not Serena symbol tools.

`get_diagnostics` is available for both instances but was not called (simulation). The user supplied the paths instead:

| Instance | Repository | Role | Path |
|---|---|---|---|
| serena_backend | backend | Rust backend service | /home/user/backend |
| serena_ui | frontend-ui | TypeScript frontend | /home/user/frontend-ui |

## Step 3 – Jira Configuration

- Atlassian MCP was detected (`mcp__atlassian__jira_get_issue`, `jira_search_issues`, `jira_edit_issue`, `jira_transition_issue`, `jira_add_comment`, `jira_user_info`).
- The listing does not include `getVisibleJiraProjects`, `getAccessibleAtlassianResources` or `getJiraProjectIssueTypesMetadata`. Auto-discovery was not attempted in any case, because this is a simulation.
- The user supplied the fields manually (Step 3.4 path):
  - Project key: TC
  - Cloud ID: 2b9e35e3-6bd3-4cec-b838-f4249ee02432
  - Feature issue type ID: 10142
  - Git Pull Request custom field: customfield_10875
  - GitHub Issue custom field: customfield_10747

## Step 3.5 – Hierarchy Preferences

- The issue type hierarchy could not be discovered: no MCP call was allowed, and the task gives no hierarchy data or grouping strategy.
- Because the existence of an Epic-level (level 1) type could not be confirmed, no grouping strategy was invented. The `## Hierarchy Configuration` section was **not created**. A later `/setup` run can add it once the hierarchy can be discovered.

## Step 4 – Jira Field Defaults

- Priorities and fixVersions could not be discovered (`getJiraIssueTypeMetaWithFields` is not available and no MCP calls were allowed).
- No answers were supplied, so the skill's documented defaults were applied: Default priority = none, fixVersion scope = both, Prompt for priority = true, Prompt for fixVersion = true.

## Step 5 – Code Intelligence

- Example instance: `serena_backend` (first entry in the Repository Registry).
- Limitations: the user reported none for `serena_backend` or `serena_ui`.

## Step 7 – Constraints Template

- The task allows writing only to `outputs/`, so the target project's `docs/constraints.md` was not checked or created.

## Step 8 – CONVENTIONS.md

- The task gives no instruction for this step and allows writes only to `outputs/`, so no CONVENTIONS.md was scaffolded for `backend` or `frontend-ui`.

## Step 9 – Bug Configuration

- Bug issue type ID: 10001 (assumed discovered from Jira metadata, as the task specifies)
- Bug template path: `docs/bug-template.md` (user accepted the default)
- Bug-to-Task link type: Blocks (user accepted the default)
- Template copy (Step 9.4): skipped, as the task instructs for this simulation.

## Step 10 – Security Configuration

- User accepted enabling security triage.
- Product Lifecycle:
  - Product pages URL: https://access.example.com/product-lifecycle
  - Jira version prefix: MYPRODUCT
  - Vulnerability issue type ID: 10200
  - Component label pattern: pscomponent:
  - VEX Justification custom field: customfield_12345
  - Upstream Affected Component, PS Component, Stream custom fields, ProdSec email, ProdSec Jira account ID, Embargo policy URL: not provided, left empty
- Version Streams: one stream, `2.1.x`, with repo `git.downstream.example.com/my-org/product-release.2.1.z`, local path `/home/user/product-release.2.1.z` and matrix `security-matrix.md`
- Source Repositories:
  - backend: https://github.com/example/backend (deployment context not given, so it uses the default `upstream`)
  - frontend-ui: https://github.com/example/frontend-ui (deployment context not given, so it uses the default `upstream`)
- Step 10.5 security-matrix.md scaffolding: the user skipped it
- Step 10.6 supportability matrix population: the user declined
