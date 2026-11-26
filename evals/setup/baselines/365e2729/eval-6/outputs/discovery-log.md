# Discovery Log — /sdlc-workflow:setup (simulated)

Inputs:
- Existing CLAUDE.md: `evals/setup/files/claude-md-configured-with-security.md`
- MCP tool listing: `evals/setup/files/mcp-tools-with-serena.md`

No MCP tools were called. No Bash commands were run. Discovery was simulated from the tool listing.

## Step 1 – Read Existing Configuration

`# Project Configuration` heading found. Parsed sections:

| Section | Present | State |
|---|---|---|
| Repository Registry | Yes | 2 entries: `backend` (serena_backend), `frontend-ui` (serena_ui) |
| Jira Configuration | Yes | Project key, Cloud ID, Feature issue type ID, Git PR custom field, GitHub Issue custom field all populated |
| Jira Field Defaults (subsection) | No | Not present |
| Code Intelligence | Yes | Naming convention, example (`serena_backend`), and `### Limitations` covering both instances |
| Bug Configuration | Yes | Bug issue type ID (10001), Bug template (docs/bug-template.md), Bug-to-Task link type (Blocks). No `{{placeholder}}` markers |
| Security Configuration | Yes | Product Lifecycle, Version Streams, Source Repositories all present. No `{{placeholder}}` markers |
| Hierarchy Configuration | No | Not present |

## Step 2 – Discover Serena Instances

Tools that match `mcp__<instance>__<tool>` with Serena tool names (`find_symbol`, `get_symbols_overview`, `search_for_pattern`, `replace_symbol_body`, ...):

- `serena_backend` — already in Repository Registry (`backend`)
- `serena_ui` — already in Repository Registry (`frontend-ui`)

`mcp__atlassian__*` tools are not Serena tools and were excluded.

Result: **Repository Registry is up to date.** No new instances, so no prompts for name/role/path.

## Step 3 – Jira Configuration

All three required fields (Project key: TC, Cloud ID, Feature issue type ID: 10142) are populated, and so are both optional custom fields.

Result: **Jira Configuration is up to date.** No Atlassian MCP or REST API discovery was needed.

## Step 3.5 – Hierarchy Preferences

`## Hierarchy Configuration` is absent. Filling it in requires issue-type hierarchy discovery (`getJiraProjectIssueTypesMetadata`) and asking the user which Epic grouping strategy to use. This simulation cannot call MCP and has no user to answer, and the Atlassian tools in the listing do not include `getJiraProjectIssueTypesMetadata`. So no section was scaffolded and no value was made up.

Result: **Not configured. Needs interactive input** (an optional section, not required by the Step 11 checks).

## Step 4 – Jira Field Defaults

`### Jira Field Defaults` is absent. Filling it in requires `getJiraIssueTypeMetaWithFields` (not in the listing) plus user choices for priority, fixVersion scope, and the two prompt flags. No defaults were assumed.

Result: **Not configured. Needs interactive input** (optional subsection).

## Step 5 – Code Intelligence

The section exists, documents the `mcp__<instance>__<tool>` convention, and has a `### Limitations` subheading with an entry for each registered Serena instance (`serena_backend`, `serena_ui`). No new instances were added in Step 2.

Result: **Code Intelligence is up to date.**

## Step 6 – Write Configuration

No changes were made to any existing section. See changes-log.md.

## Step 7 – Constraints Template

Not run in this simulation, because writes are limited to `outputs/`. For the target project, the skill would check for `docs/constraints.md` and copy it from the template only if it is missing.

## Step 8 – CONVENTIONS.md

Not run in this simulation, because writes are limited to `outputs/` and the repository paths (`/home/user/backend`, `/home/user/frontend-ui`) cannot be checked. It is optional and does not block setup.

## Step 9 – Bug Configuration

`## Bug Configuration` exists with all three required fields populated and no `{{placeholder}}` markers.

Result: **Bug Configuration is up to date.** Discovery and scaffolding were skipped. The bug template was not copied.

## Step 10 – Security Configuration

`## Security Configuration` exists and is fully populated, with no `{{placeholder}}` markers:
- Product Lifecycle: Product pages URL, Jira version prefix, Vulnerability issue type ID, and Component label pattern (all four required) are populated. VEX Justification custom field (optional) is also populated.
- Version Streams: 1 row (`2.1.x`).
- Source Repositories: 2 rows (`backend`, `frontend-ui`).

Result: **Security Configuration is up to date.** The opt-in prompt ("Would you like to enable security triage for this project?") was **not** shown, because the section already exists and is fully populated (idempotency skip). Steps 10.1–10.6 were skipped.

Informational notes (no action taken, existing values kept):
- Optional Product Lifecycle fields are absent: Upstream Affected Component, PS Component, Stream custom fields, ProdSec contact email, ProdSec Jira account ID, and Embargo policy URL. They are optional and do not trigger re-scaffolding.
- The Source Repositories table has no `Deployment Context` column. That column is optional, and repositories without it default to `upstream`.

## Step 11 – Validate (against the preserved configuration)

- [x] `# Project Configuration` heading exists
- [x] Repository Registry has the columns Repository, Role, Serena Instance, Path
- [x] Jira Configuration has Project key, Cloud ID, Feature issue type ID
- [x] Code Intelligence documents `mcp__<instance>__<tool>`
- [x] Code Intelligence has a `### Limitations` subheading
- [x] Bug Configuration has Bug issue type ID, Bug template path, Bug-to-Task link type
- [x] Security Configuration has `### Product Lifecycle` with all four required fields
- [x] Security Configuration has `### Version Streams` with at least one row
- [x] Security Configuration has `### Source Repositories` with at least one row
- [ ] `docs/constraints.md` existence in the target project was not checked (simulation)
- n/a Jira Field Defaults / Hierarchy Configuration were not configured

## Summary

Project Configuration is up to date. No changes are needed to the existing sections. The optional Jira Field Defaults and Hierarchy Configuration sections are absent and can be added later by running setup interactively.
