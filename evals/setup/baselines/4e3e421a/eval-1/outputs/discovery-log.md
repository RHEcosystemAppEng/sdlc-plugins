# Discovery Log — /sdlc-workflow:setup (simulated)

Note: the Skill tool did not recognize `sdlc-workflow:setup`, so I followed
`plugins/sdlc-workflow/skills/setup/SKILL.md` and `project-config.template.md` directly.
I did not call any MCP tools. All discovery is simulated from the input files and the
answers supplied in the task.

## Step 1 — Read existing configuration

- Source: `evals/setup/files/claude-md-empty.md`
- Found: `# my-project`, `## Documentation`, `## Getting Started`
- Not found: `# Project Configuration`, Repository Registry, Jira Configuration,
  Jira Field Defaults, Code Intelligence, Bug Configuration, Security Configuration,
  Hierarchy Configuration
- Conclusion: greenfield. Every Project Configuration section has to be created.

## Step 2 — Serena instances

- Source: `evals/setup/files/mcp-tools-with-serena.md`
- Pattern used: `mcp__<instance>__<tool>`, with Serena tool names such as `find_symbol`,
  `get_symbols_overview`, `search_for_pattern` and `replace_symbol_body`
- Discovered instances (10 tools each, including `get_diagnostics`):
  - `serena_backend`
  - `serena_ui`
- `mcp__atlassian__*` was not counted as a Serena instance because its tools are Jira operations.
- Neither instance was in the Repository Registry, because no registry existed.
- Path, name and role came from the user's answers. `get_diagnostics` was available but not called, since this is a simulation.
  - serena_backend → `trustify-backend`, "Rust backend service", `/home/user/trustify-backend`
  - serena_ui → `trustify-ui`, "TypeScript frontend", `/home/user/trustify-ui`

## Step 3 — Jira Configuration

- An Atlassian MCP was found in the tool listing (`mcp__atlassian__jira_*`), but I did not call it.
- Values came from the user:
  - Project key: TC
  - Cloud ID: 2b9e35e3-6bd3-4cec-b838-f4249ee02432
  - Feature issue type ID: 10142
  - Git Pull Request custom field: customfield_10875
  - GitHub Issue custom field: customfield_10747

## Step 3.5 — Hierarchy Configuration

- The task did not give a hierarchy. I assumed the project has a level-1 Epic type, as
  is standard in Jira, so the grouping question applies.
- Strategy: `by-repository`. I chose the option the skill recommends for multi-repo
  projects, because this project has two repositories. This is an assumption, not a user answer.

## Step 4 — Jira Field Defaults

- Priority and fixVersion discovery via `getJiraIssueTypeMetaWithFields` was not run.
- The task gave no values, so I used the skill defaults: Default priority `none`,
  fixVersion scope `both`, Prompt for priority `true`, Prompt for fixVersion `true`.

## Step 5 — Code Intelligence

- The naming convention and example use the first registry instance (`serena_backend`).
- Limitations: the user reported none for either instance.

## Step 7 — Constraints template

- Copying `docs/constraints.md` was not performed because this is a simulation and writing outside outputs/ is not allowed.

## Step 8 — CONVENTIONS.md scaffolding

- Not performed, for the same reason. No answers were given for this step.

## Step 9 — Bug Configuration (the task calls this "Step 8")

- Bug issue type ID: 10001. Assumed to come from Jira issue type metadata (an issue type named "Bug").
- Bug template path: `docs/bug-template.md` (the user accepted the default)
- Bug-to-Task link type: `Blocks` (the user accepted the default)
- Copying the bug template was skipped, as the task instructed.

## Step 10 — Security Configuration (the task calls this "Step 9")

- No existing section was found.
- I asked: "Would you like to enable security triage for this project?" The user declined.
- No Security Configuration section was created.

## Step 11 — Validation (against outputs/claude-md-result.md)

- `# Project Configuration` heading: present
- Repository Registry table has the columns Repository, Role, Serena Instance, Path: present (2 rows)
- Jira Configuration has Project key, Cloud ID and Feature issue type ID: present
- Jira Field Defaults has all 4 fields: present
- Code Intelligence documents `mcp__<instance>__<tool>`: present
- `### Limitations` subheading: present
- Bug Configuration has 3 fields: present
- Hierarchy Configuration has Default epic grouping strategy: present
- Security Configuration: absent, as intended (the user declined)
- `docs/constraints.md` and the bug template file: not created (simulation)
