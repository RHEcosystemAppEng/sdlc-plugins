# Discovery Log

## Serena Instances

- `serena_backend` — already configured in Repository Registry (mapped to `backend` at `/home/user/backend`). Up to date.
- `serena_ui` — already configured in Repository Registry (mapped to `frontend-ui` at `/home/user/frontend-ui`). Up to date.

## Jira Configuration

Already up to date. All fields present and populated:
- Project key: TC
- Cloud ID: 2b9e35e3-6bd3-4cec-b838-f4249ee02432
- Feature issue type ID: 10142
- Git Pull Request custom field: customfield_10875
- GitHub Issue custom field: customfield_10747

## Code Intelligence

Already up to date. Naming convention, example, and Limitations section are all present with entries for both `serena_backend` and `serena_ui`.

## Bug Configuration

Already up to date. All fields present and populated:
- Bug issue type ID: 10001
- Bug template: docs/bug-template.md
- Bug-to-Task link type: Blocks

## Security Configuration

Already fully configured. Up to date. All subsections present and populated:
- Product Lifecycle: all required fields set (Product pages URL, Jira version prefix, Vulnerability issue type ID, Component label pattern, VEX Justification custom field)
- Version Streams: 1 stream configured (2.1.x)
- Source Repositories: 2 repositories configured (backend, frontend-ui)

Security Configuration opt-in was NOT offered because the section already exists and is fully populated (idempotency).
