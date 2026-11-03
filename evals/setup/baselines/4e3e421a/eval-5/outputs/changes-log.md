# Changes Log — /sdlc-workflow:setup (simulated)

Target: CLAUDE.md (simulated from `evals/setup/files/claude-md-empty.md`)
Result written to: `outputs/claude-md-result.md`. No real project files were modified.

## Write mode

CLAUDE.md exists but has no `# Project Configuration`, so the new section was **appended at the end of the file**. Existing content (title, description, Documentation, Getting Started) is unchanged.

## Sections added

| Section | Action | Details |
|---|---|---|
| `# Project Configuration` | Added | New top-level heading |
| `## Repository Registry` | Added | 2 rows: `backend` (serena_backend, /home/user/backend) and `frontend-ui` (serena_ui, /home/user/frontend-ui) |
| `## Jira Configuration` | Added | Project key TC, Cloud ID 2b9e35e3-6bd3-4cec-b838-f4249ee02432, Feature issue type ID 10142, Git PR field customfield_10875, GitHub Issue field customfield_10747 |
| `### Jira Field Defaults` | Added | Default priority none, fixVersion scope both, prompts true/true (skill defaults) |
| `## Code Intelligence` | Added | `mcp__<instance>__<tool>` convention, example using `serena_backend`, `### Limitations` says none known |
| `## Security Configuration` | Added (after Code Intelligence) | Product Lifecycle (4 required fields plus VEX field customfield_12345; other optional fields blank), Version Streams (1 row: 2.1.x), Source Repositories (2 rows: backend, frontend-ui, both `upstream`) |
| `## Bug Configuration` | Added | Bug issue type ID 10001, template docs/bug-template.md, link type Blocks |
| `## Hierarchy Configuration` | Added | Default epic grouping strategy: by-repository (assumed; see discovery log) |

## Sections modified / removed

None. This was a greenfield setup.

## Actions skipped (simulation)

- `docs/constraints.md` copy from `constraints.template.md` (Step 7)
- CONVENTIONS.md scaffolding for `backend` / `frontend-ui` (Step 8)
- Bug template file copy to `docs/bug-template.md` (Step 9.4)
- security-matrix.md scaffolding at `security-matrix.md` (Step 10.5), skipped by the user
- Supportability Matrix / Container Images population (Step 10.6), declined by the user

## Validation (Step 11, against outputs/claude-md-result.md)

| Check | Result |
|---|---|
| `# Project Configuration` heading exists | PASS |
| Repository Registry table has columns Repository, Role, Serena Instance, Path | PASS |
| Jira Configuration has Project key, Cloud ID, Feature issue type ID | PASS |
| Jira Field Defaults has valid values | PASS |
| Code Intelligence documents the `mcp__<instance>__<tool>` convention | PASS |
| Code Intelligence has `### Limitations` | PASS |
| `docs/constraints.md` exists | N/A (copy skipped in simulation) |
| Bug Configuration has issue type ID, template path, link type | PASS |
| Bug template file exists at the configured path | N/A (copy skipped in simulation) |
| Hierarchy Configuration has Default epic grouping strategy | PASS |
| Security Configuration `### Product Lifecycle` has all 4 required fields | PASS |
| Security Configuration `### Version Streams` has at least 1 row | PASS (1) |
| Security Configuration `### Source Repositories` has at least 1 row | PASS (2) |
| No `{{placeholder}}` markers remain | PASS |
