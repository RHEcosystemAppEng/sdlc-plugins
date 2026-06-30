# Changes Log

## Summary

All Project Configuration sections were created from scratch since the existing CLAUDE.md had no `# Project Configuration` section.

## Sections Created

### 1. Repository Registry (new)

Added table with 2 repositories:

| Repository | Role | Serena Instance | Path |
|---|---|---|---|
| backend | Rust backend service | serena_backend | /home/user/backend |
| frontend-ui | TypeScript frontend | serena_ui | /home/user/frontend-ui |

### 2. Jira Configuration (new)

Added all 5 fields:

- Project key: TC
- Cloud ID: 2b9e35e3-6bd3-4cec-b838-f4249ee02432
- Feature issue type ID: 10142
- Git Pull Request custom field: customfield_10875
- GitHub Issue custom field: customfield_10747

Note: Jira Field Defaults subsection was not created (MCP discovery of priorities and fixVersions not performed in simulation mode).

### 3. Code Intelligence (new)

- Added tool naming convention documentation (`mcp__<instance>__<tool>`)
- Added example using `serena_backend` instance
- Added Limitations subsection noting no known limitations

### 4. Bug Configuration (new)

- Bug issue type ID: 10001
- Bug template: docs/bug-template.md
- Bug-to-Task link type: Blocks

Note: Bug template file copy was skipped per simulation instructions.

### 5. Security Configuration (new)

#### Product Lifecycle

- Product pages URL: https://access.example.com/product-lifecycle
- Jira version prefix: MYPRODUCT
- Vulnerability issue type ID: 10200
- Component label pattern: pscomponent:
- VEX Justification custom field: customfield_12345
- Optional fields left empty: Upstream Affected Component, PS Component, Stream, ProdSec contact email, ProdSec Jira account ID, Embargo policy URL

#### Version Streams

Added 1 stream:

| Stream | Konflux Release Repo | Local Path | Security Matrix Path |
|---|---|---|---|
| 2.1.x | git.downstream.example.com/my-org/product-release.2.1.z | /home/user/product-release.2.1.z | security-matrix.md |

#### Source Repositories

Added 2 repositories:

| Repository | URL |
|---|---|
| backend | https://github.com/example/backend |
| frontend-ui | https://github.com/example/frontend-ui |

### 6. Hierarchy Configuration (new)

- Default epic grouping strategy: by-sub-feature

## Sections Skipped

- **Jira Field Defaults**: Not scaffolded (requires MCP discovery of available priorities and fixVersions, which was not performed in simulation mode)
- **Constraints template copy**: Skipped (simulation mode -- no file writes to target project)
- **CONVENTIONS.md scaffolding**: Skipped (simulation mode -- no file writes to target project repositories)
- **Bug template file copy**: Skipped per simulation instructions
- **security-matrix.md scaffolding**: Skipped per user instruction
- **Supportability matrix population**: User declined

## Files Written

- `outputs/claude-md-result.md` -- the generated Project Configuration section
- `outputs/discovery-log.md` -- step-by-step discovery log
- `outputs/changes-log.md` -- this file
