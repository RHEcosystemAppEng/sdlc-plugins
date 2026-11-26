# Changes Log — /sdlc-workflow:setup (security matrix)

## Discovery (simulated; no MCP tools, external services, or shell commands invoked)

| Step | Result |
|---|---|
| Step 1 – Read existing configuration | `# Project Configuration` present with Repository Registry, Jira Configuration, Code Intelligence, Bug Configuration, Security Configuration |
| Step 2 – Serena instances | Discovered `serena_backend`, `serena_ui` from MCP tool listing; both already in Repository Registry — "Repository Registry is up to date" |
| Step 3 – Jira Configuration | Project key, Cloud ID, Feature issue type ID populated — "Jira Configuration is up to date" |
| Step 5 – Code Intelligence | Covers both Serena instances, has `### Limitations` — "Code Intelligence is up to date" |
| Step 9 – Bug Configuration | All three fields populated — "Bug Configuration is up to date" |
| Step 10 – Security Configuration | Present, required fields populated (Jira version prefix `MYPRODUCT`), no placeholders — "Security Configuration is up to date" |
| Step 10.5 – security-matrix.md | Stream `2.1.x` → path `security-matrix.md` → **missing**; scaffold proposed |
| Step 10.6 – Supportability / image population | Offered; **user declined** — skipped |

Out of scope for this task (not changed): Hierarchy Configuration, Jira Field Defaults, constraints.md, CONVENTIONS.md.

## Proposed Changes

| # | File | Action | Details | Status |
|---|---|---|---|---|
| 1 | `security-matrix.md` (stream 2.1.x) | Create (create-if-absent) | Scaffold from `docs/templates/security-matrix.template.md`; `{source-repo-name}` header, separator, and `{source-ref}` value cells expanded in lockstep into `backend` and `frontend-ui` columns; Source Pinning Method expanded into `backend` and `frontend-ui` entries; fixed columns, headings, Container Images, Ecosystem Mappings, and Forward Pointer retained verbatim | User confirmed; written to `outputs/security-matrix-review.md` only (eval — no project file modified) |

## Not Changed

- CLAUDE.md — no modifications (all Project Configuration sections already up to date; Security Configuration preserved as-is).
- No other project files created or modified.
- No Supportability Matrix rows, Container Images rows, pinning methods, or Ecosystem Mappings populated (user declined Step 10.6).
- No `Last-Updated` timestamp added.
