# Discovery Log — /sdlc-workflow:setup (simulated)

Note: The Skill tool did not list `sdlc-workflow:setup`, so the skill was followed directly from
`plugins/sdlc-workflow/skills/setup/SKILL.md` and its templates. No MCP tools, Bash commands, or
external services were used. All discovery was simulated from the provided input files and
the user-supplied answers in the task.

## Step 1 — Read Existing Configuration

Source: `evals/setup/files/claude-md-empty.md`

| Item | Status |
|---|---|
| `# Project Configuration` | Not present |
| `## Repository Registry` | Not present (no repositories registered) |
| `## Jira Configuration` | Not present |
| `### Jira Field Defaults` | Not present |
| `## Code Intelligence` | Not present |
| `## Bug Configuration` | Not present |
| `## Security Configuration` | Not present |
| `## Hierarchy Configuration` | Not present |

Conclusion: greenfield project. The whole Project Configuration section must be created and
appended to the end of the existing CLAUDE.md. Existing content (title, Documentation,
Getting Started) is kept as-is.

## Step 2 — Discover Serena Instances

Source: `evals/setup/files/mcp-tools-with-serena.md`

I looked for tools matching `mcp__<instance>__<tool>` that include Serena tool names
(`find_symbol`, `get_symbols_overview`, `search_for_pattern`, `replace_symbol_body`, ...).

| Instance | Serena tools found | `get_diagnostics` present |
|---|---|---|
| `serena_backend` | find_symbol, get_symbols_overview, search_for_pattern, find_referencing_symbols, replace_symbol_body, insert_after_symbol, insert_before_symbol, rename_symbol, get_diagnostics, list_dir | Yes |
| `serena_ui` | find_symbol, get_symbols_overview, search_for_pattern, find_referencing_symbols, replace_symbol_body, insert_after_symbol, insert_before_symbol, rename_symbol, get_diagnostics, list_dir | Yes |

Excluded: `mcp__atlassian__*`, since these are Jira tools, not Serena tools. Built-in tools
(Bash, Read, Write, Edit, Glob, Grep) were also excluded.

Neither instance was already in the Repository Registry. `get_diagnostics` was not called
(simulation), so the details came from the user:

| Instance | Repository | Role | Path |
|---|---|---|---|
| serena_backend | backend | Rust backend service | /home/user/backend |
| serena_ui | frontend-ui | TypeScript frontend | /home/user/frontend-ui |

## Step 3 — Jira Configuration

- Atlassian MCP was detected (`mcp__atlassian__*`). It does not expose
  `getVisibleJiraProjects`, `getAccessibleAtlassianResources`, or
  `getJiraProjectIssueTypesMetadata`, and the eval forbids MCP calls, so auto-discovery was not run.
- Values supplied by the user (manual entry path, Step 3.4):
  - Project key: TC
  - Cloud ID: 2b9e35e3-6bd3-4cec-b838-f4249ee02432
  - Feature issue type ID: 10142
  - Git Pull Request custom field: customfield_10875
  - GitHub Issue custom field: customfield_10747

## Step 3.5 — Hierarchy Preferences

- Section not present, so it must be scaffolded.
- Issue type hierarchy could not be discovered live (no MCP calls). Simulated metadata
  assumes a standard Jira hierarchy that includes a level-1 Epic type, so the grouping
  strategy question applies.
- The task gave no grouping strategy. **Assumption:** `by-repository`, the option the skill
  marks as recommended for multi-repo projects (this project has 2 repositories).

## Step 4 — Jira Field Defaults

- Section not present. Priorities and fixVersions could not be fetched
  (`getJiraIssueTypeMetaWithFields` was not called).
- The task gave no values. **Assumption:** the skill defaults were accepted:
  - Default priority: none
  - fixVersion scope: both
  - Prompt for priority: true
  - Prompt for fixVersion: true

## Step 5 — Code Intelligence

- Section not present, so it is generated with the `mcp__<instance>__<tool>` convention.
- Example uses the first registry instance: `serena_backend`.
- Limitations: the user reports none for either instance.

## Step 7 — Constraints Template

- `docs/constraints.md` would be copied from `constraints.template.md` if absent. Skipped because
  this is a simulation and only outputs/ may be written.

## Step 8 — CONVENTIONS.md Scaffolding

- This step would check `/home/user/backend/CONVENTIONS.md` and `/home/user/frontend-ui/CONVENTIONS.md`.
  Skipped because this is a simulation and only outputs/ may be written.

## Step 9 — Bug Configuration

- Section not present, so it must be scaffolded.
- Bug issue type ID: 10001 (from simulated Jira issue-type metadata, type named "Bug").
- Bug template path: `docs/bug-template.md` (default accepted).
- Bug-to-Task link type: `Blocks` (default accepted; `getIssueLinkTypes` not called).
- Bug template copy (Step 9.4): skipped per task instructions.

## Step 10 — Security Configuration

- Section not present. The user **accepted** enabling security triage.
- Product Lifecycle:
  - Product pages URL: https://access.example.com/product-lifecycle
  - Jira version prefix: MYPRODUCT
  - Vulnerability issue type ID: 10200
  - Component label pattern: pscomponent:
  - VEX Justification custom field: customfield_12345
  - Upstream Affected Component / PS Component / Stream custom fields: not provided, left blank
  - ProdSec contact email / ProdSec Jira account ID / Embargo policy URL: not provided, left blank
- Version Streams (1):
  - 2.1.x | git.downstream.example.com/my-org/product-release.2.1.z | /home/user/product-release.2.1.z | security-matrix.md
- Source Repositories (2):
  - backend | https://github.com/example/backend | upstream (default; no context given)
  - frontend-ui | https://github.com/example/frontend-ui | upstream (default; no context given)
- Step 10.5 security-matrix.md scaffolding: user skipped.
- Step 10.6 supportability matrix population: user declined.

## Step 11 — Validation (against outputs/claude-md-result.md)

| Check | Result |
|---|---|
| `# Project Configuration` heading exists | PASS |
| Repository Registry table has columns Repository, Role, Serena Instance, Path | PASS (2 rows) |
| Jira Configuration has Project key, Cloud ID, Feature issue type ID | PASS |
| Jira Field Defaults has valid values | PASS |
| Code Intelligence documents `mcp__<instance>__<tool>` | PASS |
| Code Intelligence has `### Limitations` | PASS |
| `docs/constraints.md` exists | NOT CHECKED (simulation; copy skipped) |
| Bug Configuration has issue type ID, template path, link type | PASS |
| Bug template file exists at configured path | NOT CHECKED (copy skipped per task) |
| Hierarchy Configuration has Default epic grouping strategy | PASS |
| Security Configuration `### Product Lifecycle` has 4 required fields | PASS |
| Security Configuration `### Version Streams` has at least 1 row | PASS (1 row) |
| Security Configuration `### Source Repositories` has at least 1 row | PASS (2 rows) |
