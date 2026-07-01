# Changes Log

## Summary

Incremental update to an existing Project Configuration. One new Serena instance (`serena_ui`) was discovered and added. All existing configuration was preserved.

---

## Preserved (no changes)

### Repository Registry
- **Preserved row**: `trustify-backend` | Rust backend service | `serena_backend` | `/home/user/trustify-backend`

### Jira Configuration
- **Preserved**: Project key: TC
- **Preserved**: Cloud ID: 2b9e35e3-6bd3-4cec-b838-f4249ee02432
- **Preserved**: Feature issue type ID: 10142
- **Preserved**: Git Pull Request custom field: customfield_10875
- **Preserved**: GitHub Issue custom field: customfield_10747

### Code Intelligence
- **Preserved**: Tool naming convention explanation
- **Preserved**: `serena_backend` example
- **Preserved**: `serena_backend` limitation (rust-analyzer indexing delay)

### Bug Configuration
- **Preserved**: Bug issue type ID: 10001
- **Preserved**: Bug template: docs/bug-template.md
- **Preserved**: Bug-to-Task link type: Blocks

---

## Added

### Repository Registry
- **Added row**: `trustify-ui` | TypeScript frontend | `serena_ui` | `/home/user/trustify-ui`

### Code Intelligence — Limitations
- **Added**: `serena_ui` — No known limitations

---

## Not configured (skipped)

### Jira Field Defaults
- **Reason**: Requires MCP or REST API access to discover available priorities and fixVersions. Not available in simulation mode.

### Hierarchy Configuration
- **Reason**: Requires MCP or REST API access to discover issue type hierarchy. Not available in simulation mode.

### Security Configuration
- **Reason**: User declined when asked whether to enable security triage.
