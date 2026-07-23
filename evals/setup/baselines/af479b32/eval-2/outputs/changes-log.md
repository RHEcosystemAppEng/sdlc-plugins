# Setup Changes Log

## Summary

Incremental update to an existing Project Configuration. One new Serena instance was discovered and added. All existing configuration was preserved.

## Changes Made

### Repository Registry -- UPDATED

**Added:**
- `trustify-ui | TypeScript frontend | serena_ui | /home/user/trustify-ui`

**Preserved (no changes):**
- `trustify-backend | Rust backend service | serena_backend | /home/user/trustify-backend`

### Code Intelligence -- UPDATED

**Added:**
- `serena_ui` entry under `### Limitations`: "No known limitations"

**Preserved (no changes):**
- Tool naming convention explanation (`mcp__<instance>__<tool>`)
- Example using `serena_backend`
- Existing limitation: `serena_backend`: rust-analyzer may take 30-60 seconds to index on first use

### Jira Configuration -- PRESERVED (no changes)

All fields preserved as-is:
- Project key: TC
- Cloud ID: 2b9e35e3-6bd3-4cec-b838-f4249ee02432
- Feature issue type ID: 10142
- Git Pull Request custom field: customfield_10875
- GitHub Issue custom field: customfield_10747

### Bug Configuration -- PRESERVED (no changes)

All fields preserved as-is:
- Bug issue type ID: 10001
- Bug template: docs/bug-template.md
- Bug-to-Task link type: Blocks

## Sections Not Configured

### Jira Field Defaults -- SKIPPED

Not present in original configuration. Could not be configured because discovery of available priorities and fixVersions requires MCP tool calls or Bash commands, which are prohibited by eval constraints.

### Hierarchy Configuration -- SKIPPED

Not present in original configuration. Could not be configured because discovery of issue type hierarchy requires MCP tool calls or Bash commands, which are prohibited by eval constraints.

### Security Configuration -- SKIPPED

Not present in original configuration. User declined to enable security triage when asked.

### Constraints Document -- SKIPPED

Could not scaffold `docs/constraints.md` to target project because eval constraints prohibit writing files outside of outputs/.

### CONVENTIONS.md -- SKIPPED

Could not scaffold CONVENTIONS.md files to target repositories because eval constraints prohibit writing files outside of outputs/.
