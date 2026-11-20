# Setup Discovery Log

Source CLAUDE.md: `evals/setup/files/claude-md-configured.md`
Simulated MCP tool listing: `evals/setup/files/mcp-tools-with-serena.md`
No MCP tools, Bash commands, or external services were called. Everything below is simulated from the input files.

## Step 1 – Read Existing Configuration

| Section | Status | Details |
|---|---|---|
| `# Project Configuration` | Present | |
| `## Repository Registry` | Present | 1 row: `trustify-backend` (serena_backend, /home/user/trustify-backend) |
| `## Jira Configuration` | Present, required fields filled in | Project key TC, Cloud ID 2b9e35e3-..., Feature issue type ID 10142, plus both optional custom fields |
| `### Jira Field Defaults` | Missing | Not in the existing file |
| `## Code Intelligence` | Present | Documents `serena_backend`; Limitations lists one entry for `serena_backend` |
| `## Bug Configuration` | Present, filled in | 10001 / docs/bug-template.md / Blocks |
| `## Security Configuration` | Missing | |
| `## Hierarchy Configuration` | Missing | |

## Step 2 – Discover Serena Instances

Tool names matching `mcp__<instance>__<tool>` with Serena tool names (`find_symbol`, `get_symbols_overview`, `search_for_pattern`, `replace_symbol_body`, `get_diagnostics`, ...):

| Instance | Serena tools found | Already in Registry? | Action |
|---|---|---|---|
| `serena_backend` | 10 | Yes (trustify-backend) | Keep as is |
| `serena_ui` | 10 | **No** | **New: add to Registry** |

Non-Serena MCP server: `atlassian` (`mcp__atlassian__*`). Not counted as a Serena instance.

New instance `serena_ui`: answers from the simulated user (`get_diagnostics` was not called):
- Repository short name: `trustify-ui`
- Role: `TypeScript frontend`
- Path: `/home/user/trustify-ui`

## Step 3 – Jira Configuration

All three required fields are present. Result: "Jira Configuration is up to date". No Atlassian MCP calls were made.

## Step 3.5 – Hierarchy Preferences

The section is missing. The skill would discover the hierarchy with `getJiraProjectIssueTypesMetadata`, but this eval does not allow MCP calls and gives no user answer for the grouping strategy. **Skipped: no value was made up.** The user should run setup again in a live session to fill this in.

## Step 4 – Jira Field Defaults

The subsection is missing. The skill would discover priorities and fixVersions with `getJiraIssueTypeMetaWithFields` and then ask the user. MCP calls are not allowed here and no user answers were given. **Skipped: no value was made up.** Pending a live run.

## Step 5 – Code Intelligence

The section exists. `serena_ui` was added in Step 2, so the user was asked about known limitations. Simulated answer: none. Result: the limitation entry "`serena_ui`: No known limitations" was added. The naming convention text and the `serena_backend` example were kept as they were.

## Step 6 – Write Configuration

Changes: one Registry row and one Limitations bullet were added. Everything else was kept unchanged. The result was written to `outputs/claude-md-result.md` and the real CLAUDE.md was not changed.

## Step 7 – Constraints Template

Not run, because this eval does not allow file changes outside outputs/. In a live run, setup would check whether `docs/constraints.md` exists in the target project.

## Step 8 – Scaffold CONVENTIONS.md

Not run, because no file changes are allowed. In a live run, setup would check `/home/user/trustify-backend/CONVENTIONS.md` and `/home/user/trustify-ui/CONVENTIONS.md`.

## Step 9 – Bug Configuration

All three fields are present with no placeholders. Result: "Bug Configuration is up to date".

## Step 10 – Security Configuration (task's "Step 9")

The section is missing, so the user was asked: "Would you like to enable security triage for this project?" Simulated answer: **declined**. Security Configuration was not created, and no security-matrix.md was scaffolded.

## Step 11 – Validate (against outputs/claude-md-result.md)

- [x] `# Project Configuration` heading exists
- [x] Repository Registry table has the columns Repository, Role, Serena Instance, Path (2 rows)
- [x] Jira Configuration has Project key, Cloud ID, Feature issue type ID
- [x] Code Intelligence documents the `mcp__<instance>__<tool>` convention
- [x] Code Intelligence has a `### Limitations` subheading (covers both instances)
- [x] Bug Configuration has all three fields
- [n/a] Jira Field Defaults: not configured (pending a live run)
- [n/a] Hierarchy Configuration: not configured (pending a live run)
- [n/a] Security Configuration: declined
- [n/a] docs/constraints.md: not checked in this simulation
