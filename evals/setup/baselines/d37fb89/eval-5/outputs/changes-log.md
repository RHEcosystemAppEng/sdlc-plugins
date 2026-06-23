# Setup Changes Log

All sections below were newly added to CLAUDE.md. The existing content (project description, documentation links, getting started steps) was preserved unchanged.

## Sections Added

- **# Project Configuration** — Top-level section header added; did not exist previously.
- **## Repository Registry** — New section; table with 2 rows: `backend` (serena_backend) and `frontend-ui` (serena_ui).
- **## Jira Configuration** — New section; populated with project key, Cloud ID, feature issue type ID, Git Pull Request custom field, and GitHub Issue custom field.
- **## Code Intelligence** — New section; describes `mcp__<instance>__<tool>` naming convention with a `serena_backend` example. Includes ### Limitations subsection stating no known limitations.
- **## Bug Configuration** — New section; populated with Bug issue type ID (10001), Bug template (docs/bug-template.md), and Bug-to-Task link type (Blocks).
- **## Security Configuration** — New section; opted in by the user. Includes three subsections:
  - **### Product Lifecycle** — 5 fields: Product pages URL, Jira version prefix, Vulnerability issue type ID, Component label pattern, VEX Justification custom field.
  - **### Version Streams** — Table with 1 row for stream 2.1.x.
  - **### Source Repositories** — Table with 2 rows: backend and frontend-ui.
