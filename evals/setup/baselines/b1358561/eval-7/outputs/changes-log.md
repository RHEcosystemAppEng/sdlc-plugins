# Changes Log — /sdlc-workflow:setup (security matrix, simulated)

## Summary

No project files were modified. A matrix proposal was prepared for review; writing it is blocked by an unresolved
image revision mismatch.

## Step-by-step

| Step | Result |
|---|---|
| 1 – Read existing configuration | Read `claude-md-configured-with-security.md`. Found Project Configuration with Repository Registry (backend, frontend-ui), Jira Configuration, Code Intelligence, Bug Configuration, Security Configuration. |
| 2 – Serena discovery (simulated from `mcp-tools-with-serena.md`) | Found `serena_backend`, `serena_ui` — both already registered. "Repository Registry is up to date." |
| 3 – Jira Configuration | All required fields present. "Jira Configuration is up to date." |
| 3.5 – Hierarchy Configuration | Not present; out of scope for this security-matrix request — not changed. |
| 4 – Jira Field Defaults | Not present; out of scope for this request — not changed. |
| 5 – Code Intelligence | Covers both instances. "Code Intelligence is up to date." |
| 6 – Write Configuration | No CLAUDE.md changes. |
| 7 / 8 / 9 | Not part of this request; no changes. Bug Configuration fully populated ("up to date"). |
| 10 – Security Configuration | Present, no `{{placeholder}}` markers. "Security Configuration is up to date." (Source Repositories table has no Deployment Context column; optional, defaults to upstream — left unchanged.) |
| 10.5 – Scaffold security-matrix.md | Stream `2.1.x` → `security-matrix.md` missing (simulated). User confirmed scaffolding. Scaffold source: **`docs/templates/security-matrix.template.md` only** (canonical). `docs/templates/security-matrix.md` (worked example) NOT used as template or fallback. Expanded `{source-repo-name}`/`{source-ref}` + separators into `backend` and `frontend-ui` columns; two Source Pinning Method entries; fixed columns, Container Images, Ecosystem Mappings retained. |
| 10.6 – Populate from evidence | User accepted. Populated from `security-matrix-image-identity.md`: 2 Supportability rows (2.1.0, 2.1.1), 2 verified Container Images rows (2.1.0 api-rhel9, 2.1.0 api-rhel10), Source Pinning Methods, Ecosystem Mappings (Cargo/backend, npm/frontend-ui). |
| 11 – Validate | Not run — nothing written. |

## Revision checks

- 2.1.0 api-rhel9: `v0.3.12` → `0123456789abcdef0123456789abcdef01234567`; label matches — verified.
- 2.1.0 api-rhel10: `v0.3.12` → `0123456789abcdef0123456789abcdef01234567`; label matches — verified.
- 2.1.1 api-rhel10: `v0.3.13` → `89abcdef0123456789abcdef0123456789abcdef`; label `fedcba9876543210fedcba9876543210fedcba98` — **MISMATCH, blocked**. Not presented as a verified mapping; excluded from the proposed Container Images table; corrected evidence requested.

## Open questions for the user

1. Corrected evidence for 2.1.1 api-rhel10 (revision mismatch).
2. Was a 2.1.1 api-rhel9 image shipped? No evidence supplied; no row proposed.
3. Forward Pointer: `None` (latest stream) or a next stream?

## Files

| File | Action |
|---|---|
| `security-matrix.md` (project) | NOT written — awaiting confirmation and mismatch resolution; will use create-if-absent with pre-write re-read against the (absent) source snapshot. |
| `CLAUDE.md` (project) | No changes. |
| `outputs/security-matrix-review.md` | Written (eval output: full proposal + revision checks). |
| `outputs/changes-log.md` | Written (this file). |
