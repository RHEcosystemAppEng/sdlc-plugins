# Changes Log

## Summary

Incremental update to existing Project Configuration. One new Serena instance (serena_ui) was added alongside the already-configured serena_backend instance.

## Repository Registry

| Entry | Status | Details |
|---|---|---|
| trustify-backend | Preserved (existing) | Row unchanged — Rust backend service, serena_backend, /home/user/trustify-backend |
| trustify-ui | Added (new) | New row — TypeScript frontend, serena_ui, /home/user/trustify-ui |

## Jira Configuration

- Status: **Preserved (existing)** — all fields unchanged (Project key: TC, Cloud ID, Feature issue type ID: 10142, custom fields).

## Code Intelligence

- Tool naming convention: **Preserved (existing)** — `mcp__<instance>__<tool>` documentation unchanged.
- Example block: **Preserved (existing)** — serena_backend example unchanged.

### Limitations

| Entry | Status | Details |
|---|---|---|
| serena_backend | Preserved (existing) | "rust-analyzer may take 30-60 seconds to index on first use" — unchanged |
| serena_ui | Added (new) | "No known limitations" |

## Bug Configuration

- Status: **Up to date** — all fields unchanged (Bug issue type ID: 10001, Bug template: docs/bug-template.md, Bug-to-Task link type: Blocks).

## Security Configuration

- Status: **Not added** — user declined when asked.
