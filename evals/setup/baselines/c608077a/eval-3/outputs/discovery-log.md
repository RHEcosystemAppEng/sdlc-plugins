# Discovery Log — /sdlc-workflow:setup (simulation)

Note: the Skill tool did not list `sdlc-workflow:setup`, so the skill was run by following
`plugins/sdlc-workflow/skills/setup/SKILL.md` directly with `project-config.template.md`.
No MCP tools or Bash commands were run. Tool discovery used `mcp-tools-no-serena.md` only.

## Step 1 – Read Existing Configuration

- Source: `evals/setup/files/claude-md-empty.md`
- `# Project Configuration`: NOT found
- `## Repository Registry`: not found
- `## Jira Configuration`: not found
- `### Jira Field Defaults`: not found
- `## Code Intelligence`: not found
- `## Bug Configuration`: not found
- `## Security Configuration`: not found
- `## Hierarchy Configuration`: not found
- Conclusion: every section has to be created. The new section goes at the end of the file.

## Step 2 – Discover Serena Instances

Tools checked (from `mcp-tools-no-serena.md`):
- Built-in: Bash, Read, Write, Edit, Glob, Grep
- MCP: `mcp__github__create_issue`, `mcp__github__list_pull_requests`, `mcp__github__get_file_contents`

Only the `github` MCP prefix appeared. Its tools are not Serena tools (no `find_symbol`,
`get_symbols_overview`, `search_for_pattern`, `replace_symbol_body`, `get_diagnostics`).

- Serena instances found: **none**
- Prompt to user: "No Serena MCP servers were found. Continue without code intelligence, or set up Serena first?"
- Simulated answer: **continue without code intelligence**
- Action: Repository Registry created with headers only.

## Step 3 – Jira Configuration

- Step 3.1: no tools with the `mcp__atlassian__` prefix. Atlassian MCP is **not available**, so no MCP calls were attempted.
- Step 3.2/3.4: user picked **manual entry** (no REST API fallback).
- Values entered:
  - Project key: MYPROJ
  - Cloud ID: abc123
  - Feature issue type ID: 10001
  - Git Pull Request custom field: none (line left out)
  - GitHub Issue custom field: none (line left out)

## Step 3.5 – Hierarchy Preferences

- Section not present.
- Step 3.5.1: auto-discovery is not possible because there is no Atlassian MCP and the REST fallback was declined.
- The skill says to ask for the hierarchy manually. The eval script gave no hierarchy
  details and confirmed no Epic-level (level-1) issue type.
- Result: by the Step 3.5.2 rule, Epic grouping is unavailable without a confirmed level-1 type.
  "No Epic-level type found in project — Epic grouping is not available. Hierarchy
  Configuration will not be created."
- **Hierarchy Configuration was NOT created.** Re-run setup once the hierarchy is known to add it.

## Step 4 – Jira Field Defaults

- Jira Configuration now exists, so this step runs.
- Step 4.1: `getJiraIssueTypeMetaWithFields` is not available (no Atlassian MCP), and the REST fallback was declined. Priorities and fixVersions could not be discovered.
- Step 4.2: the eval script gave no values, so the skill defaults were used:
  - Default priority: none
  - fixVersion scope: both (default)
  - Prompt for priority: true (default)
  - Prompt for fixVersion: true (default)

## Step 5 – Code Intelligence

- Section not present, so it was generated with the `mcp__<instance>__<tool>` naming convention.
- There is no Serena instance to use in the example, so the generic `<instance>` placeholder is used, with a note that code intelligence is unavailable.
- Limitations: no instances, so "No limitations known".

## Step 6 – Write Configuration

- CLAUDE.md exists but has no `# Project Configuration`, so the section is appended at the end of the file.
- Written to `outputs/claude-md-result.md` (simulation; the real CLAUDE.md was not changed).

## Step 7 – Copy Constraints Template

- Simulation: `docs/constraints.md` would be created from `constraints.template.md` if it is missing. No file was written.

## Step 8 – Scaffold CONVENTIONS.md

- Repository Registry is empty, so there are no repositories to scaffold for. Skipped.

## Step 9 – Bug Configuration

- Section not present.
- Step 9.1: `getJiraProjectIssueTypesMetadata` is not available. Bug issue type ID entered manually: **10001**
- Step 9.2: default template path accepted: **docs/bug-template.md**
- Step 9.3: `getIssueLinkTypes` is not available and the REST fallback was declined. Default link type accepted: **Blocks**
- Step 9.4: copy of the bug template **skipped** (simulation, as instructed)
- Step 9.5: section written.

## Step 10 – Security Configuration

- Section not present.
- Prompt: "Would you like to enable security triage for this project?"
- Simulated answer: **declined**, so the section was not created and Steps 10.1–10.6 were skipped.

## Step 11 – Validate (against outputs/claude-md-result.md)

- [PASS] `# Project Configuration` heading exists
- [PASS] `## Repository Registry` table has columns Repository, Role, Serena Instance, Path (headers only)
- [PASS] `## Jira Configuration` has Project key, Cloud ID, Feature issue type ID
- [PASS] `### Jira Field Defaults` has all four fields with no placeholders
- [PASS] `## Code Intelligence` documents `mcp__<instance>__<tool>`
- [PASS] `## Code Intelligence` has `### Limitations`
- [N/A — simulated] `docs/constraints.md` exists
- [PASS] `## Bug Configuration` has Bug issue type ID, Bug template path, Bug-to-Task link type
- [N/A — simulated] Bug template file at `docs/bug-template.md` (copy skipped)
- [N/A] Hierarchy Configuration not created
- [N/A] Security Configuration not created (declined)
- [PASS] No `{{placeholder}}` markers remain
