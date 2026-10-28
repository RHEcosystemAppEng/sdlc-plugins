# Changes Log

## Summary

This log identifies which configuration entries were preserved (existing) and which were added (new) during the setup run.

## Repository Registry

| Entry | Status | Details |
|---|---|---|
| trustify-backend | PRESERVED | Existing entry unchanged (Rust backend service, serena_backend, /home/user/trustify-backend) |
| trustify-ui | ADDED | New entry for newly discovered serena_ui instance (TypeScript frontend, serena_ui, /home/user/trustify-ui) |

## Jira Configuration

| Field | Status | Value |
|---|---|---|
| Project key | PRESERVED | TC |
| Cloud ID | PRESERVED | 2b9e35e3-6bd3-4cec-b838-f4249ee02432 |
| Feature issue type ID | PRESERVED | 10142 |
| Git Pull Request custom field | PRESERVED | customfield_10875 |
| GitHub Issue custom field | PRESERVED | customfield_10747 |

## Code Intelligence

| Item | Status | Details |
|---|---|---|
| Tool naming convention | PRESERVED | mcp__<instance>__<tool> pattern with serena_backend example |
| serena_backend limitation | PRESERVED | rust-analyzer may take 30-60 seconds to index on first use |
| serena_ui limitation | ADDED | No known limitations |

## Bug Configuration

| Field | Status | Value |
|---|---|---|
| Bug issue type ID | PRESERVED | 10001 |
| Bug template | PRESERVED | docs/bug-template.md |
| Bug-to-Task link type | PRESERVED | Blocks |

## Security Configuration

Not added -- user declined when asked whether to enable security triage. Section did not exist previously.
