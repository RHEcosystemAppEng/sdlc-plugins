# Discovery Log — /sdlc-workflow:setup (simulated)

The skill was not registered with the Skill tool, so I followed `plugins/sdlc-workflow/skills/setup/SKILL.md` and its templates (`project-config.template.md`, `security-config.template.md`) directly. No MCP tools or Bash commands were run. Discovery was simulated from `evals/setup/files/mcp-tools-with-serena.md`.

## Step 1 – Read Existing Configuration

Source: `evals/setup/files/claude-md-empty.md`

| Section | Present? | Notes |
|---|---|---|
| `# Project Configuration` | No | File has only project description, Documentation, Getting Started |
| `## Repository Registry` | No | — |
| `## Jira Configuration` | No | — |
| `### Jira Field Defaults` | No | — |
| `## Code Intelligence` | No | — |
| `## Bug Configuration` | No | — |
| `## Security Configuration` | No | — |
| `## Hierarchy Configuration` | No | — |

Conclusion: the CLAUDE.md file exists but has no `# Project Configuration` section, so the whole section must be created and added at the end of the file.

## Step 2 – Discover Serena Instances

Pattern matched: `mcp__<instance-name>__<tool>` with Serena tool names (`find_symbol`, `get_symbols_overview`, `search_for_pattern`, `replace_symbol_body`, ...).

| Instance | Evidence (sample tools) | Serena? |
|---|---|---|
| `serena_backend` | find_symbol, get_symbols_overview, search_for_pattern, replace_symbol_body, get_diagnostics | Yes |
| `serena_ui` | find_symbol, get_symbols_overview, search_for_pattern, replace_symbol_body, get_diagnostics | Yes |
| `atlassian` | jira_get_issue, jira_search_issues, ... | No (Atlassian MCP) |

Neither instance was already in the Registry. Answers the user gave (simulated):

| Instance | Repository | Role | Path |
|---|---|---|---|
| serena_backend | backend | Rust backend service | /home/user/backend |
| serena_ui | frontend-ui | TypeScript frontend | /home/user/frontend-ui |

(`get_diagnostics` is available on both instances but was not called. The user supplied the paths.)

## Step 3 – Jira Configuration

- An Atlassian MCP was found (`mcp__atlassian__*`). The listing does not include `getVisibleJiraProjects`, `getAccessibleAtlassianResources` or `getJiraProjectIssueTypesMetadata`. Per the task, no MCP calls were made, so I used the values the user provided:
  - Project key: TC
  - Cloud ID: 2b9e35e3-6bd3-4cec-b838-f4249ee02432
  - Feature issue type ID: 10142
  - Git Pull Request custom field: customfield_10875
  - GitHub Issue custom field: customfield_10747
- The REST API fallback was not used. This was a simulation, and all values came from the user.

## Step 3.5 – Hierarchy Preferences

- `getJiraProjectIssueTypesMetadata` is not in the tool listing, and the scenario gave no issue-type hierarchy and no grouping-strategy answer. Without that data I could not confirm a level-1 (Epic) type or get the user's grouping choice.
- Result: `## Hierarchy Configuration` was **not created**. I chose not to invent a value. Running `/setup` again with Jira metadata available will add it.

## Step 4 – Jira Field Defaults

- `getJiraIssueTypeMetaWithFields` is not available (simulation), so I could not discover priorities or fixVersions.
- The scenario gave no specific answers, so I used the defaults documented in the skill:
  - Default priority: none (no default pre-selection)
  - fixVersion scope: both (default)
  - Prompt for priority: true (default)
  - Prompt for fixVersion: true (default)

## Step 5 – Code Intelligence

- Naming convention: `mcp__<instance>__<tool>`
- Example uses the first Registry instance: `serena_backend`
- Limitations: the user reported none for `serena_backend` or `serena_ui`

## Step 7 – Constraints Template

- The task forbids modifying actual files, so `docs/constraints.md` was not copied into the target project. In a real run it would be created from `constraints.template.md` if it did not already exist.

## Step 8 – CONVENTIONS.md Scaffolding

- In a real run, the skill would check `/home/user/backend/CONVENTIONS.md` and `/home/user/frontend-ui/CONVENTIONS.md`. In this simulation nothing was checked or written, and the scenario gave no scaffolding answer.

## Step 9 – Bug Configuration

- Bug issue type ID: **10001** (from Jira metadata, as the scenario states)
- Bug template path: `docs/bug-template.md` (user accepted the default)
- Bug-to-Task link type: `Blocks` (user accepted the default)
- Step 9.4 (bug template copy): skipped, as the task instructs for this simulation

## Step 10 – Security Configuration

- Enable security triage? **Yes** (user accepted)
- Product Lifecycle (user-provided):
  - Product pages URL: https://access.example.com/product-lifecycle
  - Jira version prefix: MYPRODUCT
  - Vulnerability issue type ID: 10200
  - Component label pattern: pscomponent:
  - VEX Justification custom field: customfield_12345
  - Upstream Affected Component, PS Component, Stream custom fields, ProdSec email, ProdSec Jira account ID, Embargo policy URL: not provided, so left blank
- Version Streams:
  - 2.1.x | git.downstream.example.com/my-org/product-release.2.1.z | /home/user/product-release.2.1.z | security-matrix.md
- Source Repositories:
  - backend | https://github.com/example/backend | upstream (the default, because no deployment context was given)
  - frontend-ui | https://github.com/example/frontend-ui | upstream (the default, because no deployment context was given)
- Step 10.5 (security-matrix.md scaffold): skipped at the user's request
- Step 10.6 (populate the Supportability Matrix and Container Images): the user declined

## Step 11 – Validation (against outputs/claude-md-result.md)

| Check | Result |
|---|---|
| `# Project Configuration` heading exists | PASS |
| Repository Registry table has columns Repository, Role, Serena Instance, Path | PASS (2 rows) |
| Jira Configuration has Project key, Cloud ID, Feature issue type ID | PASS |
| Jira Field Defaults has valid values | PASS |
| Code Intelligence documents `mcp__<instance>__<tool>` | PASS |
| Code Intelligence has `### Limitations` | PASS |
| `docs/constraints.md` exists | NOT CHECKED (simulation, no file writes) |
| Bug Configuration has issue type ID, template path, link type | PASS |
| Bug template file exists at the configured path | NOT CHECKED (copy skipped per task) |
| Hierarchy Configuration has a grouping strategy | N/A (not scaffolded) |
| Security Configuration Product Lifecycle has all four required fields | PASS |
| Security Configuration Version Streams has at least one row | PASS (1 row) |
| Security Configuration Source Repositories has at least one row | PASS (2 rows) |
| No `{{placeholder}}` markers left | PASS |
