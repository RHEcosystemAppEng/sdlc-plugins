# Discovery Log — /sdlc-workflow:setup (simulated)

Inputs:
- Existing CLAUDE.md: `evals/setup/files/claude-md-configured.md`
- MCP tool listing: `evals/setup/files/mcp-tools-with-serena.md`
- No MCP tools were called; discovery came from the tool listing only.

## Step 1: Read the existing configuration

The `# Project Configuration` heading is present. Section-by-section state:

| Section | Status | Details |
|---|---|---|
| Repository Registry | Present | 1 row: trustify-backend / Rust backend service / serena_backend / /home/user/trustify-backend |
| Jira Configuration | Present, all fields filled | Project key TC, Cloud ID 2b9e35e3-..., Feature issue type ID 10142, PR field customfield_10875, GitHub Issue field customfield_10747 |
| Jira Field Defaults | Missing | — |
| Code Intelligence | Present | Covers serena_backend. Has a `### Limitations` entry for serena_backend |
| Bug Configuration | Present, all fields filled | 10001 / docs/bug-template.md / Blocks |
| Security Configuration | Missing | — |
| Hierarchy Configuration | Missing | — |

## Step 2: Discover Serena instances

I scanned the tool listing for the `mcp__<instance>__<tool>` pattern, using Serena tool names such as find_symbol, get_symbols_overview, search_for_pattern and replace_symbol_body.

| Instance | Evidence | Already in Registry? |
|---|---|---|
| serena_backend | 10 tools (find_symbol, get_symbols_overview, get_diagnostics, ...) | Yes. Preserved without changes |
| serena_ui | 10 tools (find_symbol, get_symbols_overview, get_diagnostics, ...) | **No. New instance** |

`mcp__atlassian__*` is the Atlassian MCP, not Serena, so it was not counted as a Serena instance.

For the new instance serena_ui:
- Path: `get_diagnostics` was not called (MCP calls are not allowed). The user gave the path: `/home/user/trustify-ui`
- Repository short name (from user): `trustify-ui`
- Role (from user): `TypeScript frontend`

## Step 3: Jira Configuration

All three required fields are present. **"Jira Configuration is up to date"**. No Jira discovery was run.

## Step 3.5: Hierarchy Preferences

The section is missing. The skill would normally discover the issue type hierarchy through `getJiraProjectIssueTypesMetadata` and then ask for an Epic grouping strategy. That did not happen here:
- MCP calls are not allowed in this eval, and the Atlassian tool listing does not include `getJiraProjectIssueTypesMetadata`.
- The task gave no user answer for the grouping strategy.

Result: **Deferred.** The section was not added. Writing an invented value or a leftover `{{placeholder}}` would break the "never invent values" and "ask only for what is missing" rules. An interactive run would prompt for it.

## Step 4: Jira Field Defaults

The subsection is missing. Discovery needs `getJiraIssueTypeMetaWithFields`, which was not called and is not in the listing. The task gave no user answers for these fields.

Result: **Deferred.** The subsection was not added, for the same reasons as Step 3.5. An interactive run would prompt for Default priority, fixVersion scope, Prompt for priority and Prompt for fixVersion.

## Step 5: Code Intelligence

The section exists but does not cover serena_ui, which was added in Step 2. Following the skill:
- The naming-convention text and the serena_backend example are kept as they are.
- I asked about known limitations for serena_ui. The user reported none, so I added "`serena_ui`: No known limitations" under `### Limitations`.

## Step 6: Write the configuration

Only the changed subsections were updated: Repository Registry and Code Intelligence > Limitations. The result was written to `outputs/claude-md-result.md`. No real files were changed.

## Step 7: Constraints template

I could not check whether the target project has `docs/constraints.md`, because no filesystem access to the target was allowed. Not performed. An interactive run would copy `constraints.template.md` if the file is absent.

## Step 8: Scaffold CONVENTIONS.md

- trustify-backend (/home/user/trustify-backend): not checked, because the path is outside the eval scope.
- trustify-ui (/home/user/trustify-ui): not checked. An interactive run would offer to scaffold this new repo's CONVENTIONS.md from `conventions.template.md`.

Nothing was written.

## Step 9: Bug Configuration

All three fields are present with no placeholders. **"Bug Configuration is up to date"**.

## Step 10: Security Configuration (the task calls this "Step 9")

The section is missing. I asked the user: "Would you like to enable security triage for this project?" **The user declined.** The section was not created, and Steps 10.1 to 10.6 were skipped.

## Step 11: Validation (on the generated output)

- [x] `# Project Configuration` heading exists
- [x] Repository Registry table has the columns Repository, Role, Serena Instance, Path (2 rows)
- [x] Jira Configuration has Project key, Cloud ID, Feature issue type ID
- [x] Code Intelligence documents `mcp__<instance>__<tool>`
- [x] Code Intelligence has `### Limitations`, with entries for both instances
- [x] Bug Configuration has all three fields
- [ ] `docs/constraints.md`: not verifiable in this eval
- Jira Field Defaults, Hierarchy Configuration, Security Configuration: not configured (deferred or declined)
