# Changes Log — /sdlc-workflow:setup (eval simulation)

No real project files, MCP tools, external services or shell commands were used to change anything.
All discovery was simulated from the supplied input files.

## Step Results

| Step | Result |
|---|---|
| 1 – Read existing configuration | Parsed `# Project Configuration`: Registry (backend, frontend-ui), Jira, Code Intelligence, Bug, Security Configuration all present. No Jira Field Defaults or Hierarchy Configuration sections |
| 2 – Discover Serena instances | Found `serena_backend`, `serena_ui`. Both are already in the Registry. "Repository Registry is up to date" |
| 3 – Jira Configuration | All required fields present. "Jira Configuration is up to date" |
| 3.5 – Hierarchy Configuration | Absent. Discovery would need Atlassian MCP calls, which are not allowed in this simulation. Not part of the requested task, so it was not scaffolded |
| 4 – Jira Field Defaults | Absent. Discovery would need Atlassian MCP calls, which are not allowed in this simulation. Not part of the requested task, so it was not scaffolded |
| 5 – Code Intelligence | Covers both instances, with Limitations. "Code Intelligence is up to date" |
| 6 – Write configuration | No CLAUDE.md changes |
| 7 / 8 – constraints.md / CONVENTIONS.md | Out of scope for this task. Not touched |
| 9 – Bug Configuration | Fully populated. "Bug Configuration is up to date" |
| 10 – Security Configuration | Fully populated, no placeholders. "Security Configuration is up to date" |
| 10.5 – Scaffold security-matrix.md | `security-matrix.md` (2.1.x) is missing. Scaffold proposed from `docs/templates/security-matrix.template.md` (not the worked example). Source columns and pinning entries expanded for backend and frontend-ui. User confirmed. Write is create-if-absent, with a re-read right before writing |
| 10.6 – Populate | User accepted. Revision checks: 2.1.0/api-rhel9 MATCH, 2.1.0/api-rhel10 MATCH, **2.1.1/api-rhel10 MISMATCH** (label `fedcba98…` vs resolved `89abcdef…`). Matrix **not populated**. Corrected evidence requested. Draft proposal shown for review only. Last-Updated not set |
| 11 – Validate | Nothing written, so there is nothing to validate beyond the existing configuration, which passes |

## Files

| File | Action |
|---|---|
| CLAUDE.md | Unchanged |
| security-matrix.md | Scaffold confirmed (create-if-absent, simulated). Population withheld pending verified evidence |
| outputs/security-matrix-review.md | Written (eval output) |
| outputs/changes-log.md | Written (eval output) |

## Open Items for the User

1. Corrected evidence for 2.1.1 / api-rhel10: the revision label does not match the resolved SHA for `v0.3.13`.
2. Is there a 2.1.1 api-rhel9 image, or did 2.1.1 ship rhel10 only?
3. The Forward Pointer value.
4. Should the Ecosystem Mappings Check Commands stay generic or be pinned to concrete refs?
