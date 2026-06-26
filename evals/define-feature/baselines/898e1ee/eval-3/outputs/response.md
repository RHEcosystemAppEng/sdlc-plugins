**Execution stopped — missing Project Configuration.**

The CLAUDE.md for this repository does not contain a Project Configuration section. The define-feature skill requires a fully populated Project Configuration with the following subsections:

- **Repository Registry** — maps repositories, roles, and Serena instances
- **Jira Configuration** — provides the project key, cloud ID, issue type IDs, and custom field mappings
- **Code Intelligence** — declares Serena MCP server availability and known limitations

Without this configuration, the skill cannot determine the Jira project, issue type, or custom fields needed to create a Feature.

**Recommended next step:** Run `/setup` to generate the Project Configuration section in your CLAUDE.md before retrying `/define-feature`.
