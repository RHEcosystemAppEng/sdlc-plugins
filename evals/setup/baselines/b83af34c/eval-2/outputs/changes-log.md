# Changes Log

## What was added

### Repository Registry
- **Added** row for `trustify-ui` (TypeScript frontend, serena_ui, /home/user/trustify-ui)

### Code Intelligence -- Limitations
- **Added** entry for `serena_ui`: No known limitations

## What was preserved (unchanged)

### Repository Registry
- **Preserved** existing row for `trustify-backend` (Rust backend service, serena_backend, /home/user/trustify-backend)

### Jira Configuration
- **Preserved** all existing fields:
  - Project key: TC
  - Cloud ID: 2b9e35e3-6bd3-4cec-b838-f4249ee02432
  - Feature issue type ID: 10142
  - Git Pull Request custom field: customfield_10875
  - GitHub Issue custom field: customfield_10747

### Code Intelligence
- **Preserved** existing tool naming convention explanation and example
- **Preserved** existing limitation for `serena_backend` (rust-analyzer indexing delay)

### Bug Configuration
- **Preserved** all existing fields:
  - Bug issue type ID: 10001
  - Bug template: docs/bug-template.md
  - Bug-to-Task link type: Blocks

## What was skipped

| Section | Reason |
|---|---|
| Jira Field Defaults | Requires MCP calls to discover available priorities and fixVersions (not available in eval mode) |
| Hierarchy Configuration | Requires MCP calls to discover issue type hierarchy (not available in eval mode) |
| Security Configuration | User declined when asked whether to enable security triage |
| Constraints template (Step 7) | Eval mode -- no actual file modifications outside outputs/ |
| CONVENTIONS.md scaffold (Step 8) | Eval mode -- no actual file modifications outside outputs/ |
