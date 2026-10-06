# Changes Log

## What was added

The following sections were created from scratch (no prior Project Configuration existed):

### 1. Repository Registry (new)
- Added table with 2 repositories:
  - trustify-backend (Rust backend service, serena_backend, /home/user/trustify-backend)
  - trustify-ui (TypeScript frontend, serena_ui, /home/user/trustify-ui)

### 2. Jira Configuration (new)
- Project key: TC
- Cloud ID: 2b9e35e3-6bd3-4cec-b838-f4249ee02432
- Feature issue type ID: 10142
- Git Pull Request custom field: customfield_10875
- GitHub Issue custom field: customfield_10747

### 3. Code Intelligence (new)
- Tool naming convention documentation
- Example using serena_backend instance
- Limitations subsection (no limitations known)

### 4. Bug Configuration (new)
- Bug issue type ID: 10001
- Bug template: docs/bug-template.md
- Bug-to-Task link type: Blocks

### 5. Hierarchy Configuration (new)
- Default epic grouping strategy: by-sub-feature

## What was preserved

- All existing CLAUDE.md content (project title, documentation links, getting started section) is preserved and unchanged
- The Project Configuration section is appended at the end of the existing file content

## What was skipped

- **Jira Field Defaults**: Skipped because MCP auto-discovery is not available in simulation mode (cannot discover available priorities and fixVersions)
- **Security Configuration**: User declined to enable security triage
- **Constraints template copy**: Skipped (simulation)
- **CONVENTIONS.md scaffolding**: Skipped (simulation)
- **Bug template file copy**: Skipped (simulation)
