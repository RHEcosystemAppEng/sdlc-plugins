# Discovery Log — /sdlc-workflow:setup (simulated)

Skill followed: `plugins/sdlc-workflow/skills/setup/SKILL.md` (read directly; template `project-config.template.md`).

## Step 1 – Read Existing Configuration

- Source: `evals/setup/files/claude-md-empty.md`
- Found: `# my-project`, `## Documentation`, `## Getting Started`.
- Not found: `# Project Configuration` and all its subsections (Repository Registry, Jira Configuration, Jira Field Defaults, Code Intelligence, Bug Configuration, Security Configuration, Hierarchy Configuration).
- Conclusion: greenfield — the entire Project Configuration section must be created and appended at the end of the file.

## Step 2 – Discover Serena Instances

- Source: `evals/setup/files/mcp-tools-with-serena.md` (simulated MCP tool listing; no real MCP calls made).
- Pattern matched: `mcp__<instance>__<tool>` with Serena tool names (`find_symbol`, `get_symbols_overview`, `search_for_pattern`, `replace_symbol_body`, `get_diagnostics`, ...).
- Discovered instances:
  - `serena_backend` (10 tools, includes `get_diagnostics`)
  - `serena_ui` (10 tools, includes `get_diagnostics`)
- `mcp__atlassian__*` tools are not Serena (no symbol tools) — excluded.
- Neither instance was in a Repository Registry (none existed).
- Repository details (simulated user answers; `get_diagnostics` not called):
  - serena_backend → `trustify-backend`, role "Rust backend service", path `/home/user/trustify-backend`
  - serena_ui → `trustify-ui`, role "TypeScript frontend", path `/home/user/trustify-ui`

## Step 3 – Jira Configuration

- Atlassian MCP detected in listing (`mcp__atlassian__jira_get_issue`, `jira_search_issues`, `jira_edit_issue`, `jira_transition_issue`, `jira_add_comment`, `jira_user_info`). The discovery tools named in the skill (`getVisibleJiraProjects`, `getAccessibleAtlassianResources`, `getJiraProjectIssueTypesMetadata`) are not in the listing, and MCP calls are forbidden in this eval, so no auto-discovery was performed.
- Values provided by the user (simulated):
  - Project key: TC
  - Cloud ID: 2b9e35e3-6bd3-4cec-b838-f4249ee02432
  - Feature issue type ID: 10142
  - Git Pull Request custom field: customfield_10875
  - GitHub Issue custom field: customfield_10747
- No REST API fallback used (Bash disallowed; no credentials needed since values were supplied).

## Step 3.5 – Hierarchy Preferences

- Issue-type hierarchy discovery (`getJiraProjectIssueTypesMetadata`) could not be performed, and the eval scenario provided no hierarchy data or grouping-strategy answer.
- Result: `## Hierarchy Configuration` NOT created. The skill only creates it once a level-1 (Epic) type is confirmed and the user chooses a strategy. Re-run setup with Jira access to add it.

## Step 4 – Jira Field Defaults

- Priority/fixVersion values (`getJiraIssueTypeMetaWithFields`) not discovered (no MCP calls allowed).
- The scenario gave no answers, so the skill's documented defaults were used: Default priority = none, fixVersion scope = both, Prompt for priority = true, Prompt for fixVersion = true.

## Step 5 – Code Intelligence

- Naming convention documented; example uses the first registry instance, `serena_backend`.
- Limitations: user reports none for either instance (simulated).

## Step 6 – Write Configuration

- CLAUDE.md exists without `# Project Configuration` → section appended at end of file. Result written to `outputs/claude-md-result.md` only; the real file was not modified.

## Step 7 – Constraints Template

- Would check for `docs/constraints.md` in the target project and copy `constraints.template.md` if missing. Skipped in this simulation (no file writes outside outputs/).

## Step 8 – CONVENTIONS.md scaffolding

- Would check `/home/user/trustify-backend/CONVENTIONS.md` and `/home/user/trustify-ui/CONVENTIONS.md`. Not performed in this simulation (no filesystem access to those paths, no writes allowed). The scenario gave no answer.

## Bug Configuration (the task's "Step 8"; Step 9 in the current SKILL.md)

- Bug issue type ID: 10001 — discovered from Jira issue-type metadata (simulated; type named "Bug").
- Bug template path: `docs/bug-template.md` — user accepted the default.
- Bug-to-Task link type: `Blocks` — user accepted the default.
- Bug template copy (from `docs/templates/bug-template.md`): skipped, as instructed for the simulation.

## Security Configuration (the task's "Step 9"; Step 10 in the current SKILL.md)

- `## Security Configuration` absent → asked the user whether to enable security triage.
- User declined → section not created; Steps 10.1–10.6 skipped.

## Step 11 – Validate (against outputs/claude-md-result.md)

- [x] `# Project Configuration` heading exists
- [x] `## Repository Registry` table has columns Repository, Role, Serena Instance, Path (2 rows)
- [x] `## Jira Configuration` has Project key, Cloud ID, Feature issue type ID
- [x] `### Jira Field Defaults` has all four fields, no placeholders
- [x] `## Code Intelligence` documents `mcp__<instance>__<tool>`
- [x] `## Code Intelligence` has `### Limitations`
- [ ] `docs/constraints.md` — not checked or created (simulation)
- [x] `## Bug Configuration` has Bug issue type ID, Bug template path, Bug-to-Task link type
- [ ] Bug template file at `docs/bug-template.md` — copy skipped (simulation)
- [n/a] Hierarchy Configuration — not scaffolded
- [n/a] Security Configuration — user declined
- [x] No `{{placeholder}}` markers left
