# Changes Log

## Preserved

- All existing content in CLAUDE.md preserved (project title, Documentation section, Getting Started section)
- No existing configuration was overwritten (CLAUDE.md had no prior Project Configuration)

## Added

### Project Configuration (new section appended to CLAUDE.md)

1. **Repository Registry** — new table with headers only (Repository, Role, Serena Instance, Path); no data rows because no Serena instances were discovered and the user chose to continue without code intelligence

2. **Jira Configuration** — new section with three fields provided via manual entry:
   - Project key: MYPROJ
   - Cloud ID: abc123
   - Feature issue type ID: 10001
   - Git Pull Request custom field: omitted (user declined)
   - GitHub Issue custom field: omitted (user declined)

3. **Code Intelligence** — new section indicating no Serena MCP servers are configured, with Limitations subsection noting no limitations are known

4. **Bug Configuration** — new section with three fields:
   - Bug issue type ID: 10001 (provided manually)
   - Bug template: docs/bug-template.md (default accepted)
   - Bug-to-Task link type: Blocks (default accepted)

## Not Added

- **Jira Field Defaults** — skipped; requires MCP or REST API to discover available priorities and fixVersions, neither of which is available
- **Hierarchy Configuration** — skipped; requires MCP or REST API to discover issue type hierarchy, neither of which is available
- **Security Configuration** — skipped; user declined when asked whether to enable security triage
- **Constraints file** (docs/constraints.md) — skipped in simulation mode
- **Bug template file** (docs/bug-template.md) — skipped in simulation mode
- **CONVENTIONS.md** — no repositories in Registry to scaffold for
