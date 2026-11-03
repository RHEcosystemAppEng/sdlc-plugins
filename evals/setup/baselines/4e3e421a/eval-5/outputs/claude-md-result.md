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

### Jira Field Defaults

- Default priority: none
- fixVersion scope: both
- Prompt for priority: true
- Prompt for fixVersion: true

## Code Intelligence

Tools are prefixed by Serena instance name: `mcp__<instance>__<tool>`.

For example, to search for a symbol in a repository whose Serena instance
is `serena_backend`:

    mcp__serena_backend__find_symbol(
      name_path_pattern="MyService",
      substring_matching=true,
      include_body=false
    )

### Limitations

No known limitations for `serena_backend` or `serena_ui`.

## Security Configuration

<!-- TODO: This section configures project-specific security triage settings.
     It is consumed by the triage-security skill and scaffolded by the setup skill.
     Run /setup to populate interactively, or fill in manually using the
     placeholders below. -->

### Product Lifecycle

<!-- Required fields:
     - Product pages URL: the product lifecycle page for EOL/support status checks
     - Jira version prefix: filters Jira versions to this product (e.g., "MYPRODUCT")
     - Vulnerability issue type ID: the Jira issue type for Vulnerability issues
     - Component label pattern: the label prefix used by PSIRT on Vulnerability issues
       to identify the affected component (e.g., "pscomponent:")

     Optional fields (left blank = feature disabled):
     - VEX Justification custom field: Jira custom field ID for VEX Justification
     - Upstream Affected Component custom field: enables cross-CVE overlap detection
     - PS Component custom field / Stream custom field: cross-CVE overlap filtering
     - ProdSec contact email / ProdSec Jira account ID: security team notification
     - Embargo policy URL: coordinated vulnerability disclosure warning gate -->

- Product pages URL: https://access.example.com/product-lifecycle
- Jira version prefix: MYPRODUCT
- Vulnerability issue type ID: 10200
- Component label pattern: pscomponent:
- VEX Justification custom field: customfield_12345
- Upstream Affected Component custom field:
- PS Component custom field:
- Stream custom field:
- ProdSec contact email:
- ProdSec Jira account ID:
- Embargo policy URL:

### Version Streams

<!-- One row per version stream. Each stream maps to a Konflux release repo and a
     local security-matrix.md file.
     - Konflux Release Repo: the git repository URL
     - Local Path: the user's local clone path to the Konflux release repo
     - Security Matrix Path: path to security-matrix.md relative to the project
       working directory -->

| Stream | Konflux Release Repo | Local Path | Security Matrix Path |
|---|---|---|---|
| 2.1.x | git.downstream.example.com/my-org/product-release.2.1.z | /home/user/product-release.2.1.z | security-matrix.md |

### Source Repositories

<!-- One row per source repository whose dependencies are tracked for CVEs.
     Deployment Context (defaults to upstream):
     - internal: Private repos, internal tools/services. No public disclosure needed.
     - upstream: Public upstream components. Coordinate with upstream maintainers.
     - customer-shipped: Products shipped to customers. Full Product Security coordination required. -->

| Repository | URL | Deployment Context |
|---|---|---|
| backend | https://github.com/example/backend | upstream |
| frontend-ui | https://github.com/example/frontend-ui | upstream |

## Bug Configuration

- Bug issue type ID: 10001
- Bug template: docs/bug-template.md
- Bug-to-Task link type: Blocks

## Hierarchy Configuration

- Default epic grouping strategy: by-repository
