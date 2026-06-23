# Changes Log

## Project Configuration — Newly Added

All Project Configuration sections were newly added to the CLAUDE.md file. The existing content (project description, documentation links, getting started instructions) was preserved.

### Sections Added

1. **Project Configuration** (top-level heading) — New section added below existing content.

2. **Repository Registry** — Added table with headers (Repository, Role, Serena Instance, Path) and no data rows. No Serena instances are available, so no repositories were registered.

3. **Jira Configuration** — Added with manually entered fields:
   - Project key: MYPROJ
   - Cloud ID: abc123
   - Feature issue type ID: 10001
   - No Git Pull Request custom field (not provided)
   - No GitHub Issue custom field (not provided)

4. **Code Intelligence** — Added section noting no Serena MCP servers are configured and code intelligence is not available. Documented the `mcp__<instance>__<tool>` naming convention for future reference.

5. **Limitations** — Added subsection under Code Intelligence noting no limitations known since no Serena instances are configured.

6. **Bug Configuration** — Added with:
   - Bug issue type ID: 10001
   - Bug template: docs/bug-template.md
   - Bug-to-Task link type: Blocks

### Sections Not Added

- **Security Configuration** — User declined security configuration setup.
