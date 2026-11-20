# Changes Log — /sdlc-workflow:setup (security matrix, 2.1.x)

Mode: simulation. No project files were modified. No MCP tools, external services, or shell commands were called.

## Inputs
- CLAUDE.md: `evals/setup/files/claude-md-configured-with-security.md`
- MCP tool listing: `evals/setup/files/mcp-tools-with-serena.md`
- Release and published-image evidence: `evals/setup/files/security-matrix-image-identity.md`

## Section Status (no CLAUDE.md changes)
| Step | Section | Result |
|---|---|---|
| 2 | Repository Registry | Up to date (serena_backend, serena_ui already registered) |
| 3 | Jira Configuration | Up to date |
| 5 | Code Intelligence | Up to date |
| 9 | Bug Configuration | Up to date |
| 10 | Security Configuration | Up to date (no placeholders; Deployment Context defaults to `upstream`) |
| 3.5 / 4 | Hierarchy Configuration, Jira Field Defaults | Missing from the supplied CLAUDE.md. Outside this request, not changed. Running full setup would offer them. |

**CLAUDE.md: no changes.**

## Security Matrix Actions
| # | Action | Target | Status |
|---|---|---|---|
| 1 | Existence check | `security-matrix.md` (2.1.x) | Missing |
| 2 | Scaffold from `docs/templates/security-matrix.template.md` with backend + frontend-ui columns and Source Pinning entries; Ecosystem Mappings kept | `security-matrix.md` | User confirmed. Proposed with create-if-absent semantics (re-read before writing; never overwrite). Not written in this simulation. |
| 3 | Revision label check: 2.1.0 / api-rhel9 | image `sha256:aaaa…` | MATCH (`0123456789abcdef…01234567`) |
| 4 | Revision label check: 2.1.0 / api-rhel10 | image `sha256:bbbb…` | MATCH (`0123456789abcdef…01234567`) |
| 5 | Revision label check: 2.1.1 / api-rhel10 | image `sha256:cccc…` | **MISMATCH**: label `fedcba9876543210fedcba9876543210fedcba98` ≠ resolved `89abcdef0123456789abcdef0123456789abcdef` (tag `v0.3.13`) |
| 6 | Populate Supportability Matrix, Container Images, Source Pinning Method, Ecosystem Mappings | `security-matrix.md` | **BLOCKED**. Matrix left unchanged until corrected evidence is verified. Draft is in the review file for reference only. |
| 7 | Set `<!-- Last-Updated -->` timestamp | `security-matrix.md` | Not set (nothing was written) |

## Open Items for the User
1. Corrected evidence for the 2.1.1 / api-rhel10 published image vs. the `v0.3.13` tag resolution.
2. Whether api-rhel9 shipped in 2.1.1. There is no evidence for it, so no row was inferred.
3. Forward Pointer value for the 2.1.x matrix.
4. Retag status or Notes for 2.1.0 and 2.1.1. The evidence does not cover it.

## Output Files
- `/tmp/setup-eval-baseline/eval-7/outputs/security-matrix-review.md`
- `/tmp/setup-eval-baseline/eval-7/outputs/changes-log.md`
