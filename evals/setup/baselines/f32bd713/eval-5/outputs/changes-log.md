# Changes Log

## Preserved

The following existing content from CLAUDE.md was preserved unchanged:

- **Project heading**: `# my-project` and description ("A web application for managing inventory.")
- **Documentation section**: `## Documentation` with links to architecture.md and api.md
- **Getting Started section**: `## Getting Started` with 3-step setup instructions

## Added

All Project Configuration sections are new (no prior Project Configuration existed):

- **`# Project Configuration`** — top-level heading added
- **`## Repository Registry`** — table with 2 repositories (backend via serena_backend, frontend-ui via serena_ui)
- **`## Jira Configuration`** — 5 fields (Project key, Cloud ID, Feature issue type ID, Git Pull Request custom field, GitHub Issue custom field)
- **`## Code Intelligence`** — naming convention documentation with concrete example, `### Limitations` subsection (no known limitations)
- **`## Bug Configuration`** — 3 fields (Bug issue type ID, Bug template path, Bug-to-Task link type)
- **`## Security Configuration`** — new section with 3 subsections:
  - **`### Product Lifecycle`** — 5 fields (Product pages URL, Jira version prefix, Vulnerability issue type ID, Component label pattern, VEX Justification custom field)
  - **`### Version Streams`** — table with 1 stream (2.1.x)
  - **`### Source Repositories`** — table with 2 repositories (backend, frontend-ui)
