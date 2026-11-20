# Discovery Log — /sdlc-workflow:setup

Inputs:
- Existing CLAUDE.md: `evals/setup/files/claude-md-configured-with-security.md`
- MCP tool listing: `evals/setup/files/mcp-tools-with-serena.md`

No real MCP tools were called. Serena discovery was simulated from the tool listing.

## Step 1 – Read Existing Configuration

`# Project Configuration` heading: present.

| Section | Status | Details |
|---|---|---|
| Repository Registry | Present | 2 entries: `backend` (serena_backend), `frontend-ui` (serena_ui) |
| Jira Configuration | Present, fully populated | Project key TC, Cloud ID 2b9e35e3-..., Feature issue type ID 10142, Git PR field customfield_10875, GitHub Issue field customfield_10747 |
| Jira Field Defaults | Absent | No `### Jira Field Defaults` subsection |
| Code Intelligence | Present | Naming convention, `serena_backend` example, `### Limitations` covering both instances |
| Bug Configuration | Present, fully populated | Bug issue type ID 10001, template docs/bug-template.md, link type Blocks; no `{{placeholder}}` markers |
| Security Configuration | Present, fully populated | Product Lifecycle (4 required fields + VEX Justification), Version Streams (1 row: 2.1.x), Source Repositories (2 rows); no `{{placeholder}}` markers |
| Hierarchy Configuration | Absent | No `## Hierarchy Configuration` section |

## Step 2 – Discover Serena Instances

Tools matching `mcp__<instance>__<tool>` with Serena tool names (`find_symbol`, `get_symbols_overview`, `search_for_pattern`, `replace_symbol_body`, ...):

- `serena_backend` — already in Repository Registry (`backend`)
- `serena_ui` — already in Repository Registry (`frontend-ui`)

Non-Serena tools ignored: built-ins (Bash, Read, Write, Edit, Glob, Grep) and `mcp__atlassian__*`.

Result: **Repository Registry is up to date.** No user prompts for name/role/path.

## Step 3 – Jira Configuration

All three required fields (Project key, Cloud ID, Feature issue type ID) are populated, and so are both optional custom fields.
Result: **Jira Configuration is up to date.** No Atlassian MCP calls were needed.

## Step 3.5 – Hierarchy Preferences

`## Hierarchy Configuration` does not exist. Under the skill, this would start discovery (`getJiraProjectIssueTypesMetadata`, then the Epic grouping strategy prompt). In this simulation I could not call MCP tools or get user input, so I did not discover or invent a value.
Result: **Not scaffolded. Needs user input** (see changes log).

Note: the Atlassian MCP listing has `jira_get_issue`, `jira_search_issues`, `jira_edit_issue`, `jira_transition_issue`, `jira_add_comment`, `jira_user_info`. It does not include `getJiraProjectIssueTypesMetadata` or `getJiraIssueTypeMetaWithFields`, so in a live run discovery would fall back to REST or manual entry.

## Step 4 – Jira Field Defaults

`### Jira Field Defaults` does not exist. Under the skill, this would start discovery of priorities and fixVersions and then four user prompts. In this simulation I asked no questions and invented no values.
Result: **Not scaffolded. Needs user input** (see changes log).

## Step 5 – Code Intelligence

The section exists, documents the `mcp__<instance>__<tool>` convention, has a concrete example (`serena_backend`), and its `### Limitations` covers every instance in the Registry (serena_backend, serena_ui). No new instances were added in Step 2.
Result: **Code Intelligence is up to date.**

## Step 7 – Constraints Template

This simulation did not check or write the target project's `docs/constraints.md`, because the only allowed writes are to outputs/. In a live run: create it from `constraints.template.md` if absent, otherwise skip.

## Step 8 – CONVENTIONS.md

The simulation did not inspect `/home/user/backend` or `/home/user/frontend-ui`. In a live run, check each Registry path for `CONVENTIONS.md`, and offer to scaffold one only if it is missing or still contains placeholders.

## Step 9 – Bug Configuration

The section exists, all three required fields are populated, and there are no `{{placeholder}}` markers.
Result: **Bug Configuration is up to date.** No discovery ran and the Bug Configuration prompts were not shown.

## Step 10 – Security Configuration

`## Security Configuration` exists and has no `{{placeholder}}` markers:
- `### Product Lifecycle`: Product pages URL, Jira version prefix, Vulnerability issue type ID and Component label pattern are all populated (the 4 required fields). VEX Justification custom field is also set (customfield_12345).
- `### Version Streams`: 1 row (2.1.x).
- `### Source Repositories`: 2 rows (backend, frontend-ui).

The optional fields (Upstream Affected Component, PS Component, Stream, ProdSec email, ProdSec Jira account ID, Embargo policy URL) and the optional Deployment Context column are left out. These are optional, and leaving them out is not the same as having unfilled placeholders. Deployment Context defaults to `upstream`.

Result: **Security Configuration is up to date.** The opt-in prompt ("Would you like to enable security triage...") was **not** shown. Steps 10.1–10.4 were skipped (idempotency skip). The optional matrix steps (10.5/10.6) were not part of this task, and no security-matrix files were touched.

## Step 11 – Validate (against the result in outputs/claude-md-result.md)

- [x] `# Project Configuration` heading exists
- [x] Repository Registry table has the columns Repository, Role, Serena Instance, Path
- [x] Jira Configuration has Project key, Cloud ID, Feature issue type ID
- [ ] Jira Field Defaults: not configured (optional per validation, "If configured")
- [x] Code Intelligence documents `mcp__<instance>__<tool>`
- [x] Code Intelligence has `### Limitations`
- [ ] `docs/constraints.md`: not checked (simulation)
- [x] Bug Configuration has all three fields
- [ ] Hierarchy Configuration: not configured (optional per validation, "If scaffolded")
- [x] Security Configuration: Product Lifecycle has all four required fields
- [x] Security Configuration: Version Streams has at least one row
- [x] Security Configuration: Source Repositories has at least one row
