# Discovery Log — /sdlc-workflow:setup (simulated)

Skill source: `plugins/sdlc-workflow/skills/setup/SKILL.md` (the Skill tool did not recognise `sdlc-workflow:setup`, so I followed SKILL.md directly). Template: `project-config.template.md`.

## Step 1 — Read existing configuration

- Source: `evals/setup/files/claude-md-empty.md`
- Found: `# my-project`, `## Documentation`, `## Getting Started`
- No `# Project Configuration` heading, so every subsection needs to be created:
  - Repository Registry: missing
  - Jira Configuration / Jira Field Defaults: missing
  - Code Intelligence: missing
  - Bug Configuration: missing
  - Security Configuration: missing
  - Hierarchy Configuration: missing

## Step 2 — Serena instances

- Source: `evals/setup/files/mcp-tools-with-serena.md` (simulated tool listing; no MCP calls made)
- Pattern matched: `mcp__<instance>__<tool>` with Serena tool names (`find_symbol`, `get_symbols_overview`, `search_for_pattern`, `replace_symbol_body`, `get_diagnostics`, ...)
- Discovered instances:
  | Instance | Evidence | Repository (user) | Role (user) | Path (user) |
  |---|---|---|---|---|
  | serena_backend | 10 tools, including `mcp__serena_backend__find_symbol` and `mcp__serena_backend__get_diagnostics` | trustify-backend | Rust backend service | /home/user/trustify-backend |
  | serena_ui | 10 tools, including `mcp__serena_ui__find_symbol` and `mcp__serena_ui__get_diagnostics` | trustify-ui | TypeScript frontend | /home/user/trustify-ui |
- Neither instance was already in a Repository Registry, so both are new.
- Paths came from the user. `get_diagnostics` exists for both instances but was not called (simulation).

## Step 3 — Jira Configuration

- Atlassian MCP detected in the listing (`mcp__atlassian__*`: jira_get_issue, jira_search_issues, jira_edit_issue, jira_transition_issue, jira_add_comment, jira_user_info). No MCP calls were made, as the eval requires.
- The listing does not include the discovery tools `getVisibleJiraProjects`, `getAccessibleAtlassianResources` or `getJiraProjectIssueTypesMetadata`.
- All values came from the user (equivalent to Step 3.4 manual entry):
  - Project key: TC
  - Cloud ID: 2b9e35e3-6bd3-4cec-b838-f4249ee02432
  - Feature issue type ID: 10142
  - Git Pull Request custom field: customfield_10875
  - GitHub Issue custom field: customfield_10747
- REST API fallback was not used, and no credentials were stored.

## Step 3.5 — Hierarchy Configuration

- No issue type hierarchy data was given for the simulation, and no Jira metadata calls were allowed. Without hierarchy data I could not confirm a level-1 (Epic) type or get a grouping strategy from the user.
- Result: Hierarchy Configuration was **not created**. Re-run setup with Jira access to add it.

## Step 4 — Jira Field Defaults

- `getJiraIssueTypeMetaWithFields` was not called (simulation). Available priorities and fixVersions were not discovered.
- No user values were given, so I applied the skill's documented defaults:
  - Default priority: none (no default pre-selection)
  - fixVersion scope: both (skill default)
  - Prompt for priority: true (skill default)
  - Prompt for fixVersion: true (skill default)

## Step 5 — Code Intelligence

- Naming convention `mcp__<instance>__<tool>` documented. The example uses the first registry instance, `serena_backend`.
- Limitations: the user reported none for either instance.

## Step 7 — Constraints template

- Simulation: `docs/constraints.md` was not checked or created. In a real run it would be copied from `constraints.template.md` if missing.

## Step 8 — CONVENTIONS.md scaffolding

- Simulation: no files were checked or written at /home/user/trustify-backend or /home/user/trustify-ui. In a real run, setup would offer to scaffold each repo from `conventions.template.md`.

## Step 9 (eval "Step 8") — Bug Configuration

- Bug issue type ID: 10001 (from Jira project issue type metadata, an issue type named "Bug", as the eval specifies)
- Bug template path: `docs/bug-template.md` (user accepted the default)
- Bug-to-Task link type: Blocks (user accepted the default)
- Template copy (Step 9.4): skipped because this is a simulation.

## Step 10 (eval "Step 9") — Security Configuration

- The user was asked whether to enable security triage and declined.
- Security Configuration was not created. security-matrix.md was not scaffolded.

## Step 11 — Validation (against the generated output)

- [x] `# Project Configuration` heading exists
- [x] Repository Registry table has the columns Repository, Role, Serena Instance, Path (2 rows)
- [x] Jira Configuration has Project key, Cloud ID, Feature issue type ID
- [x] Jira Field Defaults has all 4 fields, with no placeholders
- [x] Code Intelligence documents `mcp__<instance>__<tool>`
- [x] Code Intelligence has a `### Limitations` subheading
- [ ] `docs/constraints.md`: not verified (simulation)
- [x] Bug Configuration has Bug issue type ID, Bug template, Bug-to-Task link type
- [ ] Bug template file: not created (copy skipped in simulation)
- [n/a] Hierarchy Configuration: not scaffolded
- [n/a] Security Configuration: declined
