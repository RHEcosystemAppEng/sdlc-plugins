# Changes Log — /sdlc-workflow:setup (security matrix, 2.1.x)

Simulation only. No MCP tools, external services, or shell commands were invoked. No project
files were modified.

## CLAUDE.md

| Section | Status | Change |
|---|---|---|
| Repository Registry | Up to date (serena_backend, serena_ui already registered) | None |
| Jira Configuration | Up to date | None |
| Code Intelligence | Up to date | None |
| Bug Configuration | Up to date | None |
| Security Configuration | Up to date (no placeholders; optional Deployment Context absent, defaults to `upstream`) | None |
| Jira Field Defaults / Hierarchy Configuration | Absent; outside this request | None |

## security-matrix.md (2.1.x stream)

| Step | Action | Result |
|---|---|---|
| 10.5 existence check | `security-matrix.md` | Missing |
| 10.5 scaffold | Built from canonical `docs/templates/security-matrix.template.md`, not the worked example. The source column and Source Pinning entry were expanded for `backend` and `frontend-ui`. Fixed columns and Ecosystem Mappings kept. | User confirmed |
| 10.5 write | Re-read before write; create-if-absent | Proposed: create the scaffold (simulated, not written to the project) |
| 10.6 population | Evidence from `security-matrix-image-identity.md` | User accepted |
| 10.6 revision check: 2.1.0 / api-rhel9 | label `0123456789abcdef0123456789abcdef01234567` = resolved SHA | Verified |
| 10.6 revision check: 2.1.0 / api-rhel10 | label `0123456789abcdef0123456789abcdef01234567` = resolved SHA | Verified |
| 10.6 revision check: 2.1.1 / api-rhel10 | label `fedcba9876543210fedcba9876543210fedcba98` != resolved SHA `89abcdef0123456789abcdef0123456789abcdef` (tag `v0.3.13`) | **Unresolved mismatch** |
| 10.6 write | Blocked: evidence is not verified | **Matrix left unchanged.** No populated content, no partial rows, no `Last-Updated` timestamp |

## Pending user input

1. Corrected evidence for the 2.1.1 / api-rhel10 image, or the correct release tag / SHA.
2. Confirm whether a 2.1.1 api-rhel9 image exists.
3. Forward Pointer value: the next stream, or `None`.

After the corrected evidence is verified, the next steps are:
1. Present the complete proposal again.
2. Get fresh confirmation.
3. Re-read the target and compare it with the snapshot.
4. Write, then set `<!-- Last-Updated: <UTC ISO-8601> -->` on the first line.

## Files written by this eval

- /tmp/setup-eval-baseline/eval-7/outputs/security-matrix-review.md
- /tmp/setup-eval-baseline/eval-7/outputs/changes-log.md
