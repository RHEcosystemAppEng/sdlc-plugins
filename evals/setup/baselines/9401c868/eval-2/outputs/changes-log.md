# Changes Log

## Summary

Incremental update to an existing Project Configuration. One new Serena instance (serena_ui) was discovered and added to the configuration. All existing entries were preserved unchanged.

## Changes Made

### Repository Registry

- **ADDED**: `trustify-ui | TypeScript frontend | serena_ui | /home/user/trustify-ui`
- **PRESERVED**: `trustify-backend | Rust backend service | serena_backend | /home/user/trustify-backend`

### Code Intelligence — Limitations

- **ADDED**: `serena_ui`: No known limitations
- **PRESERVED**: `serena_backend`: rust-analyzer may take 30-60 seconds to index on first use

## Sections Preserved (No Changes)

### Jira Configuration

All fields preserved as-is:
- Project key: TC
- Cloud ID: 2b9e35e3-6bd3-4cec-b838-f4249ee02432
- Feature issue type ID: 10142
- Git Pull Request custom field: customfield_10875
- GitHub Issue custom field: customfield_10747

### Code Intelligence (Main Body)

Tool naming convention explanation and example preserved unchanged.

### Bug Configuration

All fields preserved as-is:
- Bug issue type ID: 10001
- Bug template: docs/bug-template.md
- Bug-to-Task link type: Blocks

## Sections Not Configured

### Jira Field Defaults

Not configured — auto-discovery of available priorities and fixVersions requires MCP or REST API access, which was not available in this simulation.

### Hierarchy Configuration

Not configured — auto-discovery of Jira issue type hierarchy requires MCP or REST API access, which was not available in this simulation.

### Security Configuration

Not configured — user declined to enable security triage.

## Non-CLAUDE.md Artifacts

### docs/constraints.md

Simulated — in a live run, would be created from `constraints.template.md` if not already present.

### CONVENTIONS.md

Simulated — in a live run, would be offered for scaffolding at each repository root:
- /home/user/trustify-backend
- /home/user/trustify-ui
