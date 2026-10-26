# Changes Log

## Summary

Incremental update to Project Configuration. One new Serena instance discovered and added; existing configuration preserved without modification.

## Changes Made

### Repository Registry — MODIFIED

**Added:**
- Row: `trustify-ui | TypeScript frontend | serena_ui | /home/user/trustify-ui`

**Preserved (unchanged):**
- Row: `trustify-backend | Rust backend service | serena_backend | /home/user/trustify-backend`

### Code Intelligence — MODIFIED

**Added:**
- `### Limitations` entry: `serena_ui`: No known limitations

**Preserved (unchanged):**
- Tool naming convention explanation (`mcp__<instance>__<tool>`)
- Code example using `serena_backend`
- Existing limitation: `serena_backend`: rust-analyzer may take 30-60 seconds to index on first use

## Sections Preserved (No Changes)

### Jira Configuration — PRESERVED
All fields retained as-is:
- Project key: TC
- Cloud ID: 2b9e35e3-6bd3-4cec-b838-f4249ee02432
- Feature issue type ID: 10142
- Git Pull Request custom field: customfield_10875
- GitHub Issue custom field: customfield_10747

### Bug Configuration — PRESERVED
All fields retained as-is:
- Bug issue type ID: 10001
- Bug template: docs/bug-template.md
- Bug-to-Task link type: Blocks

## Sections Not Created

### Jira Field Defaults — SKIPPED
Reason: Requires Atlassian MCP tool calls to discover available priorities and fixVersions. Not available in this simulation.

### Hierarchy Configuration — SKIPPED
Reason: Requires Atlassian MCP tool calls to discover issue type hierarchy. Not available in this simulation.

### Security Configuration — SKIPPED
Reason: User declined to enable security triage.

## Non-CLAUDE.md File Operations

### docs/constraints.md — SKIPPED
Reason: Simulation mode; not modifying actual project files.

### CONVENTIONS.md — SKIPPED
Reason: Simulation mode; not modifying actual project files.
