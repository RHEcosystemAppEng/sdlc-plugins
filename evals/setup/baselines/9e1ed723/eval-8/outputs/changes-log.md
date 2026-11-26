# Changes Log — /sdlc-workflow:setup (security matrix, simulated)

## Proposed Changes

| # | Target | Change | Status |
|---|---|---|---|
| 1 | `security-matrix.md` (stream 2.1.x) | Create new file from `docs/templates/security-matrix.template.md`, expanding `{source-repo-name}` / `{source-ref}` and matching separator cells into `backend` and `frontend-ui` columns, plus one Source Pinning Method entry each | Confirmed by user (simulated; captured in `security-matrix-review.md`, not written to project) |

## No Changes

- CLAUDE.md: no modifications. Repository Registry, Jira Configuration, Code Intelligence, Bug Configuration, and Security Configuration (Product Lifecycle with Jira version prefix `MYPRODUCT`, Version Streams, Source Repositories) are already fully populated.
- Template fixed headings and placeholders other than `{source-repo-name}` / `{source-ref}` (e.g., `{stream}`, `{version}`, `{component}`, `{ecosystem}`, `{forward-pointer}`) left unchanged.
- Container Images table, Ecosystem Mappings table, Forward Pointer: retained as in template.
- No `<!-- Last-Updated -->` timestamp added.

## Declined

- Step 10.6 Supportability Matrix / Container Images population — declined by user. No release history, image digests, or revision labels were gathered.

## Not Performed

- No MCP tool calls (Serena, Atlassian), external service calls, or shell commands against the project; discovery was simulated from the provided input files.
- No actual project files were created or modified.
