# Changes Log — /sdlc-workflow:setup (simulated)

Target: CLAUDE.md (input: `evals/setup/files/claude-md-empty.md`)
Mode: CLAUDE.md exists but has no `# Project Configuration` → section appended at end of file. All existing content (`# my-project`, `## Documentation`, `## Getting Started`) preserved unchanged.

## Added

1. `# Project Configuration` heading (new).
2. `## Repository Registry` — empty table, headers only (`Repository | Role | Serena Instance | Path`), because no Serena instances were found and the user chose to continue without code intelligence.
3. `## Jira Configuration` (manual entry):
   - Project key: MYPROJ
   - Cloud ID: abc123
   - Feature issue type ID: 10001
   - Git Pull Request / GitHub Issue custom fields: not configured (user has none) — lines omitted.
4. `### Jira Field Defaults` (under Jira Configuration) — default values: priority none, fixVersion scope both, prompt for priority true, prompt for fixVersion true.
5. `## Code Intelligence` — naming convention `mcp__<instance>__<tool>`, generic example, note that no Serena servers are configured; `### Limitations` with "No limitations known".
6. `## Bug Configuration`:
   - Bug issue type ID: 10001
   - Bug template: docs/bug-template.md
   - Bug-to-Task link type: Blocks

## Not Added / Skipped

- `## Hierarchy Configuration` — not created: issue type hierarchy could not be discovered (no Atlassian MCP, REST fallback declined) and no Epic-level type was confirmed.
- `## Security Configuration` — user declined security triage.
- `docs/constraints.md` — would be created from `constraints.template.md` if absent; not written (simulation, no real file modifications).
- `CONVENTIONS.md` — no repositories in the Repository Registry; nothing to scaffold.
- Bug template file copy to `docs/bug-template.md` — skipped per simulation instructions.

## Files Actually Written

- `/tmp/setup-eval-baseline/eval-3/outputs/claude-md-result.md`
- `/tmp/setup-eval-baseline/eval-3/outputs/discovery-log.md`
- `/tmp/setup-eval-baseline/eval-3/outputs/changes-log.md`

No repository files modified, no MCP tools called, no Bash commands run.

## Step 11 – Validation (against claude-md-result.md)

- [x] `# Project Configuration` heading exists
- [x] `## Repository Registry` table with columns Repository, Role, Serena Instance, Path
- [x] `## Jira Configuration` has Project key, Cloud ID, Feature issue type ID
- [x] `### Jira Field Defaults` has valid values
- [x] `## Code Intelligence` documents `mcp__<instance>__<tool>`
- [x] `## Code Intelligence` has `### Limitations`
- [ ] `docs/constraints.md` exists — not verified (simulation)
- [x] `## Bug Configuration` has Bug issue type ID, Bug template path, Bug-to-Task link type
- [ ] Bug template file exists at `docs/bug-template.md` — copy skipped (simulation)
- n/a `## Hierarchy Configuration` — not scaffolded
- n/a `## Security Configuration` — declined
