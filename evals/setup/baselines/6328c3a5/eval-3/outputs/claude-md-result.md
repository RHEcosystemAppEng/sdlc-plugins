<!-- SYNTHETIC TEST DATA — CLAUDE.md with no Project Configuration, simulating a greenfield project -->

# my-project

A web application for managing inventory.

## Documentation

- [docs/architecture.md](docs/architecture.md) — System architecture overview
- [docs/api.md](docs/api.md) — REST API reference

## Getting Started

1. Clone the repository
2. Run `npm install`
3. Run `npm start`

# Project Configuration

## Repository Registry

| Repository | Role | Serena Instance | Path |
|---|---|---|---|

## Jira Configuration

- Project key: MYPROJ
- Cloud ID: abc123
- Feature issue type ID: 10001

### Jira Field Defaults

- Default priority: (none)
- fixVersion scope: both
- Prompt for priority: true
- Prompt for fixVersion: true

## Code Intelligence

Tools are prefixed by Serena instance name: `mcp__<instance>__<tool>`.

For example, to search for a symbol in a repository whose Serena instance is `<instance>`:

    mcp__<instance>__find_symbol(name_path_pattern="MyService")

No Serena MCP servers are configured. Code intelligence is not available.

### Limitations

No limitations known — no Serena instances configured.

## Bug Configuration

- Bug issue type ID: 10001
- Bug template: [docs/bug-template.md](docs/bug-template.md)
- Bug-to-Task link type: Blocks

## Hierarchy Configuration

- Default epic grouping strategy: by-sub-feature
