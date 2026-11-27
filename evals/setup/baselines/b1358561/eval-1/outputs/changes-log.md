# Changes Log — /sdlc-workflow:setup (simulated)

## Preserved (unchanged)

- HTML comment header line
- `# my-project` heading and description
- `## Documentation` section (both links)
- `## Getting Started` section (3 steps)

## Added (appended at end of file, since no `# Project Configuration` existed)

- `# Project Configuration`
  - `## Repository Registry` — 2 rows: trustify-backend (serena_backend), trustify-ui (serena_ui)
  - `## Jira Configuration` — Project key TC, Cloud ID, Feature issue type ID 10142,
    Git Pull Request custom field customfield_10875, GitHub Issue custom field customfield_10747
    - `### Jira Field Defaults` — none / both / true / true (skill defaults)
  - `## Code Intelligence` — `mcp__<instance>__<tool>` convention, `serena_backend` example,
    `### Limitations` (no known limitations)
  - `## Bug Configuration` — Bug issue type ID 10001, template `docs/bug-template.md`, link type Blocks

## Not added

- `## Security Configuration` — user declined security triage.
- `## Hierarchy Configuration` — issue type hierarchy/grouping strategy not available in the
  simulation; left for a later run.

## Removed / Overwritten

- None.

## Other files (skipped in simulation)

- `docs/constraints.md` — would be created from template if absent.
- `docs/bug-template.md` — copy skipped per instructions.
- `CONVENTIONS.md` in trustify-backend / trustify-ui — scaffolding not performed.
