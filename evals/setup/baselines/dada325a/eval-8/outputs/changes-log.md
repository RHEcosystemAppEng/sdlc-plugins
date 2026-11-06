# Changes Log — /sdlc-workflow:setup (security matrix scaffold)

## Discovery (simulated, no MCP/external calls)

| Step | Result |
|---|---|
| 1 – Read existing configuration | Project Configuration present; all sections populated |
| 2 – Serena instances | `serena_backend`, `serena_ui` discovered; both already in Repository Registry — "Repository Registry is up to date" |
| 3 – Jira Configuration | Project key, Cloud ID, Feature issue type ID present — "Jira Configuration is up to date" |
| 3.5 – Hierarchy Configuration | Not present; out of scope for this task (security matrix only) — no change proposed |
| 4 – Jira Field Defaults | Not present; out of scope for this task — no change proposed |
| 5 – Code Intelligence | Covers both Serena instances — "Code Intelligence is up to date" |
| 9 – Bug Configuration | All three fields populated — "Bug Configuration is up to date" |
| 10 – Security Configuration | Fully populated (Jira version prefix `MYPRODUCT`) — "Security Configuration is up to date" |
| 10.5 – security-matrix.md | Stream `2.1.x` → `security-matrix.md` missing; user confirmed scaffold |
| 10.6 – Supportability/image population | User declined — skipped |

## Proposed Changes

1. **Create `security-matrix.md`** (stream 2.1.x) from `docs/templates/security-matrix.template.md` with create-if-absent semantics.
   - Supportability Matrix: `{source-repo-name}` expanded to `backend` and `frontend-ui` columns; separator and `` `{source-ref}` `` value cells expanded in lockstep (6 columns total).
   - Source Pinning Method: two entries, `backend` and `frontend-ui`, with `{source-pinning-method}` left unfilled.
   - All fixed headings, comments, fixed columns, Container Images table, Ecosystem Mappings, and Forward Pointer retained verbatim from the template. No heading rewritten.
   - No `Last-Updated` timestamp added (population declined).
   - Full proposed content: `outputs/security-matrix-review.md`.

## Not Changed

- CLAUDE.md — no modifications (all relevant sections up to date).
- No actual project files written; no MCP tools, external services, or Jira calls used.
- `docs/templates/security-matrix.md` (worked example) not used as a scaffold source.
