This skill requires Project Configuration in your CLAUDE.md. Please run `/setup` first to configure your project, then re-run this skill.

Your CLAUDE.md is missing the `# Project Configuration` section, which must include:

- `## Repository Registry` — a table with at least one entry
- `## Jira Configuration` — with Project key, Cloud ID, and Feature issue type ID
- `## Code Intelligence` — with the tool naming convention

These are required for the define-feature skill to create Jira issues. Run `/setup` to generate this configuration automatically.
