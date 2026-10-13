# Changes Log

## Sections Added to Project Configuration

All Project Configuration sections were newly added (no prior Project Configuration existed in CLAUDE.md):

1. **Repository Registry** — Added with table headers (Repository, Role, Serena Instance, Path) but no data rows, since no Serena instances were discovered and no repositories were registered.
2. **Jira Configuration** — Added with manually provided values: Project key (MYPROJ), Cloud ID (abc123), Feature issue type ID (10001). Git Pull Request and GitHub Issue custom fields were omitted as the user did not provide them.
3. **Code Intelligence** — Added with a note that no Serena MCP servers are configured and code intelligence is not available. Limitations subsection notes no Serena instances configured.
4. **Bug Configuration** — Added with Bug issue type ID (10001), bug template path (docs/bug-template.md), and Bug-to-Task link type (Blocks).
5. **Hierarchy Configuration** — Added with default epic grouping strategy (by-sub-feature).

## Pre-existing Content Preserved

The following pre-existing content in CLAUDE.md was preserved without modification:

- Project heading (`# my-project`) and description
- `## Documentation` section with architecture and API links
- `## Getting Started` section with setup instructions

## Sections Not Added

- **Security Configuration** — Was offered to the user during setup, but the user declined to enable security triage. Section was not added.
