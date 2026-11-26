# Changes Log — /sdlc-workflow:setup (simulated)

Target: CLAUDE.md (input: `evals/setup/files/claude-md-empty.md`)
Write strategy: CLAUDE.md exists with no `# Project Configuration`, so the section was appended
at the end of the file (Step 6). Result written to `outputs/claude-md-result.md`.

## Preserved (unchanged)

- The leading HTML comment (synthetic test data marker)
- `# my-project` heading and description ("A web application for managing inventory.")
- `## Documentation` (links to docs/architecture.md and docs/api.md)
- `## Getting Started` (3 steps)

Nothing was removed or modified.

## Added

- `# Project Configuration` (new top-level section, appended)
  - `## Repository Registry`, 2 rows:
    - trustify-backend | Rust backend service | serena_backend | /home/user/trustify-backend
    - trustify-ui | TypeScript frontend | serena_ui | /home/user/trustify-ui
  - `## Jira Configuration`: Project key TC, Cloud ID 2b9e35e3-6bd3-4cec-b838-f4249ee02432,
    Feature issue type ID 10142, Git Pull Request custom field customfield_10875,
    GitHub Issue custom field customfield_10747
    - `### Jira Field Defaults`: Default priority none, fixVersion scope both,
      Prompt for priority true, Prompt for fixVersion true (skill defaults)
  - `## Code Intelligence`: `mcp__<instance>__<tool>` naming convention, a `find_symbol` example
    using `serena_backend`, and `### Limitations` (none known for either instance)
  - `## Bug Configuration`: Bug issue type ID 10001, Bug template docs/bug-template.md,
    Bug-to-Task link type Blocks

## Not added (intentionally)

- `## Security Configuration`: user declined security triage (Step 10).
- `## Hierarchy Configuration`: no issue type hierarchy data was available in this simulation, so no
  Epic-level type could be confirmed and no grouping strategy was chosen (Step 3.5).

## Other file operations (skipped in simulation)

- `docs/constraints.md` copy from `constraints.template.md`: skipped (only writing to outputs/).
- `CONVENTIONS.md` scaffolding for trustify-backend / trustify-ui: skipped.
- Bug template copy to `docs/bug-template.md`: skipped as instructed.

## Validation (Step 11, against outputs/claude-md-result.md)

- [x] `# Project Configuration` heading exists
- [x] `## Repository Registry` table has columns Repository, Role, Serena Instance, Path
- [x] `## Jira Configuration` has Project key, Cloud ID, Feature issue type ID
- [x] `### Jira Field Defaults` has valid values
- [x] `## Code Intelligence` documents `mcp__<instance>__<tool>`
- [x] `## Code Intelligence` has `### Limitations`
- [x] `## Bug Configuration` has Bug issue type ID, Bug template path, Bug-to-Task link type
- [ ] `docs/constraints.md` exists: not checked (copy skipped in simulation)
- [ ] Bug template file exists at configured path: not checked (copy skipped in simulation)
- [n/a] Security Configuration: not scaffolded (declined)
- [n/a] Hierarchy Configuration: not scaffolded
