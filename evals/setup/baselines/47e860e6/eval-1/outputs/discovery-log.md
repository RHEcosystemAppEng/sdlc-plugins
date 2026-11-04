# Discovery Log — /sdlc-workflow:setup (simulation)

## Step 1 – Read Existing Configuration

- Source: `evals/setup/files/claude-md-empty.md` (stands in for the project CLAUDE.md)
- Found: `# my-project` heading, description, `## Documentation`, `## Getting Started`
- `# Project Configuration`: NOT present
- Repository Registry, Jira Configuration, Jira Field Defaults, Code Intelligence, Bug Configuration, Security Configuration, Hierarchy Configuration: all absent
- Conclusion: the whole Project Configuration section has to be created and appended to the end of the file

## Step 2 – Discover Serena Instances

- Source: the simulated MCP tool listing in `evals/setup/files/mcp-tools-with-serena.md`. No real MCP tools were called.
- Method: matched tool names against `mcp__<instance-name>__<tool>` and looked for Serena tool names (`find_symbol`, `get_symbols_overview`, `search_for_pattern`, `replace_symbol_body`, `get_diagnostics`, ...)
- **2 Serena instances discovered:**
  1. `serena_backend`: 10 tools (find_symbol, get_symbols_overview, search_for_pattern, find_referencing_symbols, replace_symbol_body, insert_after_symbol, insert_before_symbol, rename_symbol, get_diagnostics, list_dir)
  2. `serena_ui`: the same 10 tools
- Neither instance was in the Repository Registry, because there was no registry yet.
- The path for each repository could have come from `get_diagnostics`. This was not called, so the user-supplied values were used instead (simulated user input):
  - serena_backend → repository `trustify-backend`, role `Rust backend service`, path `/home/user/trustify-backend`
  - serena_ui → repository `trustify-ui`, role `TypeScript frontend`, path `/home/user/trustify-ui`
- Other servers in the listing:
  - `mcp__atlassian__*` (Atlassian MCP): jira_get_issue, jira_search_issues, jira_edit_issue, jira_transition_issue, jira_add_comment, jira_user_info. This is not a Serena server.
  - Built-in tools (Bash, Read, Write, Edit, Glob, Grep): not MCP servers.

## Step 3 – Jira Configuration

- An Atlassian MCP server is present in the listing. The task said not to call MCP tools, so automatic discovery was skipped and the manual entry path (Step 3.4) was used.
- Source: simulated user input
  - Project key: TC
  - Cloud ID: 2b9e35e3-6bd3-4cec-b838-f4249ee02432
  - Feature issue type ID: 10142
  - Git Pull Request custom field: customfield_10875
  - GitHub Issue custom field: customfield_10747
- No REST API fallback was used, and no credentials were collected or stored.

## Step 3.5 – Hierarchy Preferences

- Discovering the issue type hierarchy needs `getJiraProjectIssueTypesMetadata`. That tool is not in the simulated listing, MCP calls were forbidden, and the task gave no hierarchy data or grouping strategy.
- There was no evidence of an Epic-level (level-1) issue type, so no grouping strategy could be chosen.
- Result: `## Hierarchy Configuration` was **not created**. A later setup run can add it once hierarchy metadata is available.

## Step 4 – Jira Field Defaults

- Discovering priorities and fixVersions needs `getJiraIssueTypeMetaWithFields`. That tool is not in the simulated listing, MCP calls were forbidden, and the task gave no values.
- The skill's documented defaults were used: Default priority = none, fixVersion scope = both, Prompt for priority = true, Prompt for fixVersion = true.

## Step 5 – Code Intelligence

- Source: the instances discovered in Step 2. The concrete example uses `serena_backend`, the first entry in the Repository Registry.
- Limitations: the simulated user reported none for either instance.

## Step 7 – Constraints Template

- Writing `docs/constraints.md` was not done. This is a simulation, and the task allowed writes only to `outputs/`.

## Step 8 – CONVENTIONS.md Scaffolding

- Not done, because this is a simulation. The task did not say how to handle CONVENTIONS.md, and no files outside `outputs/` could be written.

## Step 9 (task "Step 8") – Bug Configuration

- Bug issue type ID: **10001**, discovered from Jira metadata (simulated, as stated in the task)
- Bug template path: **docs/bug-template.md**. The user accepted the default.
- Bug-to-Task link type: **Blocks**. The user accepted the default.
- Bug template file copy (Step 9.4): **skipped**, as the task instructed for this simulation

## Step 10 (task "Step 9") – Security Configuration

- `## Security Configuration` did not exist, so the opt-in prompt was shown:
  > "Would you like to enable security triage for this project? This configures the triage-security skill to perform CVE impact analysis across supported product versions."
- Simulated user response: **declined**
- Result: no Security Configuration section was added, and security-matrix.md scaffolding was skipped.

## Step 11 – Validation (against outputs/claude-md-result.md)

- [x] `# Project Configuration` heading exists
- [x] `## Repository Registry` table has the columns Repository, Role, Serena Instance, Path (2 rows)
- [x] `## Jira Configuration` has Project key, Cloud ID, and Feature issue type ID, plus both optional custom fields
- [x] `### Jira Field Defaults` has valid values
- [x] `## Code Intelligence` documents `mcp__<instance>__<tool>`
- [x] `## Code Intelligence` has a `### Limitations` subheading
- [ ] `docs/constraints.md`: not written (simulation)
- [x] `## Bug Configuration` has Bug issue type ID, Bug template, and Bug-to-Task link type
- [ ] Bug template file at `docs/bug-template.md`: copy skipped, as the task instructed
- [n/a] Hierarchy Configuration: not created (no hierarchy data)
- [n/a] Security Configuration: the user declined
