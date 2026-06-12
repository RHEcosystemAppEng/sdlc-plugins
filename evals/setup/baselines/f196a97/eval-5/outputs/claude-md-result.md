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
| backend | Rust backend service | serena_backend | /home/user/backend |
| frontend-ui | TypeScript frontend | serena_ui | /home/user/frontend-ui |

## Jira Configuration

- Project key: TC
- Cloud ID: 2b9e35e3-6bd3-4cec-b838-f4249ee02432
- Feature issue type ID: 10142
- Git Pull Request custom field: customfield_10875
- GitHub Issue custom field: customfield_10747

## Code Intelligence

Tools are prefixed by Serena instance name: `mcp__<instance>__<tool>`.

- `mcp__serena_backend__<tool>` — Rust backend service (backend)
- `mcp__serena_ui__<tool>` — TypeScript frontend (frontend-ui)

### Limitations

No known limitations for either Serena instance.

## Security Configuration

### Product Lifecycle

- Product pages URL: https://access.example.com/product-lifecycle
- Jira version prefix: MYPRODUCT
- Vulnerability issue type ID: 10200
- Component label pattern: pscomponent:
- VEX Justification custom field: customfield_12345

### Version Streams

| Stream | Konflux Release Repo | Local Path | Security Matrix Path |
|---|---|---|---|
| 2.1.x | git.downstream.example.com/my-org/product-release.2.1.z | /home/user/product-release.2.1.z | security-matrix.md |

### Source Repositories

| Repository | URL |
|---|---|
| backend | https://github.com/example/backend |
| frontend-ui | https://github.com/example/frontend-ui |
