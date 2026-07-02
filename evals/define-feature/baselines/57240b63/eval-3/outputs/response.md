This skill requires Project Configuration in your CLAUDE.md. Please run `/setup` first to configure your project, then re-run this skill.

Your CLAUDE.md is missing the required `# Project Configuration` section, which must include:

1. **Repository Registry** -- a table with at least one repository entry
2. **Jira Configuration** -- containing the Project key, Cloud ID, and Feature issue type ID
3. **Code Intelligence** -- with the tool naming convention

Without these, the define-feature skill cannot determine which Jira project to create the Feature in or how to connect to your Jira instance.

Run `/setup` to generate the Project Configuration, then re-run `/sdlc-workflow:define-feature`.
