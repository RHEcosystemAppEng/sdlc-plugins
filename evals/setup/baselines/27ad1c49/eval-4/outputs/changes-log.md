# Changes Log

## Preserved Entries

The following existing configuration was preserved without modification:

- **Repository Registry**: The existing `trustify-backend` entry (including its repository name, role, Serena instance, and path fields) was preserved verbatim.
- **Jira Configuration**: All existing Jira fields (Project key, Cloud ID, Feature issue type ID, Git Pull Request custom field, GitHub Issue custom field) were preserved verbatim.
- **Code Intelligence**: The existing Code Intelligence section text was preserved verbatim.
- **Limitations**: Both existing limitation entries for `serena_backend` were preserved verbatim.

## New Entries Added

- **Repository Registry**: Added `trustify-ui` row -- repository `trustify-ui`, role `TypeScript frontend`, Serena instance `serena_ui`, path `/home/user/trustify-ui`. This was discovered from the MCP tool listing which showed a `serena_ui` instance.
- **Bug Configuration**: Added a new Bug Configuration section with Bug issue type ID `10001`, bug template path `docs/bug-template.md`, and Bug-to-Task link type `Blocks`.

## Sections Not Added

- **Security Configuration**: The user was offered security triage configuration but declined. No Security Configuration section was added.
