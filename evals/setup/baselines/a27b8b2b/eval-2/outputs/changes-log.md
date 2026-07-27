# Changes Log

## Summary

Incremental update to an existing Project Configuration. One new Serena instance (serena_ui) was discovered and added. All existing configuration was preserved unchanged.

## Changes by Section

### Repository Registry

| Change | Detail |
|---|---|
| PRESERVED | trustify-backend row (Rust backend service, serena_backend, /home/user/trustify-backend) |
| ADDED | trustify-ui row (TypeScript frontend, serena_ui, /home/user/trustify-ui) |

### Jira Configuration

| Change | Detail |
|---|---|
| PRESERVED | Project key: TC |
| PRESERVED | Cloud ID: 2b9e35e3-6bd3-4cec-b838-f4249ee02432 |
| PRESERVED | Feature issue type ID: 10142 |
| PRESERVED | Git Pull Request custom field: customfield_10875 |
| PRESERVED | GitHub Issue custom field: customfield_10747 |

No changes -- all fields were already populated.

### Jira Field Defaults

| Change | Detail |
|---|---|
| SKIPPED | Subsection not present; MCP/REST unavailable for priority and fixVersion discovery |

### Code Intelligence

| Change | Detail |
|---|---|
| PRESERVED | Tool naming convention explanation (`mcp__<instance>__<tool>`) |
| PRESERVED | Example using serena_backend |
| PRESERVED | Limitation: `serena_backend` rust-analyzer indexing delay |
| ADDED | Limitation entry: `serena_ui` -- No known limitations |

### Bug Configuration

| Change | Detail |
|---|---|
| PRESERVED | Bug issue type ID: 10001 |
| PRESERVED | Bug template: docs/bug-template.md |
| PRESERVED | Bug-to-Task link type: Blocks |

No changes -- all fields were already populated.

### Hierarchy Configuration

| Change | Detail |
|---|---|
| SKIPPED | Section not present; MCP/REST unavailable for issue type hierarchy discovery |

### Security Configuration

| Change | Detail |
|---|---|
| SKIPPED | Section not present; user declined to enable security triage |

### Constraints Template (docs/constraints.md)

| Change | Detail |
|---|---|
| SKIPPED | Cannot check target filesystem in simulated run |

### CONVENTIONS.md Scaffolding

| Change | Detail |
|---|---|
| SKIPPED | Cannot check target filesystem in simulated run |
