# Discovery Log — /sdlc-workflow:setup (simulated)

The `/sdlc-workflow:setup` skill was not available through the Skill tool. I followed `plugins/sdlc-workflow/skills/setup/SKILL.md` and `project-config.template.md` directly. This was a simulation: I called no MCP tools, ran no Bash commands, and modified no project files.

## Step 1 – Read Existing Configuration

Source: `evals/setup/files/claude-md-empty.md`

- CLAUDE.md exists.
- `# Project Configuration` heading: **not found**
- `## Repository Registry`: not found. No repositories are registered.
- `## Jira Configuration` / `### Jira Field Defaults`: not found
- `## Code Intelligence`: not found
- `## Bug Configuration`: not found
- `## Security Configuration`: not found
- `## Hierarchy Configuration`: not found
- Existing non-configuration content: the project heading (`# my-project`), the description, `## Documentation` and `## Getting Started`.

Conclusion: every Project Configuration section has to be created and appended at the end of the file.

## Step 2 – Discover Serena Instances

Source: `evals/setup/files/mcp-tools-with-serena.md` (simulated MCP tool listing)

I matched tool names against the pattern `mcp__<instance>__<tool>`, looking for typical Serena tools such as `find_symbol`, `get_symbols_overview`, `search_for_pattern` and `replace_symbol_body`. **I found 2 Serena instances:**

| Instance | Evidence (tools found) |
|---|---|
| `serena_backend` | find_symbol, get_symbols_overview, search_for_pattern, find_referencing_symbols, replace_symbol_body, insert_after_symbol, insert_before_symbol, rename_symbol, get_diagnostics, list_dir |
| `serena_ui` | find_symbol, get_symbols_overview, search_for_pattern, find_referencing_symbols, replace_symbol_body, insert_after_symbol, insert_before_symbol, rename_symbol, get_diagnostics, list_dir |

Neither instance was in the Repository Registry, because there was no Registry. Both instances list `get_diagnostics`, but I did not call it. The simulated user supplied each repository's details instead:

- `serena_backend` → repository `trustify-backend`, role `Rust backend service`, path `/home/user/trustify-backend`
- `serena_ui` → repository `trustify-ui`, role `TypeScript frontend`, path `/home/user/trustify-ui`

The Atlassian tools (`mcp__atlassian__*`) are not Serena tools, so I left them out of the Registry.

## Step 3 – Jira Configuration

- Source: the simulated user's input.
- Atlassian MCP **is present** in the listing (`mcp__atlassian__jira_get_issue`, `jira_search_issues`, `jira_edit_issue`, `jira_transition_issue`, `jira_add_comment`, `jira_user_info`).
- The task forbids MCP calls, so I ran no project, cloud-ID or issue-type discovery calls and used no REST fallback.
- Values the user provided:
  - Project key: TC
  - Cloud ID: 2b9e35e3-6bd3-4cec-b838-f4249ee02432
  - Feature issue type ID: 10142
  - Git Pull Request custom field: customfield_10875
  - GitHub Issue custom field: customfield_10747

## Step 3.5 – Hierarchy Preferences

- I could not run hierarchy discovery. The tool listing has no `getJiraProjectIssueTypesMetadata`, and MCP calls are not allowed anyway.
- The eval prompt gave no hierarchy input. **Assumption:** project TC has an Epic type at level 1, as in the skill's own TC example (Level 1: Epic, id 10000). I also assumed the user chose the option the skill recommends for multi-repo projects: `by-repository`. This value is an assumption, not a discovery.

## Step 4 – Jira Field Defaults

- I could not discover priorities or fixVersions (`getJiraIssueTypeMetaWithFields` cannot be called in this simulation).
- The eval prompt gave no input, so I used the skill's documented defaults: Default priority `none`, fixVersion scope `both`, Prompt for priority `true`, Prompt for fixVersion `true`.

## Step 5 – Code Intelligence

- I wrote the naming convention `mcp__<instance>__<tool>` with an example that uses the first registered instance, `serena_backend`.
- Limitations: the simulated user reported **none** for either instance.

## Step 7 – Constraints Template

- This simulation did not write `docs/constraints.md`, because the task allows writes only to `outputs/`. In a real run, the skill would copy `constraints.template.md` if `docs/constraints.md` is missing.

## Step 8 – CONVENTIONS.md Scaffolding

- I skipped this step because the task allows no writes outside `outputs/`. It is optional and does not block setup.

## Step 9 – Bug Configuration (the eval prompt calls this "Step 8")

- Bug issue type ID: **10001**. Per the eval prompt, this came from Jira metadata (the issue type named "Bug").
- Bug template path: the user accepted the default, `docs/bug-template.md`.
- Bug-to-Task link type: the user accepted the default, `Blocks`.
- I skipped copying the bug template file, as the eval instructed.

## Step 10 – Security Configuration (the eval prompt calls this "Step 9")

- `## Security Configuration` did not exist, so the skill showed the opt-in prompt:
  > "Would you like to enable security triage for this project? This configures the triage-security skill to perform CVE impact analysis across supported product versions."
- The simulated user **declined**, so I collected no security fields, scaffolded no security-matrix.md and added no Security Configuration section.

## Step 11 – Validation (performed against outputs/claude-md-result.md)

| Check | Result |
|---|---|
| `# Project Configuration` heading exists | Pass |
| Registry table has columns Repository, Role, Serena Instance, Path | Pass (2 rows) |
| Jira Configuration has Project key, Cloud ID, Feature issue type ID | Pass (all 5 fields) |
| Jira Field Defaults has valid values | Pass |
| Code Intelligence documents `mcp__<instance>__<tool>` | Pass |
| Code Intelligence has `### Limitations` | Pass |
| Bug Configuration has all three fields | Pass |
| Hierarchy Configuration has Default epic grouping strategy | Pass (assumed value) |
| Security Configuration | Not scaffolded (user declined) |
| `docs/constraints.md` exists / bug template file exists | Not applicable (simulation, no writes outside outputs/) |
