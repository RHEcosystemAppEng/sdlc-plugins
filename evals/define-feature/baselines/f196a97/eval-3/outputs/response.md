This skill requires Project Configuration in your CLAUDE.md. Please run `/setup` first to configure your project, then re-run this skill.

Your CLAUDE.md is missing the required `# Project Configuration` section. The define-feature skill needs the following subsections to operate:

- **Repository Registry** — a table listing configured repositories
- **Jira Configuration** — must include Project key, Cloud ID, and Feature issue type ID
- **Code Intelligence** — tool naming convention and Serena instance configuration

Without this configuration, the skill cannot determine which Jira project to create the Feature in or how to connect to your Jira instance. Run `/setup` to interactively configure your project, then re-run `/define-feature`.
