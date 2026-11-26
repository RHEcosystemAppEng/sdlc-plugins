# Discovery Log — /sdlc-workflow:setup (simulated)

Skill source: `plugins/sdlc-workflow/skills/setup/SKILL.md` (the Skill tool did not recognize `sdlc-workflow:setup`, so the SKILL.md file was followed directly). Templates used: `project-config.template.md`, `security-config.template.md`.

## Step 1 – Read Existing Configuration

- Input: `evals/setup/files/claude-md-empty.md`
- `# Project Configuration` heading: **not found**
- Repository Registry: not found (no repositories listed)
- Jira Configuration: not found
- Jira Field Defaults: not found
- Code Intelligence: not found
- Bug Configuration: not found
- Security Configuration: not found
- Hierarchy Configuration: not found
- Conclusion: the whole Project Configuration section has to be created and appended at the end of the file.

## Step 2 – Discover Serena Instances

Source: `evals/setup/files/mcp-tools-with-serena.md` (simulated, no MCP calls made)

Tools matching `mcp__<instance>__<tool>` with Serena tool names (`find_symbol`, `get_symbols_overview`, `search_for_pattern`, `replace_symbol_body`, ...):

| Instance | Evidence tools | Serena? |
|---|---|---|
| serena_backend | find_symbol, get_symbols_overview, search_for_pattern, replace_symbol_body, get_diagnostics, ... | Yes |
| serena_ui | find_symbol, get_symbols_overview, search_for_pattern, replace_symbol_body, get_diagnostics, ... | Yes |
| atlassian | jira_get_issue, jira_search_issues, ... | No (Atlassian MCP) |

Neither instance is in the Registry (there isn't one yet). `get_diagnostics` was not called (simulation). Paths and names came from the simulated user answers:

- serena_backend → repository `backend`, role `Rust backend service`, path `/home/user/backend`
- serena_ui → repository `frontend-ui`, role `TypeScript frontend`, path `/home/user/frontend-ui`

## Step 3 – Jira Configuration

- Atlassian MCP found (`mcp__atlassian__*`). Not called (simulation). Values came from the simulated user answers:
  - Project key: TC
  - Cloud ID: 2b9e35e3-6bd3-4cec-b838-f4249ee02432
  - Feature issue type ID: 10142
  - Git Pull Request custom field: customfield_10875
  - GitHub Issue custom field: customfield_10747
- No REST API fallback was used, so no REST credentials were stored.

## Step 3.5 – Hierarchy Preferences

- Not specified in the eval scenario. Simulated assumption: Jira issue-type metadata (the same metadata that gave Bug = 10001) includes an Epic-level (level 1) type, so the grouping-strategy question applies.
- Assumed answer: `by-repository`, the option the skill marks as recommended for multi-repo projects (this project has 2 repositories).

## Step 4 – Jira Field Defaults

- Not specified in the eval scenario. Priority/fixVersion values were not discovered (no MCP calls).
- Assumed skill defaults: Default priority `none`, fixVersion scope `both`, Prompt for priority `true`, Prompt for fixVersion `true`.

## Step 5 – Code Intelligence

- Section generated with the `mcp__<instance>__<tool>` naming convention and an example that uses the first Registry instance, `serena_backend`.
- Limitations: the user reported none for `serena_backend` or `serena_ui`.

## Step 7 – Constraints Template

- Would check `docs/constraints.md` and copy it from `constraints.template.md` if missing. **Skipped (simulation; only outputs/ may be written).**

## Step 8 – CONVENTIONS.md Scaffolding

- Would check `/home/user/backend/CONVENTIONS.md` and `/home/user/frontend-ui/CONVENTIONS.md`. **Skipped (simulation, no instructions given for this step).**

## Step 9 – Bug Configuration

- Bug issue type ID: `10001` (taken from Jira metadata, per the scenario)
- Bug template path: `docs/bug-template.md` (user accepted the default)
- Bug-to-Task link type: `Blocks` (user accepted the default)
- Bug template file copy: **skipped (simulation)**

## Step 10 – Security Configuration

- Section not found. User **accepted** enabling security triage.
- Product Lifecycle:
  - Product pages URL: https://access.example.com/product-lifecycle
  - Jira version prefix: MYPRODUCT
  - Vulnerability issue type ID: 10200
  - Component label pattern: pscomponent:
  - VEX Justification custom field: customfield_12345
  - Upstream Affected Component / PS Component / Stream custom fields, ProdSec email, ProdSec Jira account ID, Embargo policy URL: not provided, so left blank
- Version Streams: 1
  - 2.1.x | git.downstream.example.com/my-org/product-release.2.1.z | /home/user/product-release.2.1.z | security-matrix.md
- Source Repositories: 2
  - backend | https://github.com/example/backend | upstream (default, no context given)
  - frontend-ui | https://github.com/example/frontend-ui | upstream (default, no context given)
- Step 10.5 security-matrix.md scaffolding: **skipped by user**
- Step 10.6 supportability matrix population: **declined by user**

## Step 11 – Validation (against outputs/claude-md-result.md)

| Check | Result |
|---|---|
| `# Project Configuration` heading exists | PASS |
| Repository Registry table with Repository / Role / Serena Instance / Path | PASS (2 rows) |
| Jira Configuration has Project key, Cloud ID, Feature issue type ID | PASS |
| Jira Field Defaults has valid values | PASS |
| Code Intelligence documents `mcp__<instance>__<tool>` | PASS |
| Code Intelligence has `### Limitations` | PASS |
| `docs/constraints.md` exists | N/A (copy skipped in simulation) |
| Bug Configuration has issue type ID, template path, link type | PASS |
| Bug template file exists at path | N/A (copy skipped in simulation) |
| Hierarchy Configuration has Default epic grouping strategy | PASS |
| Security Product Lifecycle has 4 required fields | PASS |
| Version Streams has at least 1 row | PASS |
| Source Repositories has at least 1 row | PASS |
| No `{{placeholder}}` markers left | PASS |
