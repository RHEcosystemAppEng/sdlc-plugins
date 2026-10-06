# Changes Log

## Summary

This is a greenfield setup. The existing CLAUDE.md had no Project Configuration section, so everything below is newly added content. Nothing was preserved or modified from an existing configuration.

## Added

### Project Configuration section (new)

The entire `# Project Configuration` section was generated and appended to the existing CLAUDE.md, containing:

1. **Repository Registry table** — new table with 2 rows:
   - `trustify-backend` (Rust backend service, serena_backend, /home/user/trustify-backend)
   - `trustify-ui` (TypeScript frontend, serena_ui, /home/user/trustify-ui)

2. **Jira Configuration** — new section with 5 configuration items:
   - Project key: TC
   - Cloud ID: 2b9e35e3-6bd3-4cec-b838-f4249ee02432
   - Feature issue type ID: 10142
   - Git Pull Request custom field: customfield_10875
   - GitHub Issue custom field: customfield_10747

3. **Code Intelligence** — new section with:
   - Tool naming convention explanation (`mcp__<instance>__<tool>`)
   - Example using `serena_backend` instance
   - Limitations subsection noting no known limitations

4. **Bug Configuration** — new section with 3 configuration items:
   - Bug issue type ID: 10001
   - Bug template: docs/bug-template.md
   - Bug-to-Task link type: Blocks

5. **Hierarchy Configuration** — new section with:
   - Default epic grouping strategy: by-sub-feature

## Preserved

Nothing — no existing Project Configuration content was present in the source CLAUDE.md.

## Skipped

- **Jira Field Defaults** — not configured (MCP tools were simulated, no auto-discovery of priorities and fixVersions was performed)
- **Security Configuration** — user declined to enable security triage
- **CONVENTIONS.md scaffolding** — skipped (simulation mode, no filesystem operations)
- **Constraints template copy** — skipped (simulation mode, no filesystem operations)
- **Bug template file copy** — skipped (simulation mode, as instructed)
