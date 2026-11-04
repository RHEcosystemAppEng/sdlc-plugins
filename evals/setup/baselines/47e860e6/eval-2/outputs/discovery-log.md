# Setup Discovery Log

Skill: `/sdlc-workflow:setup` (the Skill tool reported it as unknown, so I followed `plugins/sdlc-workflow/skills/setup/SKILL.md` and `project-config.template.md` directly)
Mode: simulated. No MCP tools were called, no Bash commands were run, and no project files were changed.

## Step 1: Read existing configuration

Source: `evals/setup/files/claude-md-configured.md`

| Section | Status | Details |
|---|---|---|
| `# Project Configuration` | Present | |
| `## Repository Registry` | Present | 1 entry: `trustify-backend` (Rust backend service, `serena_backend`, `/home/user/trustify-backend`) |
| `## Jira Configuration` | Present, all required fields set | Project key TC, Cloud ID 2b9e35e3-6bd3-4cec-b838-f4249ee02432, Feature issue type ID 10142, plus both optional custom fields (customfield_10875, customfield_10747) |
| `### Jira Field Defaults` | Absent | |
| `## Code Intelligence` | Present | Documents `serena_backend`. Limitations lists `serena_backend` (rust-analyzer indexing delay) |
| `## Bug Configuration` | Present, fully populated | Type ID 10001, template `docs/bug-template.md`, link type Blocks |
| `## Security Configuration` | Absent | |
| `## Hierarchy Configuration` | Absent | |

## Step 2: Discover Serena instances

Source: `evals/setup/files/mcp-tools-with-serena.md`. I matched tool names against the `mcp__<instance>__<tool>` pattern and confirmed each instance by the Serena tool names it exposes (`find_symbol`, `get_symbols_overview`, `search_for_pattern`, `replace_symbol_body`, `get_diagnostics`, ...).

| Instance | Serena tools found | Already in Registry? | Action |
|---|---|---|---|
| `serena_backend` | 10 | Yes (`trustify-backend`) | Keep as is |
| `serena_ui` | 10 | No | New instance. Ask the user for details |

`mcp__atlassian__*` is not a Serena instance (no Serena tool names), so it was left out.

Simulated user prompt for `serena_ui` (I did not call `get_diagnostics`, because MCP calls are not allowed here):
- Repository short name: `trustify-ui`
- Role: `TypeScript frontend`
- Local path: `/home/user/trustify-ui`

Result: one new Registry row was added.

## Step 3: Jira Configuration

All three required fields plus both optional custom fields are already set. **Jira Configuration is up to date.** Nothing was asked.

(An Atlassian MCP does appear in the listing, but I did not use it because Step 3 was skipped.)

## Step 3.5: Hierarchy Preferences

`## Hierarchy Configuration` is absent. Filling it requires discovering the issue-type hierarchy through `getJiraProjectIssueTypesMetadata` (MCP or REST fallback) and then asking the user to pick an Epic grouping strategy. This eval forbids MCP calls and gave no answer for the strategy, so **I did not add the section**. I did not invent a value. A follow-up run of setup with Jira access is needed.

## Step 4: Jira Field Defaults

`### Jira Field Defaults` is absent. Filling it requires discovering priorities and fixVersions through `getJiraIssueTypeMetaWithFields` and then getting the user's choices. That was not possible in this eval and no answers were given, so **I did not add the subsection**. A follow-up run is needed.

## Step 5: Code Intelligence

The section exists and documents `serena_backend`. Because `serena_ui` was added in Step 2, I asked the user about limitations (simulated). The answer was **no known limitations**, so I added `serena_ui: No known limitations` under `### Limitations`. I kept the existing naming-convention text, the `serena_backend` example and the `serena_backend` limitation unchanged.

## Step 6: Write configuration

`# Project Configuration` exists, so only the changed subsections were updated: Repository Registry (+1 row) and Code Intelligence > Limitations (+1 bullet). The result is in `outputs/claude-md-result.md`.

## Step 7: Constraints template

Not run, because writing files is limited to `outputs/`. In a real run, setup would check whether `docs/constraints.md` exists in the target project and copy the template only if it is missing.

## Step 8: Scaffold CONVENTIONS.md

Not run, because writing files is limited to `outputs/`. In a real run, setup would check `/home/user/trustify-backend/CONVENTIONS.md` and `/home/user/trustify-ui/CONVENTIONS.md` and offer to scaffold any that are missing. The new `trustify-ui` repository would be the most likely candidate.

## Step 9: Bug Configuration

All three fields are present with no placeholders. **Bug Configuration is up to date.**

## Step 10: Security Configuration (optional)

`## Security Configuration` is absent. I asked the user: "Would you like to enable security triage for this project?" The simulated user **declined**, so the section was not scaffolded and no security-matrix files were created. (The task calls this "Step 9"; in the current SKILL.md it is Step 10.)

## Step 11: Validate (on the generated section)

- [x] `# Project Configuration` heading exists
- [x] Repository Registry table has the columns Repository, Role, Serena Instance, Path (2 rows)
- [x] Jira Configuration has Project key, Cloud ID, Feature issue type ID
- [ ] Jira Field Defaults: not configured (needs Jira discovery and user input)
- [x] Code Intelligence documents the `mcp__<instance>__<tool>` convention
- [x] Code Intelligence has a `### Limitations` subheading covering both instances
- [x] Bug Configuration has all three fields
- [ ] Hierarchy Configuration: not configured (needs Jira discovery and user input)
- [x] Security Configuration: not scaffolded because the user declined
- [ ] `docs/constraints.md`: not checked (file writes outside `outputs/` are not allowed)
