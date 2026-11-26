# Changes Log — /sdlc-workflow:setup (security matrix, 2.1.x)

Simulation only. No project files were modified and no MCP or external calls were made.

## Discovery (simulated)
- Serena instances: `serena_backend` and `serena_ui` are both already in the Repository Registry, so no change.
- Atlassian MCP is present but was not called. Jira Configuration is already complete.
- Security Configuration is present and has no placeholders. Stream 2.1.x maps to `security-matrix.md`, and the source repos are `backend` and `frontend-ui`.

## CLAUDE.md
- No changes. Every existing section is preserved. Deployment Context is optional and defaults to `upstream`.
- Hierarchy Configuration and Jira Field Defaults are absent. They are out of scope for this request and were left untouched.

## security-matrix.md (2.1.x)
- The existence check found it **missing**.
- Scaffold (Step 10.5): built from `docs/templates/security-matrix.template.md` (not the worked example). Source columns were expanded to `backend` and `frontend-ui`, with one Source Pinning Method entry per repo. Ecosystem Mappings were kept. The user confirmed. Write semantics: create-if-absent after a re-read. In the simulation this was **not written**.
- Population (Step 10.6): **BLOCKED, no population write**.
  - Revision check results: 2.1.0/api-rhel9 MATCH, 2.1.0/api-rhel10 MATCH, **2.1.1/api-rhel10 MISMATCH**. The resolved SHA for `v0.3.13` is `89abcdef0123456789abcdef0123456789abcdef`, but the image `org.opencontainers.image.revision` is `fedcba9876543210fedcba9876543210fedcba98`.
  - The matrix stays unchanged until corrected evidence is verified. The `Last-Updated` timestamp was not set.
  - Asked the user for corrected 2.1.1/api-rhel10 image or tag evidence, the Forward Pointer value, retag status confirmation, and whether a 2.1.1 rhel9 image exists.
- The full proposed matrix, with the unresolved row flagged, is in `security-matrix-review.md` for review only.

## Files written (eval outputs only)
- /tmp/setup-eval-baseline/eval-7/outputs/security-matrix-review.md
- /tmp/setup-eval-baseline/eval-7/outputs/changes-log.md
