**Error: Bug Configuration is missing from CLAUDE.md**

The `report-bug` skill requires a `## Bug Configuration` section under `# Project Configuration` in your project's CLAUDE.md. This section was not found.

Bug Configuration provides the bug issue type ID, bug template path, and bug-to-task link type that the skill needs to file a bug report in Jira.

To set up the required configuration, run `/setup` to configure the project. This will add the Bug Configuration section along with the necessary fields.
