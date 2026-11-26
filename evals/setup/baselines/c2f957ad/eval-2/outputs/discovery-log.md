# Discovery Log — /sdlc-workflow:setup (simulated)

Inputs:
- Existing CLAUDE.md: `evals/setup/files/claude-md-configured.md`
- MCP tool listing: `evals/setup/files/mcp-tools-with-serena.md`

No real MCP tools, Bash commands, or external services were used. Discovery was simulated from the tool listing.

## Step 1 – Read Existing Configuration

| Section | Status | Details |
|---|---|---|
| `# Project Configuration` | Present | |
| `## Repository Registry` | Present | 1 entry: `trustify-backend` (Rust backend service, `serena_backend`, `/home/user/trustify-backend`) |
| `## Jira Configuration` | Present, required fields complete | Project key TC, Cloud ID 2b9e35e3-..., Feature issue type ID 10142, plus PR field customfield_10875 and GitHub Issue field customfield_10747 |
| `### Jira Field Defaults` | Missing | |
| `## Code Intelligence` | Present | Covers `serena_backend`; Limitations has 1 entry for `serena_backend` |
| `## Bug Configuration` | Present, all 3 fields filled | 10001 / docs/bug-template.md / Blocks |
| `## Security Configuration` | Missing | |
| `## Hierarchy Configuration` | Missing | |

## Step 2 – Discover Serena Instances

Looked for tool names matching `mcp__<instance>__<tool>` that include Serena tools (`find_symbol`, `get_symbols_overview`, `search_for_pattern`, `replace_symbol_body`, ...).

| Instance | Serena tools found | In Registry? | Action |
|---|---|---|---|
| `serena_backend` | 10 (find_symbol, get_symbols_overview, search_for_pattern, find_referencing_symbols, replace_symbol_body, insert_after_symbol, insert_before_symbol, rename_symbol, get_diagnostics, list_dir) | Yes (`trustify-backend`) | Keep as is |
| `serena_ui` | 10 (same set) | **No** | New instance, needs user input |

`mcp__atlassian__*` tools are not Serena tools (no symbol tools), so they were left out.

New instance `serena_ui`: per the skill, the project root comes from `get_diagnostics` or from the user. MCP calls were not allowed, so the simulated user answers were used:
- Repository short name: `trustify-ui`
- Role: `TypeScript frontend`
- Path: `/home/user/trustify-ui`

## Step 3 – Jira Configuration

All three required fields (Project key, Cloud ID, Feature issue type ID) are already filled in. Result: **"Jira Configuration is up to date"**. Nothing re-asked.

Atlassian MCP is listed (`mcp__atlassian__jira_get_issue`, `jira_search_issues`, `jira_edit_issue`, `jira_transition_issue`, `jira_add_comment`, `jira_user_info`). The listing does not include `getJiraProjectIssueTypesMetadata` or `getJiraIssueTypeMetaWithFields`.

## Step 3.5 – Hierarchy Preferences

The section is missing. Discovery needs `getJiraProjectIssueTypesMetadata`, which the tool listing does not include and which this eval does not allow calling. The scenario gives no user answers for the REST fallback prompt, the hierarchy, or the grouping strategy. **Deferred**: no section written, so no value was made up. See changes-log.md.

## Step 4 – Jira Field Defaults

The subsection is missing. Discovery needs `getJiraIssueTypeMetaWithFields`, which is not available and not allowed here. The scenario gives no user answer for default priority, scope, or prompt flags. **Deferred**: no subsection written. See changes-log.md.

## Step 5 – Code Intelligence

The section exists and covers `serena_backend`. A new instance (`serena_ui`) was added in Step 2, so the user was asked about known limitations. The simulated answer was none. The existing naming-convention text, the `serena_backend` example, and the backend limitation stay as they are. A `serena_ui` line saying there are no known limitations was added.

## Step 6 – Write Configuration

Changes: one new Registry row, plus one Limitations line for `serena_ui`. Everything else is preserved word for word. The output went to `outputs/claude-md-result.md` and the real CLAUDE.md was not changed.

## Step 7 – Constraints Template

Simulated only. The file system of the target project (trustify-backend) was not checked or changed. In a real run, the skill creates `docs/constraints.md` from `constraints.template.md` only if it is missing.

## Step 8 – Scaffold CONVENTIONS.md

Simulated only. In a real run, the skill checks `/home/user/trustify-backend/CONVENTIONS.md` and `/home/user/trustify-ui/CONVENTIONS.md` and offers to scaffold any that are missing. Not run here because writing outside `outputs/` is not allowed.

## Step 9 – Bug Configuration

All three fields are filled (10001, docs/bug-template.md, Blocks). Result: **"Bug Configuration is up to date"**.

## Step 10 – Security Configuration (task brief calls this "Step 9")

The section is missing. The user was asked: "Would you like to enable security triage for this project?" The simulated answer was **declined**. Skipped: no Security Configuration section, no security-matrix scaffolding.

## Step 11 – Validate (against the generated output)

- [x] `# Project Configuration` heading exists
- [x] Repository Registry table has columns Repository, Role, Serena Instance, Path (2 rows)
- [x] Jira Configuration has Project key, Cloud ID, Feature issue type ID
- [-] Jira Field Defaults not set up (deferred)
- [x] Code Intelligence documents the `mcp__<instance>__<tool>` convention
- [x] Code Intelligence has a `### Limitations` subheading
- [-] `docs/constraints.md` not checked (outside the eval's scope)
- [x] Bug Configuration has all three fields
- [-] Hierarchy Configuration not set up (deferred)
- [-] Security Configuration not set up (user declined)
