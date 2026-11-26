# Discovery Log — /sdlc-workflow:setup (simulated)

Skill source: `plugins/sdlc-workflow/skills/setup/SKILL.md` (the Skill tool did not list `sdlc-workflow:setup`, so the SKILL.md was followed directly). Template: `project-config.template.md`.

## Step 1 – Read Existing Configuration

- Input: `evals/setup/files/claude-md-empty.md`
- `# Project Configuration` heading: NOT found
- Repository Registry: not present
- Jira Configuration / Jira Field Defaults: not present
- Code Intelligence: not present
- Bug Configuration: not present
- Security Configuration: not present
- Hierarchy Configuration: not present
- Conclusion: the whole Project Configuration section must be created and appended to the end of the file.

## Step 2 – Discover Serena Instances

- Tool listing source: `evals/setup/files/mcp-tools-no-serena.md`
- Tools found: Bash, Read, Write, Edit, Glob, Grep, `mcp__github__create_issue`, `mcp__github__list_pull_requests`, `mcp__github__get_file_contents`
- MCP prefixes: `github` only. None of its tools match Serena tool names (`find_symbol`, `get_symbols_overview`, `search_for_pattern`, `replace_symbol_body`, `get_diagnostics`).
- Result: **0 Serena instances found.**
- Prompt to user: "No Serena MCP servers were found. Do you want to continue without code intelligence or set up Serena first?"
- Simulated user answer: **Continue without code intelligence.**
- Action: create a Repository Registry table with headers only.

## Step 3 – Jira Configuration

- Step 3.1: looked for tools prefixed `mcp__atlassian__`. **None found.** Atlassian MCP is not available, so MCP discovery was not attempted.
- Step 3.2: REST API fallback offered (Yes / No - manual / Retry).
- Simulated user answer: **2 – manual entry.** No `jira-client.py` calls were made.
- Step 3.4 manual values:
  - Project key: MYPROJ
  - Cloud ID: abc123
  - Feature issue type ID: 10001
  - Git Pull Request custom field: none (line left out)
  - GitHub Issue custom field: none (line left out)

## Step 3.5 – Hierarchy Preferences

- `getJiraProjectIssueTypesMetadata` cannot run because there is no Atlassian MCP, and the user chose not to use the REST fallback.
- The user gave no hierarchy information, so no Epic-level (level-1) type could be confirmed.
- Result: "No Epic-level type found in project — Epic grouping is not available. Hierarchy Configuration will not be created." The section was left out.

## Step 4 – Jira Field Defaults

- `getJiraIssueTypeMetaWithFields` is not available (no Atlassian MCP), and the user declined the REST fallback, so priorities and fixVersions could not be discovered.
- The user gave no specific values, so the skill defaults were used: Default priority = (none), fixVersion scope = both, Prompt for priority = true, Prompt for fixVersion = true.

## Step 5 – Code Intelligence

- No Serena instances exist. The section was generated with the `mcp__<instance>__<tool>` naming rule, a generic placeholder example, a note that code intelligence is not available, and a `### Limitations` subsection saying no limitations are known.

## Step 6 – Write Configuration

- CLAUDE.md exists with no `# Project Configuration` section, so the section is appended at the end of the file.
- Written to `outputs/claude-md-result.md`. This is a simulation, so the real CLAUDE.md was not changed.

## Step 7 – Copy Constraints Template

- Simulation: would check for `docs/constraints.md` and copy it from `constraints.template.md` if it is missing. **Skipped** (no file changes allowed outside outputs/).

## Step 8 – Scaffold CONVENTIONS.md

- The Repository Registry is empty, so there are no repositories to scaffold CONVENTIONS.md for. Skipped.

## Step 9 – Bug Configuration (the eval prompt calls this "Step 8")

- Step 9.1: no Atlassian MCP and no REST fallback, so the user was asked directly. Simulated answer: **Bug issue type ID = 10001**
- Step 9.2: bug template path. The user accepted the default: **docs/bug-template.md**
- Step 9.3: `getIssueLinkTypes` is not available, so the default was offered. The user accepted: **Blocks**
- Step 9.4: copying the bug template was **skipped** (simulation, as instructed).
- Step 9.5: Bug Configuration section written.

## Step 10 – Security Configuration (the eval prompt calls this "Step 9")

- `## Security Configuration` does not exist.
- Prompt: "Would you like to enable security triage for this project?..."
- Simulated user answer: **Declined.** No Security Configuration section was created, and no security-matrix scaffolding was done.

## Step 11 – Validate (against outputs/claude-md-result.md)

- [x] `# Project Configuration` heading exists
- [x] `## Repository Registry` table has the columns Repository, Role, Serena Instance, Path (headers only)
- [x] `## Jira Configuration` has Project key, Cloud ID, Feature issue type ID
- [x] `### Jira Field Defaults` has valid values
- [x] `## Code Intelligence` documents the `mcp__<instance>__<tool>` naming rule
- [x] `## Code Intelligence` has a `### Limitations` subheading
- [ ] `docs/constraints.md` exists — not created (simulation)
- [x] `## Bug Configuration` has Bug issue type ID, Bug template path, and Bug-to-Task link type
- [ ] Bug template file exists at `docs/bug-template.md` — copy skipped (simulation)
- N/A Hierarchy Configuration (not scaffolded)
- N/A Security Configuration (user declined)

## Tool-use compliance

- No MCP tools called. No Bash commands run. The only files written are in `/tmp/setup-eval-baseline/eval-3/outputs/`.
