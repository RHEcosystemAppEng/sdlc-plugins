# Discovery Log — /sdlc-workflow:setup (simulated)

## Step 1 – Read Existing Configuration

Source: `evals/setup/files/claude-md-empty.md`

- `# Project Configuration` heading: NOT found
- `## Repository Registry`: not present
- `## Jira Configuration`: not present
- `### Jira Field Defaults`: not present
- `## Code Intelligence`: not present
- `## Bug Configuration`: not present
- `## Security Configuration`: not present
- `## Hierarchy Configuration`: not present

Conclusion: greenfield project; the entire Project Configuration section must be created and appended to the end of the file.

## Step 2 – Discover Serena Instances

Source: `evals/setup/files/mcp-tools-no-serena.md` (simulated tool listing; no MCP tools were called)

Tools listed:
- Built-in: Bash, Read, Write, Edit, Glob, Grep
- `mcp__github__create_issue`, `mcp__github__list_pull_requests`, `mcp__github__get_file_contents`

Analysis: the only `mcp__<instance>__<tool>` prefix is `github`. Its tools (`create_issue`, `list_pull_requests`, `get_file_contents`) are GitHub tools, not Serena tools (`find_symbol`, `get_symbols_overview`, `search_for_pattern`, `replace_symbol_body`).

Result: **no Serena instances found.**

Prompt to user: "No Serena MCP servers were found. Continue without code intelligence, or set up Serena first?"
User response (simulated): **Continue without code intelligence.**
Action: create an empty Repository Registry table (headers only).

## Step 3 – Jira Configuration

### Step 3.1 – Attempt MCP
- Searched for tools prefixed `mcp__atlassian__`: **none found.** Atlassian MCP is not available, so no MCP discovery calls could be attempted.

### Step 3.2 – Fallback prompt
Prompt offered: (1) REST API fallback, (2) manual entry, (3) retry.
User response (simulated): **2 – manual entry.**

### Step 3.4 – Manual Entry
- Project key: `MYPROJ`
- Cloud ID: `abc123`
- Feature issue type ID: `10001`
- Git Pull Request custom field: none provided (line left out)
- GitHub Issue custom field: none provided (line left out)

## Step 3.5 – Hierarchy Preferences

- `## Hierarchy Configuration` doesn't exist yet.
- Step 3.5.1: Atlassian MCP isn't available, and the user chose manual entry over the REST fallback, so the issue type hierarchy couldn't be discovered automatically.
- The user supplied no hierarchy details (no Epic or level-1 type information and no grouping strategy). Without a confirmed Epic-level type, the grouping strategy question doesn't apply.
- Note: "No Epic-level type found in project — Epic grouping is not available. Hierarchy Configuration will not be created."
- Result: **Hierarchy Configuration not created.** Re-run setup after Jira hierarchy information is available to add it.

## Step 4 – Jira Field Defaults

- `## Jira Configuration` is now present (from Step 3), so this step applies.
- Step 4.1: `getJiraIssueTypeMetaWithFields` can't be used because there is no Atlassian MCP. The REST fallback was declined, so no priority or fixVersion values were discovered.
- Step 4.2: the user wasn't given a list of priorities, so the documented defaults were applied:
  - Default priority: `none`
  - fixVersion scope: `both` (default)
  - Prompt for priority: `true` (default)
  - Prompt for fixVersion: `true` (default)

## Step 5 – Code Intelligence

- No Serena instances exist, so the section was generated with:
  - the standard `mcp__<instance>__<tool>` naming convention plus a generic `<instance>` example
  - a note that no Serena MCP servers are configured
  - a `### Limitations` subsection stating that no limitations are known

## Step 6 – Write Configuration

- The CLAUDE.md exists but has no `# Project Configuration`, so the section was **appended at the end of the file**.
- Output written to `outputs/claude-md-result.md` (simulation; the real CLAUDE.md was not modified).

## Step 7 – Constraints Template

- In a real run: check `docs/constraints.md` and, if missing, copy `constraints.template.md` there.
- Simulation: **skipped.** No files were written outside outputs/.

## Step 8 – Scaffold CONVENTIONS.md

- The Repository Registry is empty, so there are no repositories to scaffold. **Skipped.**

## Step 9 – Bug Configuration

- `## Bug Configuration` doesn't exist yet.
- Step 9.1: no MCP, and the REST fallback was declined. The user entered the Bug issue type ID manually: `10001`.
- Step 9.2: the user accepted the default template path `docs/bug-template.md`.
- Step 9.3: link types couldn't be listed (`getIssueLinkTypes` isn't available). The user accepted the default: `Blocks`.
- Step 9.4: bug template copy **skipped (simulation)**.
- Step 9.5: Bug Configuration section written.

## Step 10 – Security Configuration

- `## Security Configuration` doesn't exist yet.
- Prompt: "Would you like to enable security triage for this project?"
- User response (simulated): **Declined.** The Security Configuration section was not created, and security-matrix scaffolding was skipped.

## Step 11 – Validate (against outputs/claude-md-result.md)

| Check | Result |
|---|---|
| `# Project Configuration` heading exists | PASS |
| Repository Registry table with columns Repository, Role, Serena Instance, Path | PASS (headers only) |
| Jira Configuration has Project key, Cloud ID, Feature issue type ID | PASS |
| Jira Field Defaults has valid values | PASS |
| Code Intelligence documents `mcp__<instance>__<tool>` | PASS |
| Code Intelligence has `### Limitations` | PASS |
| `docs/constraints.md` exists | N/A (simulation; copy skipped) |
| Bug Configuration has Bug issue type ID, template path, link type | PASS |
| Bug template file exists at configured path | N/A (simulation; copy skipped) |
| Hierarchy Configuration | Not scaffolded |
| Security Configuration | Not scaffolded (user declined) |
