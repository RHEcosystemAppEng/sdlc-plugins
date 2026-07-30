This skill requires Project Configuration in your CLAUDE.md. Please run `/setup` first to configure your project, then re-run this skill.

Your CLAUDE.md is missing the `# Project Configuration` section, which must include:

- `## Repository Registry` — a table with at least one repository entry
- `## Jira Configuration` — containing Project key, Cloud ID, and Feature issue type ID
- `## Code Intelligence` — with the tool naming convention

Without these sections, the skill cannot determine the Jira project, issue type, or cloud instance to use.
