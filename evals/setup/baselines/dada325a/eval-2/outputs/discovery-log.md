# Discovery Log — /sdlc-workflow:setup (simulated)

Inputs:
- Existing CLAUDE.md: `evals/setup/files/claude-md-configured.md`
- MCP tool listing: `evals/setup/files/mcp-tools-with-serena.md`
- No real MCP tools were called. No Bash commands were run.

## Step 1: Read existing configuration

| Section | Status | Details |
|---|---|---|
| `# Project Configuration` | Present | |
| `## Repository Registry` | Present | 1 row: `trustify-backend` / Rust backend service / `serena_backend` / `/home/user/trustify-backend` |
| `## Jira Configuration` | Present, all required fields set | Project key TC, Cloud ID 2b9e35e3-..., Feature issue type ID 10142, plus both optional custom fields (customfield_10875, customfield_10747) |
| `### Jira Field Defaults` | Missing | |
| `## Code Intelligence` | Present | Documents `serena_backend` only. Limitations: one entry for `serena_backend` |
| `## Bug Configuration` | Present, all fields set | 10001 / docs/bug-template.md / Blocks |
| `## Security Configuration` | Missing | |
| `## Hierarchy Configuration` | Missing | |

## Step 2: Discover Serena instances

Tool names matching `mcp__<instance>__<tool>` that contain Serena tools (`find_symbol`, `get_symbols_overview`, `search_for_pattern`, `replace_symbol_body`, ...):

| Instance | Evidence | Already in Registry? |
|---|---|---|
| `serena_backend` | 10 tools, e.g. `mcp__serena_backend__find_symbol` | Yes (trustify-backend) |
| `serena_ui` | 10 tools, e.g. `mcp__serena_ui__find_symbol` | **No, new instance** |

`mcp__atlassian__*` is not Serena; it was excluded (it is the Atlassian MCP server).

New instance `serena_ui`: the skill would normally call `mcp__serena_ui__get_diagnostics` for the project root. MCP calls were not allowed here, so the user's answers were used:
- Repository short name: `trustify-ui`
- Role: `TypeScript frontend`
- Path: `/home/user/trustify-ui`

Result: 1 Registry row to add.

## Step 3: Jira Configuration

All three required fields are present (and both optional ones too). Result: **Jira Configuration is up to date**, no changes.

Atlassian MCP was found (`mcp__atlassian__*`), but this step did not need it.

## Step 3.5: Hierarchy Preferences

`## Hierarchy Configuration` is missing. Discovery needs `getJiraProjectIssueTypesMetadata` via MCP or the REST fallback. Both are forbidden in this eval, and the scenario gave no user answer for the hierarchy or the grouping strategy.
Result: **Deferred**. The section was not created. Writing an invented strategy would be fabricated configuration. Re-run setup with Jira access to add it.

## Step 4: Jira Field Defaults

`### Jira Field Defaults` is missing. Discovery needs `getJiraIssueTypeMetaWithFields`, which is forbidden here, and the scenario gave no user answers for these fields.
Result: **Deferred**. The subsection was not created. Re-run setup with Jira access to add it.

## Step 5: Code Intelligence

The section exists but only covers `serena_backend`. `serena_ui` was added to the Registry in Step 2, so the user was asked about its limitations. Answer: none known.
Result: add `- \`serena_ui\`: No known limitations` under `### Limitations`. The existing naming-convention text, the `serena_backend` example and the `serena_backend` limitation are kept unchanged.

## Step 6: Write configuration

Only the changed subsections were updated: the Registry (+1 row) and Code Intelligence > Limitations (+1 line). Everything else was kept as it was. Output: `outputs/claude-md-result.md`.

## Step 7: Constraints template

Not checked. The file system checks and writes to the target project fall outside this eval's scope (writes are limited to outputs/). In a real run: create `docs/constraints.md` from `constraints.template.md` if it is missing.

## Step 8: CONVENTIONS.md

Not performed (writes outside outputs/ are forbidden). In a real run, the skill would check for `CONVENTIONS.md` at `/home/user/trustify-backend` and at the new `/home/user/trustify-ui`, and offer to scaffold any that are missing.

## Step 9: Bug Configuration

All three fields are present with no placeholders. Result: **Bug Configuration is up to date**.

## Step 10: Security Configuration (optional)

The section is missing. The user was asked: "Would you like to enable security triage for this project?" The user **declined**.
Result: skipped. No Security Configuration section was added and no security-matrix.md was scaffolded.

## Step 11: Validation (on the generated output)

- [x] `# Project Configuration` heading exists
- [x] Repository Registry table has the columns Repository, Role, Serena Instance, Path (2 rows)
- [x] Jira Configuration has Project key, Cloud ID, Feature issue type ID
- [x] Code Intelligence documents the `mcp__<instance>__<tool>` convention
- [x] Code Intelligence has a `### Limitations` subheading covering both instances
- [x] Bug Configuration has all three fields
- [ ] Jira Field Defaults: not configured (deferred)
- [ ] Hierarchy Configuration: not configured (deferred)
- [-] Security Configuration: not scaffolded (user declined; not required)
- [-] docs/constraints.md: not verified in this simulation
