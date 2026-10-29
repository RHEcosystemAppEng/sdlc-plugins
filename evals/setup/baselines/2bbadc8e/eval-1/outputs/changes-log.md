# Changes Log

## What Was Preserved

The existing CLAUDE.md (`claude-md-empty.md`) contained the following non-configuration content that is preserved:

- `# my-project` heading
- `## Documentation` section with architecture and API links
- `## Getting Started` section with setup instructions

No Project Configuration section existed — all configuration sections are newly added.

## What Was Added

1. **Repository Registry** (new table)
   - Added row: trustify-backend | Rust backend service | serena_backend | /home/user/trustify-backend
   - Added row: trustify-ui | TypeScript frontend | serena_ui | /home/user/trustify-ui

2. **Jira Configuration** (new section)
   - Project key: TC
   - Cloud ID: 2b9e35e3-6bd3-4cec-b838-f4249ee02432
   - Feature issue type ID: 10142
   - Git Pull Request custom field: customfield_10875
   - GitHub Issue custom field: customfield_10747

3. **Code Intelligence** (new section)
   - Documented `mcp__<instance>__<tool>` naming convention
   - Added example using serena_backend
   - Added Limitations subsection (no limitations reported)

4. **Bug Configuration** (new section)
   - Bug issue type ID: 10001
   - Bug template: docs/bug-template.md
   - Bug-to-Task link type: Blocks

## What Was Not Added

- **Security Configuration** — user declined the opt-in prompt

## Summary

- Sections added: 1 (Project Configuration with 4 subsections: Repository Registry, Jira Configuration, Code Intelligence, Bug Configuration)
- Sections modified: 0
- Sections preserved: 3 (my-project heading, Documentation, Getting Started)
- Sections declined: 1 (Security Configuration)
