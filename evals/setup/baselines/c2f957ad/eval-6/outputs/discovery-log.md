# Discovery Log — /sdlc-workflow:setup (eval-6)

Mode: simulated. The Skill tool reported `sdlc-workflow:setup` as unknown, so
`plugins/sdlc-workflow/skills/setup/SKILL.md` and its templates
(`project-config.template.md`, `security-config.template.md`) were followed directly.
No MCP tools were called, no Bash commands were run, and no project files were modified.

Inputs:
- Existing CLAUDE.md: `evals/setup/files/claude-md-configured-with-security.md`
- MCP tool listing: `evals/setup/files/mcp-tools-with-serena.md`

## Step 1 — Read Existing Configuration

| Section | Status | Details |
|---|---|---|
| `# Project Configuration` | Present | — |
| `## Repository Registry` | Present | `backend` (serena_backend, /home/user/backend), `frontend-ui` (serena_ui, /home/user/frontend-ui) |
| `## Jira Configuration` | Present, required fields all filled | Project key TC, Cloud ID 2b9e35e3-6bd3-4cec-b838-f4249ee02432, Feature issue type ID 10142, Git PR field customfield_10875, GitHub Issue field customfield_10747 |
| `### Jira Field Defaults` | **Missing** | — |
| `## Code Intelligence` | Present | Naming convention, `serena_backend` example, `### Limitations` covering both `serena_backend` and `serena_ui` |
| `## Bug Configuration` | Present, all filled | Bug issue type ID 10001, Bug template docs/bug-template.md, link type Blocks |
| `## Security Configuration` | Present, all filled | Product Lifecycle, Version Streams, Source Repositories all present; no `{{placeholder}}` markers |
| `## Hierarchy Configuration` | **Missing** | — |

## Step 2 — Discover Serena Instances

Looked at the tool listing for `mcp__<instance>__<tool>` names with Serena tool
suffixes (`find_symbol`, `get_symbols_overview`, `search_for_pattern`,
`replace_symbol_body`, `get_diagnostics`, ...).

Found these Serena instances:
- `serena_backend` (10 tools, including `get_diagnostics`)
- `serena_ui` (10 tools, including `get_diagnostics`)

`mcp__atlassian__*` tools were not counted as Serena (wrong tool suffixes).

Both instances are already in the Repository Registry, so `get_diagnostics` was not
needed and no user prompts were needed.

Result: **Repository Registry is up to date.**

## Step 3 — Jira Configuration

All three required fields (Project key, Cloud ID, Feature issue type ID) are filled.
Both optional custom fields are also filled.

Result: **Jira Configuration is up to date.** Skipped to Step 3.5.

## Step 3.5 — Hierarchy Preferences

`## Hierarchy Configuration` does not exist, so discovery is needed.

- Step 3.5.1 (discover issue type hierarchy): an Atlassian MCP exists
  (`mcp__atlassian__*`), but the listing has no `getJiraProjectIssueTypesMetadata`
  tool. The eval also forbids MCP calls. The REST fallback (`scripts/jira-client.py`)
  would need Bash, which is also forbidden. Hierarchy could not be discovered
  automatically.
- Step 3.5.2 (grouping strategy): no user is available to answer. Chose option
  **4. none — ask each time (no default)**. This is the most neutral choice: it does
  not force a grouping strategy on plan-feature, and the user can change it later.
- Assumption: the project has an Epic-level (level-1) issue type. Jira Cloud projects
  normally do. If the user confirms there is no Epic type, this section should be
  dropped, as Step 3.5.2 requires.

Result: **Hierarchy Configuration will be added** with
`Default epic grouping strategy: none`. Needs user confirmation.

## Step 4 — Jira Field Defaults

`### Jira Field Defaults` does not exist under `## Jira Configuration`, and Jira
Configuration is present, so this step runs.

- Step 4.1 (discover priorities and fixVersions): the listing has no
  `getJiraIssueTypeMetaWithFields` tool, MCP calls are forbidden, and the REST
  fallback needs Bash (forbidden). Allowed values could not be discovered.
- Step 4.2 (ask the user): no user is available, so the documented defaults from
  SKILL.md were used:
  - Default priority: `none` (no pre-selection; the allowed priorities are unknown)
  - fixVersion scope: `both` (documented default)
  - Prompt for priority: `true` (documented default)
  - Prompt for fixVersion: `true` (documented default)

Result: **Jira Field Defaults will be added** under `## Jira Configuration`. Needs
user confirmation.

## Step 5 — Code Intelligence

The section exists, documents the `mcp__<instance>__<tool>` convention, has an example
using `serena_backend`, and has a `### Limitations` subsection covering both Registry
instances. Step 2 added no new instances.

Result: **Code Intelligence is up to date.**

## Step 7 — Constraints Template

Checking whether `docs/constraints.md` exists in the target project needs filesystem
access to the (synthetic) target repo, which this eval does not allow. Not run. In a
real run, the file would be created from `constraints.template.md` only if missing.

## Step 8 — Scaffold CONVENTIONS.md

The Registry paths (`/home/user/backend`, `/home/user/frontend-ui`) are synthetic and
cannot be checked. Not run. This step is optional and does not block setup.

## Step 9 — Bug Configuration

All three fields (Bug issue type ID 10001, Bug template docs/bug-template.md, Bug-to-Task
link type Blocks) are filled, with no `{{placeholder}}` markers.

Result: **Bug Configuration is up to date.**

## Step 10 — Security Configuration

`## Security Configuration` exists. Checked it against `security-config.template.md`:

- `### Product Lifecycle`: present. All four required fields are filled:
  - Product pages URL: https://access.example.com/product-lifecycle
  - Jira version prefix: MYPRODUCT
  - Vulnerability issue type ID: 10200
  - Component label pattern: pscomponent:
  - Optional VEX Justification custom field: customfield_12345 (filled)
- `### Version Streams`: present, 1 row (2.1.x), all four columns filled.
- `### Source Repositories`: present, 2 rows (backend, frontend-ui), all filled.
- No `{{placeholder}}` markers anywhere in the section.

Result: **Security Configuration is up to date.** Skipped to Step 11. Steps 10.1–10.6
(collection, scaffolding, security-matrix.md, supportability population) were not run.

Note (informational only, no change made): the current template also lists optional
fields that this section leaves out: Upstream Affected Component custom field, PS
Component custom field, Stream custom field, ProdSec contact email, ProdSec Jira account
ID, Embargo policy URL, and the optional Deployment Context column in Source
Repositories (defaults to `upstream`). All of these are optional, and the skill never
overwrites or re-asks configured sections. The user can add them by hand if needed.

## Step 11 — Validate (against outputs/claude-md-result.md)

| Check | Result |
|---|---|
| `# Project Configuration` heading exists | Pass |
| Repository Registry has columns Repository, Role, Serena Instance, Path | Pass |
| Jira Configuration has Project key, Cloud ID, Feature issue type ID | Pass |
| `### Jira Field Defaults` has valid values (no placeholders) | Pass |
| Code Intelligence documents `mcp__<instance>__<tool>` | Pass |
| Code Intelligence has `### Limitations` | Pass |
| `docs/constraints.md` exists in target project | Not verifiable (no filesystem access to target) |
| Bug Configuration has all three fields | Pass |
| Bug template file exists at configured path | Not verifiable (no filesystem access to target) |
| Hierarchy Configuration has Default epic grouping strategy | Pass |
| Security Configuration `### Product Lifecycle` has all four required fields | Pass |
| Security Configuration `### Version Streams` has at least one row | Pass (1 row) |
| Security Configuration `### Source Repositories` has at least one row | Pass (2 rows) |

## Summary

- Up to date, unchanged: Repository Registry, Jira Configuration (core fields), Code
  Intelligence, Bug Configuration, **Security Configuration**.
- Added: `### Jira Field Defaults`, `## Hierarchy Configuration` (values are defaults,
  pending user confirmation).
