# Discovery Log — /sdlc-workflow:setup (simulated)

## Step 1 – Read Existing Configuration

Source: `evals/setup/files/claude-md-empty.md`

- `# Project Configuration` heading: NOT found
- `## Repository Registry`: not present (no repositories recorded)
- `## Jira Configuration`: not present
- `### Jira Field Defaults`: not present
- `## Code Intelligence`: not present
- `## Bug Configuration`: not present
- `## Security Configuration`: not present
- `## Hierarchy Configuration`: not present

Conclusion: CLAUDE.md exists but has no Project Configuration; the full section must be created and appended at the end of the file.

## Step 2 – Discover Serena Instances

Source: `evals/setup/files/mcp-tools-with-serena.md` (simulated tool listing; no MCP tools were called).

Tools matching `mcp__<instance>__<tool>` with Serena tool names (`find_symbol`, `get_symbols_overview`, `search_for_pattern`, `replace_symbol_body`, ...):

| Instance | Evidence | Already in Registry? |
|---|---|---|
| serena_backend | 10 tools incl. find_symbol, get_symbols_overview, search_for_pattern, replace_symbol_body, get_diagnostics | No |
| serena_ui | 10 tools incl. find_symbol, get_symbols_overview, search_for_pattern, replace_symbol_body, get_diagnostics | No |

`mcp__atlassian__*` tools were seen but are not Serena (they don't have Serena tool names), so they were excluded.

Both instances provide `get_diagnostics`. Since this is a simulation, the paths came from the user's answers instead of calling it:

- serena_backend → repository `backend`, role `Rust backend service`, path `/home/user/backend`
- serena_ui → repository `frontend-ui`, role `TypeScript frontend`, path `/home/user/frontend-ui`

## Step 3 – Jira Configuration

- Atlassian MCP present (`mcp__atlassian__*`): yes, but it was not called in this simulation. The listing also has no `getVisibleJiraProjects`, `getAccessibleAtlassianResources` or `getJiraProjectIssueTypesMetadata` tools.
- Values provided by the user (manual entry path, Step 3.4):
  - Project key: TC
  - Cloud ID: 2b9e35e3-6bd3-4cec-b838-f4249ee02432
  - Feature issue type ID: 10142
  - Git Pull Request custom field: customfield_10875
  - GitHub Issue custom field: customfield_10747
- REST API fallback: not used. No Bash commands were run.

## Step 3.5 – Hierarchy Preferences

- No issue type hierarchy data was available. The simulated Atlassian MCP has no `getJiraProjectIssueTypesMetadata` tool, and the scenario gave no hierarchy levels or grouping strategy.
- Whether a level-1 (Epic) type exists could not be confirmed, so the grouping strategy question was not asked and `## Hierarchy Configuration` was NOT created. To add it later, re-run setup once hierarchy metadata is available.

## Step 4 – Jira Field Defaults

- `getJiraIssueTypeMetaWithFields` was not called (simulation). No priority or fixVersion lists were available.
- The scenario gave no answers, so the documented defaults were used: Default priority = none, fixVersion scope = both, Prompt for priority = true, Prompt for fixVersion = true.

## Step 5 – Code Intelligence

- The section was generated with the `mcp__<instance>__<tool>` naming convention and an example using the first Registry instance (`serena_backend`).
- Limitations: the user reported none for `serena_backend` or `serena_ui`.

## Step 7 – Constraints Template

- Would check `docs/constraints.md` in the target project. It was not written because file modifications are out of scope for this simulation.

## Step 8 – CONVENTIONS.md Scaffolding

- Would check `/home/user/backend/CONVENTIONS.md` and `/home/user/frontend-ui/CONVENTIONS.md`. The scenario gave no answer and file writes are out of scope, so nothing was scaffolded.

## Step 9 – Bug Configuration

- Bug issue type ID: 10001 (from Jira metadata, as stated in the scenario)
- Bug template path: `docs/bug-template.md` (default accepted)
- Bug-to-Task link type: `Blocks` (default accepted)
- Bug template copy: skipped (simulation)

## Step 10 – Security Configuration

- Section absent. The user ACCEPTED enabling security triage.
- Product Lifecycle (from the user):
  - Product pages URL: https://access.example.com/product-lifecycle
  - Jira version prefix: MYPRODUCT
  - Vulnerability issue type ID: 10200
  - Component label pattern: pscomponent:
  - VEX Justification custom field: customfield_12345
  - Upstream Affected Component / PS Component / Stream custom fields, ProdSec email, ProdSec Jira account ID, Embargo policy URL: not provided, left blank
- Version Streams: 1
  - 2.1.x | git.downstream.example.com/my-org/product-release.2.1.z | /home/user/product-release.2.1.z | security-matrix.md
- Source Repositories: 2. No deployment context was given, so the default `upstream` was used for both.
  - backend | https://github.com/example/backend
  - frontend-ui | https://github.com/example/frontend-ui
- security-matrix.md scaffolding (Step 10.5): the user skipped it
- Supportability matrix population (Step 10.6): the user declined
