**Project Configuration is missing from CLAUDE.md.**

The `define-feature` skill requires a `# Project Configuration` section in your project's CLAUDE.md with the following subsections:

- **Repository Registry** -- maps repositories and their roles
- **Jira Configuration** -- project key, cloud ID, issue type IDs, and custom field mappings
- **Code Intelligence** -- Serena instance configuration for code analysis

Without this configuration, the skill cannot determine which Jira project to create the feature in or how to map fields correctly.

Please run `/setup` first to configure your project, then re-run `/define-feature`.
