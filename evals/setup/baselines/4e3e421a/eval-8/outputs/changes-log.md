# Changes Log — /sdlc-workflow:setup (security matrix)

## Discovery (simulated; no MCP tools, external services, or project writes)

| Step | Finding | Action |
|---|---|---|
| 1 – Read config | `# Project Configuration` present; Repository Registry, Jira Configuration, Code Intelligence, Bug Configuration, Security Configuration present | None |
| 2 – Serena | Discovered `serena_backend`, `serena_ui`; both already in Repository Registry | "Repository Registry is up to date" |
| 3 – Jira | Project key TC, Cloud ID, Feature issue type ID 10142 all present | "Jira Configuration is up to date" |
| 5 – Code Intelligence | Covers both Serena instances, has `### Limitations` | "Code Intelligence is up to date" |
| 9 – Bug Configuration | All three fields populated | "Bug Configuration is up to date" |
| 10 – Security Configuration | Fully populated; Jira version prefix **MYPRODUCT** preserved as configured; stream 2.1.x -> `security-matrix.md`; Source Repositories `backend`, `frontend-ui` | "Security Configuration is up to date" (no edits) |
| 10.5 – Matrix existence | `security-matrix.md` missing | Scaffold proposed |

Out of scope for this task and not changed: Hierarchy Configuration and Jira Field Defaults are absent from the input CLAUDE.md; Source Repositories rows have no Deployment context column. These were noted only; no changes were proposed.

## Step 10.5 – Scaffold

- Source: `docs/templates/security-matrix.template.md` only (worked example `docs/templates/security-matrix.md` not used).
- Expanded `{source-repo-name}` / `{source-ref}` and matching separator cells in lockstep into `backend` and `frontend-ui` columns (header/separator/data = 6/6/6 cells).
- Expanded Source Pinning Method into two entries: `backend`, `frontend-ui`.
- Fixed headings and fixed column headers kept verbatim (including `Product Version`); Container Images table, Ecosystem Mappings, and Forward Pointer retained.
- User decision: **confirmed** scaffolding `security-matrix.md` for stream 2.1.x.
- Write semantics: create-if-absent after a final re-read (simulated). Proposed content is in `outputs/security-matrix-review.md`.

## Step 10.6 – Populate supportability/image identity

- User decision: **declined**. No release history read, no image evidence gathered, no `Last-Updated` timestamp set.

## Files

| File | Change |
|---|---|
| CLAUDE.md | None |
| security-matrix.md (project) | None written in this eval (proposed scaffold only) |
| outputs/security-matrix-review.md | Created (proposed scaffold review) |
| outputs/changes-log.md | Created (this log) |
