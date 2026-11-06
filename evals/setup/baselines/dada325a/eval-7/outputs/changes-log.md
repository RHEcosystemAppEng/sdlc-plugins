# Changes Log — /sdlc-workflow:setup (eval simulation)

Simulated run. I did not call any MCP tools, external services, or shell commands, and I
modified no project files. The only files written are the two in `outputs/`.

## Discovery summary

| Step | Area | Result |
|---|---|---|
| 1 | Read CLAUDE.md (`claude-md-configured-with-security.md`) | Project Configuration found |
| 2 | Serena instances (`serena_backend`, `serena_ui`) | Both already in the registry. **Repository Registry is up to date** |
| 3 | Jira Configuration | All required fields present. **Jira Configuration is up to date** |
| 3.5 | Hierarchy Configuration | Not present. Outside the scope of this request; not changed |
| 4 | Jira Field Defaults | Not present. Outside the scope of this request; not changed |
| 5 | Code Intelligence | Covers both instances and has Limitations. **Code Intelligence is up to date** |
| 7 | docs/constraints.md | Not evaluated in this simulation; not changed |
| 8 | CONVENTIONS.md | Not evaluated in this simulation; not changed |
| 9 | Bug Configuration | All three fields present. **Bug Configuration is up to date** |
| 10 | Security Configuration | Required fields populated, no placeholders. **Security Configuration is up to date** |
| 10.5 | `security-matrix.md` (2.1.x) | Missing. User confirmed the scaffold |
| 10.6 | Populate matrix | User accepted. **Blocked** by the revision label mismatch |

## Changes

### CLAUDE.md
- No changes.

### security-matrix.md (stream 2.1.x)
- **Scaffold (confirmed):** create from the plugin-root
  `docs/templates/security-matrix.template.md`. The source columns and Source Pinning
  Method entries are expanded for `backend` and `frontend-ui`. Fixed columns, Container
  Images, and Ecosystem Mappings are kept. Re-read just before the write and use
  create-if-absent semantics, so the scaffold never overwrites a file that has appeared since.
- **Population: NOT WRITTEN.** Revision label checks:
  - 2.1.0 / api-rhel9: label `0123456789abcdef0123456789abcdef01234567` equals the resolved SHA. Verified.
  - 2.1.0 / api-rhel10: label `0123456789abcdef0123456789abcdef01234567` equals the resolved SHA. Verified.
  - 2.1.1 / api-rhel10: label `fedcba9876543210fedcba9876543210fedcba98` does NOT equal the resolved
    SHA `89abcdef0123456789abcdef0123456789abcdef` (tag `v0.3.13`). **Unresolved.**
- The matrix stays unchanged until corrected evidence is verified. No `Last-Updated`
  timestamp is set and no image row is marked verified.

### Proposal and review
- The complete proposed matrix and the revision checks are in
  `outputs/security-matrix-review.md`.

## Open questions for the user
1. Corrected evidence for 2.1.1 / api-rhel10: the tag-to-commit resolution of `v0.3.13`
   versus the image revision label `fedcba98…`.
2. Whether 2.1.1 shipped an api-rhel9 image. There is no evidence for it, and I did not
   infer it.
3. How the `api-*` image components map to the configured source repositories, and
   whether `frontend-ui` ships as its own image.
4. The Forward Pointer: the next stream and release repo, or `None`.
5. Whether any 2.1.x release was a retag (affects the Notes column).

## Notes
- Source Repositories in CLAUDE.md has no Deployment Context column. The column is
  optional and defaults to `upstream`, so the existing values were preserved as they are.
