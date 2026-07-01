This skill requires Project Configuration in your CLAUDE.md. Please run `/setup` first to configure your project, then re-run this skill.

Your CLAUDE.md is missing the `# Project Configuration` section, which must include:

1. **Repository Registry** — a table with at least one entry
2. **Jira Configuration** — containing at minimum: Project key, Cloud ID, Feature issue type ID
3. **Code Intelligence** — with the tool naming convention

Without this configuration, the define-feature skill cannot determine the Jira project, issue type, or cloud instance to use.

Run `/setup` to generate the required Project Configuration, then re-run `/define-feature`.
