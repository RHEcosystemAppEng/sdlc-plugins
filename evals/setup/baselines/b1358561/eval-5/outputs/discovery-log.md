# Discovery Log — /sdlc-workflow:setup (simulated)

Skill source: `plugins/sdlc-workflow/skills/setup/SKILL.md` (the Skill tool did not list `sdlc-workflow:setup`, so I read the file and followed it directly). No MCP tools or Bash commands were run. Discovery was simulated from the input files.

## Step 1 – Read Existing Configuration

Source: `evals/setup/files/claude-md-empty.md`

- `# Project Configuration`: not found
- `## Repository Registry`: not found (no repositories registered)
- `## Jira Configuration` / `### Jira Field Defaults`: not found
- `## Code Intelligence`: not found
- `## Bug Configuration`: not found
- `## Security Configuration`: not found
- `## Hierarchy Configuration`: not found

Result: CLAUDE.md exists but has no Project Configuration. The whole section has to be created and appended at the end of the file.

## Step 2 – Discover Serena Instances

Source: `evals/setup/files/mcp-tools-with-serena.md`

I matched tool names against the pattern `mcp__<instance>__<tool>` and looked for Serena tools (`find_symbol`, `get_symbols_overview`, `search_for_pattern`, `replace_symbol_body`, ...):

| Instance | Serena tools seen | Serena? |
|---|---|---|
| serena_backend | find_symbol, get_symbols_overview, search_for_pattern, find_referencing_symbols, replace_symbol_body, insert_after_symbol, insert_before_symbol, rename_symbol, get_diagnostics, list_dir | Yes |
| serena_ui | (same 10 tools) | Yes |
| atlassian | jira_get_issue, jira_search_issues, ... | No (Atlassian MCP) |

I found 2 Serena instances. Neither is in the registry yet. Simulated user answers (in place of `get_diagnostics` and the prompts):

- serena_backend → repository `backend`, role `Rust backend service`, path `/home/user/backend`
- serena_ui → repository `frontend-ui`, role `TypeScript frontend`, path `/home/user/frontend-ui`

## Step 3 – Jira Configuration

- An Atlassian MCP is present (`mcp__atlassian__*`). Per the eval rules I did not call it.
- Values the user provided:
  - Project key: TC
  - Cloud ID: 2b9e35e3-6bd3-4cec-b838-f4249ee02432
  - Feature issue type ID: 10142
  - Git Pull Request custom field: customfield_10875
  - GitHub Issue custom field: customfield_10747
- I did not need the REST API fallback.

## Step 3.5 – Hierarchy Preferences

- The section did not exist. The eval did not give any hierarchy discovery data or a grouping choice.
- Assumption: the project has an Epic-level type (standard Jira hierarchy). For a multi-repo project (2 repositories) I applied the option the skill marks as recommended, `by-repository`.

## Step 4 – Jira Field Defaults

- The eval did not supply any priority or fixVersion metadata, and I made no MCP call.
- I applied the skill's defaults: Default priority `none`, fixVersion scope `both`, Prompt for priority `true`, Prompt for fixVersion `true`.

## Step 5 – Code Intelligence

- Example instance: `serena_backend` (the first in the registry).
- Limitations: the user reported none for either instance.

## Step 7 – Constraints Template

- In a real run, the skill would copy `constraints.template.md` to `docs/constraints.md` if that file is missing. This is a simulation, so I wrote nothing.

## Step 8 – CONVENTIONS.md Scaffolding

- In a real run, the skill would check `/home/user/backend/CONVENTIONS.md` and `/home/user/frontend-ui/CONVENTIONS.md`. The eval gave no instructions for this step, so I treated it as declined/skipped and wrote nothing.

## Step 9 – Bug Configuration

- Bug issue type ID: 10001 (from Jira metadata, as the eval stated)
- Bug template path: `docs/bug-template.md` (user accepted the default)
- Bug-to-Task link type: `Blocks` (user accepted the default)
- Bug template copy: skipped (simulation)

## Step 10 – Security Configuration

- The section did not exist, so I asked whether to enable security triage. The user accepted.
- Product Lifecycle:
  - Product pages URL: https://access.example.com/product-lifecycle
  - Jira version prefix: MYPRODUCT
  - Vulnerability issue type ID: 10200
  - Component label pattern: pscomponent:
  - VEX Justification custom field: customfield_12345
  - Upstream Affected Component, PS Component and Stream custom fields, ProdSec email, ProdSec Jira account ID, Embargo policy URL: not provided, left blank
- Version Streams: `2.1.x` | `git.downstream.example.com/my-org/product-release.2.1.z` | `/home/user/product-release.2.1.z` | `security-matrix.md`
- Source Repositories: `backend` (https://github.com/example/backend), `frontend-ui` (https://github.com/example/frontend-ui). No deployment context was given, so both use the default `upstream`.
- Step 10.5 security-matrix.md scaffolding: skipped (user choice)
- Step 10.6 supportability matrix population: declined by the user

## Step 11 – Validation (against outputs/claude-md-result.md)

- [x] `# Project Configuration` heading exists
- [x] Repository Registry table has the columns Repository, Role, Serena Instance, Path (2 rows)
- [x] Jira Configuration has Project key, Cloud ID, Feature issue type ID
- [x] Jira Field Defaults has all four fields, with no placeholders
- [x] Code Intelligence documents `mcp__<instance>__<tool>`
- [x] Code Intelligence has a `### Limitations` subheading
- [ ] `docs/constraints.md`: not created (simulation)
- [x] Bug Configuration has Bug issue type ID, Bug template path, Bug-to-Task link type
- [ ] Bug template file at `docs/bug-template.md`: not created (copy skipped per instructions)
- [x] Hierarchy Configuration has Default epic grouping strategy
- [x] Security Configuration `### Product Lifecycle` has all four required fields, plus the VEX field
- [x] Security Configuration `### Version Streams` has 1 row
- [x] Security Configuration `### Source Repositories` has 2 rows
- [x] No `{{placeholder}}` markers remain
