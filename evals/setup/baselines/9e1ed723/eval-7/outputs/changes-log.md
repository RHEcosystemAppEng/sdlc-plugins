# Changes Log — /sdlc-workflow:setup (eval simulation, security matrix)

## Project files modified

**None.** This is an eval simulation. No changes were made to CLAUDE.md,
`security-matrix.md`, or any other project file. No MCP tools, external services
or shell commands were used for discovery.

## Step outcomes

| Step | Outcome |
|---|---|
| 1. Read existing configuration | Parsed `claude-md-configured-with-security.md`. Project Configuration is present |
| 2. Serena discovery | Found `serena_backend` and `serena_ui`. Both are already registered, so "Repository Registry is up to date" |
| 3. Jira Configuration | "Jira Configuration is up to date" |
| 3.5 / 4. Hierarchy and Jira Field Defaults | Not in scope for this security-matrix request. Not discovered and not modified |
| 5. Code Intelligence | "Code Intelligence is up to date" |
| 6. Write configuration | No CLAUDE.md changes are needed |
| 7 / 8. Constraints and CONVENTIONS.md | Not in scope for this request. Not modified |
| 9. Bug Configuration | "Bug Configuration is up to date" |
| 10. Security Configuration | "Security Configuration is up to date". Existing values are kept, and the optional Deployment Context column and other optional fields are not added or overwritten |
| 10.5 Scaffold `security-matrix.md` (2.1.x) | Missing. The user confirmed scaffolding. A scaffold was proposed from `docs/templates/security-matrix.template.md` with source columns expanded for backend and frontend-ui, using create-if-absent semantics. Not written (simulation) |
| 10.6 Populate from evidence | Complete proposal built and presented. **Write blocked**: revision mismatch on 2.1.1 / api-rhel10 |
| 11. Validate | Nothing was written, so there was nothing to re-validate |

## Revision verification summary

- 2.1.0 / api-rhel9: label equals resolved SHA `0123456789abcdef0123456789abcdef01234567`, so verified.
- 2.1.0 / api-rhel10: label equals resolved SHA `0123456789abcdef0123456789abcdef01234567`, so verified.
- 2.1.1 / api-rhel10: label `fedcba9876543210fedcba9876543210fedcba98` does not equal the
  SHA `89abcdef0123456789abcdef0123456789abcdef` resolved from `v0.3.13`. **This is unresolved.**

## Pending user actions

1. Supply corrected evidence for the 2.1.1 / api-rhel10 mismatch: the tag resolution or retag history, or the correct image and digest.
2. Confirm whether 2.1.1 ships an api-rhel9 image. If it does, supply its tag, SHA, image, digest and CPE.
3. Provide retag status for `v0.3.12` and `v0.3.13`.
4. Confirm that frontend-ui has no separately published image.
5. Provide the Forward Pointer: the next stream's matrix path, or "None".

After the evidence is verified, the skill will re-present the complete matrix and
get fresh confirmation. Just before writing, it will re-read `security-matrix.md`
and compare it against the snapshot (absent). It will write with create-if-absent
semantics, or merge and re-confirm if the file has appeared. Finally it will set
`<!-- Last-Updated: <current UTC ISO-8601> -->` on the first line.

## Output files

- `/tmp/setup-eval-baseline/eval-7/outputs/security-matrix-review.md`
- `/tmp/setup-eval-baseline/eval-7/outputs/changes-log.md`
