# Changes Log

Summary of what was preserved versus newly added during this incremental setup run.

## Repository Registry

### Preserved (unchanged)

| Repository | Role | Serena Instance | Path |
|---|---|---|---|
| trustify-backend | Rust backend service | serena_backend | /home/user/trustify-backend |

### Added

| Repository | Role | Serena Instance | Path |
|---|---|---|---|
| trustify-ui | TypeScript frontend | serena_ui | /home/user/trustify-ui |

## Jira Configuration

### Preserved (unchanged)

- Project key: TC
- Cloud ID: 2b9e35e3-6bd3-4cec-b838-f4249ee02432
- Feature issue type ID: 10142
- Git Pull Request custom field: customfield_10875
- GitHub Issue custom field: customfield_10747

### Added

No changes -- all fields were already populated.

## Jira Field Defaults

### Skipped

Jira Field Defaults subsection does not exist yet. Discovery of available priorities
and fixVersions requires Atlassian MCP (`getJiraIssueTypeMetaWithFields`), which is
not available in this simulation. No changes made.

## Code Intelligence

### Preserved (unchanged)

- Section heading and tool naming convention explanation
- Code example using `serena_backend`
- Limitation entry: `serena_backend`: rust-analyzer may take 30-60 seconds to index on first use

### Added

- Limitation entry: `serena_ui`: No limitations known

## Bug Configuration

### Preserved (unchanged)

- Bug issue type ID: 10001
- Bug template: docs/bug-template.md
- Bug-to-Task link type: Blocks

### Added

No changes -- all fields were already populated.

## Hierarchy Configuration

### Skipped

Hierarchy Configuration section does not exist yet. Discovery of issue type hierarchy
requires Atlassian MCP (`getJiraProjectIssueTypesMetadata`), which is not available
in this simulation. No changes made.

## Security Configuration

### Skipped

Security Configuration section does not exist. User was asked whether to enable
security triage and declined. No changes made.

## Summary of Changes

| Section | Status |
|---|---|
| Repository Registry | UPDATED -- added trustify-ui row |
| Jira Configuration | PRESERVED -- no changes needed |
| Jira Field Defaults | SKIPPED -- requires MCP for discovery |
| Code Intelligence | UPDATED -- added serena_ui to Limitations |
| Bug Configuration | PRESERVED -- no changes needed |
| Hierarchy Configuration | SKIPPED -- requires MCP for discovery |
| Security Configuration | SKIPPED -- user declined |
