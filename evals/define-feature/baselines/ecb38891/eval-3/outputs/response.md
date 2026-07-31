This skill requires Project Configuration in your CLAUDE.md. Please run `/setup` first to configure your project, then re-run this skill.

Your CLAUDE.md is missing the required `# Project Configuration` section. The define-feature skill needs the following subsections to operate:

1. **Repository Registry** -- must contain a table with at least one entry
2. **Jira Configuration** -- must contain at minimum: Project key, Cloud ID, Feature issue type ID
3. **Code Intelligence** -- must exist with the tool naming convention

Run `/sdlc-workflow:setup` to generate the Project Configuration, then re-run `/sdlc-workflow:define-feature`.
