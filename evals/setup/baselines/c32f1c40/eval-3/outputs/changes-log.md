# Changes Log

## CLAUDE.md — Project Configuration

**Action**: Append new `# Project Configuration` section to end of existing CLAUDE.md

### Sections Added

1. **## Repository Registry** — Empty table (headers only, no data rows). No Serena instances were discovered.

2. **## Jira Configuration** — Manual entry with 3 required fields:
   - Project key: MYPROJ
   - Cloud ID: abc123
   - Feature issue type ID: 10001
   - Git Pull Request custom field: omitted (not provided)
   - GitHub Issue custom field: omitted (not provided)

3. **## Code Intelligence** — Note that no Serena MCP servers are configured. Includes `### Limitations` subsection stating no limitations known.

4. **## Bug Configuration** — All 3 fields populated:
   - Bug issue type ID: 10001
   - Bug template: docs/bug-template.md
   - Bug-to-Task link type: Blocks

5. **## Hierarchy Configuration** — Default epic grouping strategy set to by-sub-feature.

### Sections Not Created

- **### Jira Field Defaults** — Skipped. No MCP or REST API available to discover priorities and fixVersions; eval did not provide manual values.
- **## Security Configuration** — User declined security triage opt-in.

## Other Files

- **docs/constraints.md** — Would be created from constraints.template.md (skipped in simulation)
- **docs/bug-template.md** — Would be created from plugin bug-template.md (skipped in simulation)
- **CONVENTIONS.md** — Not applicable (no repositories in Registry)
