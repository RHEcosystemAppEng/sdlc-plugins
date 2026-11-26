# Changes Log — /sdlc-workflow:setup (eval-6)

Target: CLAUDE.md (simulated from `evals/setup/files/claude-md-configured-with-security.md`).
The result is in `outputs/claude-md-result.md`. No real files were modified.

## Added

### 1. `### Jira Field Defaults` (under `## Jira Configuration`)

```markdown
### Jira Field Defaults

- Default priority: none
- fixVersion scope: both
- Prompt for priority: true
- Prompt for fixVersion: true
```

Reason: the subsection was missing. The allowed priorities and fixVersions could not be
discovered because `getJiraIssueTypeMetaWithFields` is not in the tool listing and
MCP/Bash calls are forbidden. The values used are the SKILL.md defaults; "none" means
no priority is pre-selected. Needs user confirmation.

### 2. `## Hierarchy Configuration` (appended at the end of Project Configuration)

```markdown
## Hierarchy Configuration

- Default epic grouping strategy: none
```

Reason: the section was missing. The issue type hierarchy could not be discovered
because `getJiraProjectIssueTypesMetadata` is not in the tool listing and MCP/Bash
calls are forbidden. Chose "none" (ask each time) as the neutral option. Needs user
confirmation, and should be removed if the project has no Epic-level type.

## Preserved (no changes needed)

| Section | Status |
|---|---|
| Non-configuration content (`# backend`, `## Documentation`) | Preserved as-is |
| `## Repository Registry` | Up to date. Both discovered Serena instances (`serena_backend`, `serena_ui`) are already registered |
| `## Jira Configuration` (core + custom fields) | Up to date, values unchanged |
| `## Code Intelligence` (incl. `### Limitations`) | Up to date, covers both instances |
| `## Bug Configuration` | Up to date (10001 / docs/bug-template.md / Blocks) |
| `## Security Configuration` | **Up to date, preserved with no changes.** `### Product Lifecycle` (all 4 required fields + VEX Justification), `### Version Streams` (2.1.x row), and `### Source Repositories` (backend, frontend-ui) are copied exactly. No Security Configuration prompts were asked, and no security-matrix.md scaffolding or supportability population was done |

## Removed / Overwritten

None. No existing entries were removed or changed.

## Not Performed (needs target filesystem access, outside eval scope)

- Step 7: `docs/constraints.md` existence check and copy
- Step 8: CONVENTIONS.md scaffolding for `backend` and `frontend-ui`
- Step 9.4: bug template existence check at `docs/bug-template.md`
