# Changes Log

Summary of what was added versus preserved in the Project Configuration.

## Repository Registry

| Entry | Status | Details |
|---|---|---|
| trustify-backend | PRESERVED | Existing entry kept unchanged (Rust backend service, serena_backend, /home/user/trustify-backend) |
| trustify-ui | ADDED | New entry from discovered Serena instance `serena_ui` (TypeScript frontend, serena_ui, /home/user/trustify-ui) |

## Jira Configuration

| Field | Status | Value |
|---|---|---|
| Project key | PRESERVED | TC |
| Cloud ID | PRESERVED | 2b9e35e3-6bd3-4cec-b838-f4249ee02432 |
| Feature issue type ID | PRESERVED | 10142 |
| Git Pull Request custom field | PRESERVED | customfield_10875 |
| GitHub Issue custom field | PRESERVED | customfield_10747 |

### Jira Field Defaults

| Status | Details |
|---|---|
| NOT SCAFFOLDED | Required MCP tools (getJiraIssueTypeMetaWithFields) not available in tool listing |

## Code Intelligence

| Element | Status | Details |
|---|---|---|
| Section heading and description | PRESERVED | Existing text kept unchanged |
| Tool naming convention | PRESERVED | `mcp__<instance>__<tool>` explanation kept |
| Example (serena_backend) | PRESERVED | find_symbol example kept unchanged |
| Limitation: serena_backend | PRESERVED | "rust-analyzer may take 30-60 seconds to index on first use" |
| Limitation: serena_ui | ADDED | "No known limitations" (user confirmed) |

## Bug Configuration

| Field | Status | Value |
|---|---|---|
| Bug issue type ID | PRESERVED | 10001 |
| Bug template | PRESERVED | docs/bug-template.md |
| Bug-to-Task link type | PRESERVED | Blocks |

## Hierarchy Configuration

| Status | Details |
|---|---|
| NOT SCAFFOLDED | Required MCP tools (getJiraProjectIssueTypesMetadata) not available in tool listing for hierarchy discovery |

## Security Configuration

| Status | Details |
|---|---|
| NOT SCAFFOLDED | User declined when asked whether to enable security triage |

## Constraints Template (docs/constraints.md)

| Status | Details |
|---|---|
| SKIPPED | Cannot access target project filesystem in eval simulation mode |

## CONVENTIONS.md Scaffolding

| Repository | Status | Details |
|---|---|---|
| trustify-backend | SKIPPED | Cannot access /home/user/trustify-backend in eval simulation mode |
| trustify-ui | SKIPPED | Cannot access /home/user/trustify-ui in eval simulation mode |
