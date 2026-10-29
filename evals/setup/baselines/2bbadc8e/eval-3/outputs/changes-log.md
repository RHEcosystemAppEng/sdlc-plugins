# Changes Log

## What was preserved

- Project heading (`# my-project`) and description — preserved from existing CLAUDE.md
- `## Documentation` section — preserved unchanged
- `## Getting Started` section — preserved unchanged

## What was added

All Project Configuration sections are new (the existing CLAUDE.md had no `# Project Configuration` section):

1. **Repository Registry** (new table) — table headers only, no data rows. No Serena instances were discovered, so no repositories are registered.
2. **Jira Configuration** (new section) — 3 fields populated via manual entry: Project key (MYPROJ), Cloud ID (abc123), Feature issue type ID (10001). Git Pull Request and GitHub Issue custom fields were not provided.
3. **Code Intelligence** (new section) — documents that no Serena MCP servers are configured and code intelligence is not available. Includes a Limitations subsection noting no instances to document.
4. **Bug Configuration** (new section) — 3 fields populated: Bug issue type ID (10001), Bug template (docs/bug-template.md), Bug-to-Task link type (Blocks).

## What was not added

- **Security Configuration** — the user declined the opt-in prompt for security triage. This section was not created.
- **Hierarchy Configuration** — not scaffolded (depends on Jira hierarchy discovery which was not available without MCP or REST API).
- **Jira Field Defaults** — not scaffolded (depends on MCP or REST API for priority/fixVersion discovery).

## Summary

- Sections added: 1 (`# Project Configuration` with 4 subsections: Repository Registry, Jira Configuration, Code Intelligence, Bug Configuration)
- Sections preserved: 3 (project heading, Documentation, Getting Started)
- Sections modified: 0
- Sections declined: 1 (Security Configuration)
