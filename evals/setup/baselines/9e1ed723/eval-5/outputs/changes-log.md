# Changes Log — /sdlc-workflow:setup (simulated)

Target: CLAUDE.md, using `evals/setup/files/claude-md-empty.md` as input.
Mode: CLAUDE.md exists but has no `# Project Configuration`, so the section is **appended at
the end of the file**. Existing content (title, Documentation, Getting Started) is kept
unchanged. The result was written to `outputs/claude-md-result.md`. No real files were changed.

## Added

### `# Project Configuration` (new top-level section)

1. **`## Repository Registry`** (new)
   - `backend` | Rust backend service | serena_backend | /home/user/backend
   - `frontend-ui` | TypeScript frontend | serena_ui | /home/user/frontend-ui

2. **`## Jira Configuration`** (new)
   - Project key: TC
   - Cloud ID: 2b9e35e3-6bd3-4cec-b838-f4249ee02432
   - Feature issue type ID: 10142
   - Git Pull Request custom field: customfield_10875
   - GitHub Issue custom field: customfield_10747
   - **`### Jira Field Defaults`** (new, using the skill defaults): Default priority none, fixVersion scope both, Prompt for priority true, Prompt for fixVersion true

3. **`## Code Intelligence`** (new)
   - Explains the `mcp__<instance>__<tool>` naming convention
   - Gives an example call: `mcp__serena_backend__find_symbol(...)`
   - `### Limitations`: no known limitations for serena_backend or serena_ui

4. **`## Security Configuration`** (new, built from `security-config.template.md`, placed after Code Intelligence)
   - `### Product Lifecycle`:
     - Filled in: Product pages URL, Jira version prefix MYPRODUCT, Vulnerability issue type ID 10200, Component label pattern `pscomponent:`, VEX Justification field customfield_12345
     - Left blank: the remaining optional fields
   - `### Version Streams`: 2.1.x | git.downstream.example.com/my-org/product-release.2.1.z | /home/user/product-release.2.1.z | security-matrix.md
   - `### Source Repositories`:
     - backend | https://github.com/example/backend | upstream (the default)
     - frontend-ui | https://github.com/example/frontend-ui | upstream (the default)

5. **`## Bug Configuration`** (new)
   - Bug issue type ID: 10001
   - Bug template: docs/bug-template.md
   - Bug-to-Task link type: Blocks

6. **`## Hierarchy Configuration`** (new)
   - Default epic grouping strategy: none (ask each time). This is an assumption because the eval scenario gave no strategy.

## Modified

- None. No existing content was changed.

## Removed

- None.

## Skipped / Not Performed (simulation)

- MCP calls (Serena `get_diagnostics`, Atlassian metadata or link-type lookups): not performed. The user's values were used instead.
- `docs/constraints.md` copy (Step 7): not performed.
- CONVENTIONS.md scaffolding for backend and frontend-ui (Step 8): not performed.
- Bug template copy to `docs/bug-template.md` (Step 9.4): skipped, as instructed.
- `security-matrix.md` scaffolding (Step 10.5): skipped by the user.
- Supportability Matrix and Container Images population (Step 10.6): declined by the user.
