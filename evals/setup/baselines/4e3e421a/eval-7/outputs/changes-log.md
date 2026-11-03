# Changes Log — /sdlc-workflow:setup (security matrix, 2.1.x)

Simulation only. No MCP tools, external services, or shell commands invoked against project
systems. No actual project files modified.

## CLAUDE.md

- No changes. Repository Registry, Jira Configuration, Code Intelligence, Bug Configuration,
  and Security Configuration are up to date.
- Not touched (out of scope for this request): `## Hierarchy Configuration` and
  `### Jira Field Defaults` are absent and can be set up in a later `/setup` run. The optional
  Deployment Context column in Source Repositories is absent (defaults to `upstream`).

## security-matrix.md (stream 2.1.x, configured path `security-matrix.md`)

| Action | Status |
|---|---|
| Existence check | Missing |
| Scaffold from `docs/templates/security-matrix.template.md` (columns expanded for `backend`, `frontend-ui`) | Proposed; user confirmed; write is create-if-absent with a re-read just before writing (never overwrites a file that has appeared since the check) |
| Populate Supportability Matrix / Container Images / Source Pinning / Ecosystem Mappings | **Blocked — not written** |
| `<!-- Last-Updated -->` timestamp | Not set (only set after a confirmed, verified write) |

### Revision checks

| Product Version | Component | Result |
|---|---|---|
| 2.1.0 | api-rhel9 | Match (`0123456…01234567`) |
| 2.1.0 | api-rhel10 | Match (`0123456…01234567`) |
| 2.1.1 | api-rhel10 | **Mismatch**: tag `v0.3.13` resolves to `89abcdef0123456789abcdef0123456789abcdef`; image label is `fedcba9876543210fedcba9876543210fedcba98` |

### Open items requested from the user

1. Corrected evidence for 2.1.1 / api-rhel10 (correct tag resolution, or correct image/digest
   whose revision label matches, or an explanation of the retag along with the authoritative commit).
2. Forward Pointer (next stream or `None`).
3. Confirm that the 2.1.0 rhel9 and rhel10 images are meant to share the same CPE.
4. Confirm whether a 2.1.1 api-rhel9 image exists (no evidence was supplied, so no row was invented).

## Output files

- `outputs/security-matrix-review.md`: discovery summary, scaffold, revision checks, draft
  proposal, write procedure
- `outputs/changes-log.md`: this file
