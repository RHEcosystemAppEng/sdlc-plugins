# Discovery Log — /sdlc-workflow:setup

Mode: simulated. No MCP tools were called; discovery used the tool listing in
`evals/setup/files/mcp-tools-with-serena.md`. Existing configuration read from
`evals/setup/files/claude-md-configured.md`.

Note: the `sdlc-workflow:setup` skill was not registered with the Skill tool, so
`plugins/sdlc-workflow/skills/setup/SKILL.md` and `project-config.template.md` were
followed directly.

## Step 1 – Read Existing Configuration

| Section | Status |
|---|---|
| `# Project Configuration` | Present |
| `## Repository Registry` | Present — 1 entry: `trustify-backend` (serena_backend) |
| `## Jira Configuration` | Present — Project key, Cloud ID, Feature issue type ID, both custom fields populated |
| `### Jira Field Defaults` | **Absent** |
| `## Code Intelligence` | Present — documents `serena_backend`; `### Limitations` has 1 entry |
| `## Bug Configuration` | Present — all 3 fields populated, no placeholders |
| `## Security Configuration` | Absent |
| `## Hierarchy Configuration` | **Absent** |

## Step 2 – Discover Serena Instances

Tools matching `mcp__<instance>__<tool>` with Serena tool names (`find_symbol`,
`get_symbols_overview`, `search_for_pattern`, `replace_symbol_body`, ...):

| Instance | Serena tools found | In Registry? | Action |
|---|---|---|---|
| `serena_backend` | 10 (incl. find_symbol, get_diagnostics) | Yes (trustify-backend) | Preserve, no change |
| `serena_ui` | 10 (incl. find_symbol, get_diagnostics) | **No** | New — gather details |

`mcp__atlassian__*` tools were excluded (not Serena; no Serena tool names).

New instance `serena_ui` — details (simulated user responses; `get_diagnostics` not
called per eval rules):
- Repository short name: `trustify-ui`
- Role: `TypeScript frontend`
- Path: `/home/user/trustify-ui`

## Step 3 – Jira Configuration

All three required fields (Project key `TC`, Cloud ID, Feature issue type ID `10142`)
are populated. **Jira Configuration is up to date.**

## Step 3.5 – Hierarchy Preferences

`## Hierarchy Configuration` does not exist. Discovery requires
`getJiraProjectIssueTypesMetadata`, which is not in the available Atlassian MCP tool
listing, and MCP calls are prohibited in this eval. No grouping-strategy answer was
provided in the scenario. **Deferred** — not scaffolded, to avoid inventing values.
Re-run setup interactively to configure it.

## Step 4 – Jira Field Defaults

`### Jira Field Defaults` does not exist. Discovery requires
`getJiraIssueTypeMetaWithFields` (not available / MCP calls prohibited) and no user
answers were provided. **Deferred** — not scaffolded.

## Step 5 – Code Intelligence

Section exists and covers `serena_backend`. New instance `serena_ui` was added in
Step 2, so the user was asked about limitations: response "no known limitations".
Added `- serena_ui: No known limitations` under `### Limitations`. Existing example
(using `serena_backend`) and existing limitation entry preserved.

## Step 6 – Write Configuration

Changes are limited to Repository Registry (+1 row) and Code Intelligence Limitations
(+1 entry). Written to `outputs/claude-md-result.md` (no real files modified).

## Step 7 – Constraints Template

Not executed against the filesystem (eval restriction). Would check
`docs/constraints.md` in the target project and copy from `constraints.template.md`
only if absent.

## Step 8 – Scaffold CONVENTIONS.md

Not executed against the filesystem (eval restriction). Would check
`/home/user/trustify-backend/CONVENTIONS.md` and `/home/user/trustify-ui/CONVENTIONS.md`
and offer scaffolding only where missing.

## Step 9 – Bug Configuration

All three fields populated (Bug issue type ID `10001`, Bug template
`docs/bug-template.md`, link type `Blocks`). **Bug Configuration is up to date.**

## Step 10 – Security Configuration (Optional)

`## Security Configuration` does not exist. User asked: "Would you like to enable
security triage for this project?" — **User declined.** Section not created; no
security-matrix scaffolding.

## Step 11 – Validate (against generated output)

- [x] `# Project Configuration` heading exists
- [x] Repository Registry table has columns Repository, Role, Serena Instance, Path (2 rows)
- [x] Jira Configuration has Project key, Cloud ID, Feature issue type ID
- [ ] Jira Field Defaults — not configured (deferred)
- [x] Code Intelligence documents `mcp__<instance>__<tool>` convention
- [x] Code Intelligence has `### Limitations` (both instances listed)
- [~] `docs/constraints.md` — not verified (filesystem checks out of scope)
- [x] Bug Configuration has all three fields
- [ ] Hierarchy Configuration — not configured (deferred)
- [x] Security Configuration — not scaffolded (user declined), correctly absent
