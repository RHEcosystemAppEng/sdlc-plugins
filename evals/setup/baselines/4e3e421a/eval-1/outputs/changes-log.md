# Changes Log — /sdlc-workflow:setup (simulated)

The existing CLAUDE.md had no `# Project Configuration` section. Following Step 6, the
whole section was **appended at the end of the file**. No existing content was modified or removed.

## Preserved (existing content, unchanged)

- `# my-project` heading and the description line
- `## Documentation` (2 links)
- `## Getting Started` (3 steps)
- The synthetic-data HTML comment on line 1 of the input file was left out of the result because it is eval metadata, not project content.

## Added (new content)

1. `# Project Configuration` heading (new)
2. `## Repository Registry` (new): 2 rows
   - trustify-backend | Rust backend service | serena_backend | /home/user/trustify-backend
   - trustify-ui | TypeScript frontend | serena_ui | /home/user/trustify-ui
3. `## Jira Configuration` (new): Project key TC, Cloud ID, Feature issue type ID 10142,
   Git Pull Request field customfield_10875, GitHub Issue field customfield_10747
4. `### Jira Field Defaults` (new): priority none, fixVersion scope both, both prompts true.
   These are the skill defaults.
5. `## Code Intelligence` (new): the naming convention, a `serena_backend` example, and a
   `### Limitations` subsection saying no limitations are known
6. `## Bug Configuration` (new): Bug issue type ID 10001, template `docs/bug-template.md`,
   link type Blocks
7. `## Hierarchy Configuration` (new): Default epic grouping strategy `by-repository`.
   This value is an assumption (see the discovery log).

## Not added

- `## Security Configuration`: the user declined security triage
- Files outside CLAUDE.md (`docs/constraints.md`, `docs/bug-template.md`, `CONVENTIONS.md`):
  skipped because this is a simulation
