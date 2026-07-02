# Discovery Log

## Project Configuration

- **Greenfield project**: No existing Project Configuration found in CLAUDE.md. All sections created from scratch.
- **Project config contract**: Read docs/project-config-contract.md to determine required and optional section structure.

## Repository Registry

- Discovered two Serena MCP server instances:
  - `serena_backend` serving repository `backend` (Rust backend service) at `/home/user/backend`
  - `serena_ui` serving repository `frontend-ui` (TypeScript frontend) at `/home/user/frontend-ui`
- No limitations reported for either Serena instance.

## Jira Configuration

- Collected from user:
  - Project key: TC
  - Cloud ID: 2b9e35e3-6bd3-4cec-b838-f4249ee02432
  - Feature issue type ID: 10142
  - Git Pull Request custom field: customfield_10875
  - GitHub Issue custom field: customfield_10747

## Bug Configuration

- Bug issue type ID: 10001
- Bug template path: docs/bug-template.md (default)
- Bug-to-Task link type: Blocks (default)

## Security Configuration

- **User opted in** to Security Configuration when prompted.
- Collected Product Lifecycle settings:
  - Product pages URL: https://access.example.com/product-lifecycle
  - Jira version prefix: MYPRODUCT
  - Vulnerability issue type ID: 10200
  - Component label pattern: pscomponent:
  - VEX Justification custom field: customfield_12345
- Collected one Version Stream:
  - 2.1.x with Konflux release repo at git.downstream.example.com/my-org/product-release.2.1.z, local path /home/user/product-release.2.1.z, security matrix at security-matrix.md
- Collected two Source Repositories:
  - backend (https://github.com/example/backend)
  - frontend-ui (https://github.com/example/frontend-ui)
- User declined optional supportability matrix population.
- User skipped security-matrix.md scaffolding.
