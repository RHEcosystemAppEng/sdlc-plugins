# Discovery Log — /sdlc-workflow:setup (simulated)

The Skill tool did not list `sdlc-workflow:setup`, so I followed
`plugins/sdlc-workflow/skills/setup/SKILL.md` and its sibling templates
(`project-config.template.md`, `security-config.template.md`) directly. I made no MCP calls,
ran no Bash commands, and modified no files outside `outputs/`.

## Step 1 – Read Existing Configuration

Source: `evals/setup/files/claude-md-empty.md`

| Section | Status |
|---|---|
| `# Project Configuration` | Not found |
| `## Repository Registry` | Not found (no repositories registered) |
| `## Jira Configuration` | Not found |
| `### Jira Field Defaults` | Not found |
| `## Code Intelligence` | Not found |
| `## Bug Configuration` | Not found |
| `## Security Configuration` | Not found |
| `## Hierarchy Configuration` | Not found |

Conclusion: the CLAUDE.md file exists but has no Project Configuration, so the whole section must be created and appended at the end of the file.

## Step 2 – Discover Serena Instances

Source: `evals/setup/files/mcp-tools-with-serena.md`

Matched the tool names against the pattern `mcp__<instance>__<tool>`, using Serena tool names
such as `find_symbol`, `get_symbols_overview`, `search_for_pattern` and `replace_symbol_body`.

| Instance | Evidence (Serena tools found) | In Registry? |
|---|---|---|
| `serena_backend` | find_symbol, get_symbols_overview, search_for_pattern, find_referencing_symbols, replace_symbol_body, insert_after_symbol, insert_before_symbol, rename_symbol, get_diagnostics, list_dir | No (new) |
| `serena_ui` | find_symbol, get_symbols_overview, search_for_pattern, find_referencing_symbols, replace_symbol_body, insert_after_symbol, insert_before_symbol, rename_symbol, get_diagnostics, list_dir | No (new) |

Excluded: `mcp__atlassian__*`, because these are Jira tools and not Serena tools. Built-in
tools (Bash, Read, Write, Edit, Glob, Grep) were also excluded.

Both instances have a `get_diagnostics` tool, which could provide the project root. Because
this is a simulation, I did not call it and used the paths the user provided:

| Instance | Repository | Role | Path |
|---|---|---|---|
| serena_backend | backend | Rust backend service | /home/user/backend |
| serena_ui | frontend-ui | TypeScript frontend | /home/user/frontend-ui |

## Step 3 – Jira Configuration

- An Atlassian MCP was detected: `mcp__atlassian__*` tools are present (jira_get_issue, jira_search_issues, jira_edit_issue, jira_transition_issue, jira_add_comment, jira_user_info).
- The listing has no `getVisibleJiraProjects`, `getAccessibleAtlassianResources` or `getJiraProjectIssueTypesMetadata` tools. I made no calls, per the simulation rules.
- Values were taken from the user (manual entry, Step 3.4):
  - Project key: TC
  - Cloud ID: 2b9e35e3-6bd3-4cec-b838-f4249ee02432
  - Feature issue type ID: 10142
  - Git Pull Request custom field: customfield_10875
  - GitHub Issue custom field: customfield_10747
- I did not use the REST API fallback, so no Bash was run.

## Step 3.5 – Hierarchy Preferences

- `## Hierarchy Configuration` is absent.
- The eval scenario gave no hierarchy metadata or grouping strategy, and no metadata call could be made.
- **Assumption:** an Epic-level (level 1) type exists, as in a standard Jira project. I used the neutral option `none` ("ask each time — no default"), so plan-feature does not get a strategy the user never chose. Change it to by-repository, by-sub-feature or trivial if a default is wanted.

## Step 4 – Jira Field Defaults

- `### Jira Field Defaults` is absent.
- I could not run `getJiraIssueTypeMetaWithFields`, so no priority or fixVersion lists were discovered.
- The eval scenario gave no answers, so I applied the skill's documented defaults:
  - Default priority: none
  - fixVersion scope: both
  - Prompt for priority: true
  - Prompt for fixVersion: true

## Step 5 – Code Intelligence

- The section is absent, so I generated it.
- The example uses the first registered instance, `serena_backend`.
- Limitations: the user reported none for either instance.

## Step 7 – Constraints Template

- This is a simulation, so `docs/constraints.md` was not checked or written. In a real run it would be created from `constraints.template.md` if missing.

## Step 8 – CONVENTIONS.md Scaffolding

- This is a simulation and the eval scenario gave no instructions for it, so I did not scaffold or check CONVENTIONS.md for `backend` or `frontend-ui`.

## Step 9 – Bug Configuration

- The section is absent.
- Bug issue type ID: 10001, "discovered" from Jira metadata as the eval scenario stated.
- Bug template path: `docs/bug-template.md`, the default, which the user accepted.
- Bug-to-Task link type: `Blocks`, the default, which the user accepted.
- Bug template copy (Step 9.4): skipped, because this is a simulation.

## Step 10 – Security Configuration

- The section is absent. The user accepted the offer to enable security triage.
- Product Lifecycle:
  - Product pages URL: https://access.example.com/product-lifecycle
  - Jira version prefix: MYPRODUCT
  - Vulnerability issue type ID: 10200
  - Component label pattern: pscomponent:
  - VEX Justification custom field: customfield_12345
  - Upstream Affected Component, PS Component and Stream custom fields: not provided, left blank
  - ProdSec contact email, ProdSec Jira account ID and Embargo policy URL: not provided, left blank
- Version Streams:
  - Stream: 2.1.x
  - Konflux release repo: git.downstream.example.com/my-org/product-release.2.1.z
  - Local path: /home/user/product-release.2.1.z
  - Security matrix path: security-matrix.md
- Source Repositories:
  - backend: https://github.com/example/backend. No deployment context was given, so it defaults to `upstream`.
  - frontend-ui: https://github.com/example/frontend-ui. No deployment context was given, so it defaults to `upstream`.
- Placement: after `## Code Intelligence`, per Step 10.4.
- security-matrix.md scaffolding (Step 10.5): skipped by the user.
- Supportability Matrix and Container Images population (Step 10.6): declined by the user.

## Step 11 – Validation (performed on outputs/claude-md-result.md)

| Check | Result |
|---|---|
| `# Project Configuration` heading exists | PASS |
| Repository Registry table has columns Repository, Role, Serena Instance, Path | PASS (2 rows) |
| Jira Configuration has Project key, Cloud ID and Feature issue type ID | PASS |
| Jira Field Defaults has valid values | PASS |
| Code Intelligence documents `mcp__<instance>__<tool>` | PASS |
| Code Intelligence has `### Limitations` | PASS |
| `docs/constraints.md` exists | NOT CHECKED (simulation) |
| Bug Configuration has issue type ID, template path and link type | PASS |
| Bug template file exists at the configured path | NOT CHECKED (copy skipped in simulation) |
| Hierarchy Configuration has Default epic grouping strategy | PASS |
| Security Configuration Product Lifecycle has all 4 required fields | PASS |
| Version Streams has at least one row | PASS (1 row) |
| Source Repositories has at least one row | PASS (2 rows) |
| No `{{placeholder}}` markers remain | PASS |
