This skill requires Project Configuration in your CLAUDE.md. Please run `/setup` first to configure your project, then re-run this skill.

Your CLAUDE.md is missing the required `# Project Configuration` section. The define-feature skill needs the following subsections to operate:

1. `## Repository Registry` -- a table with at least one repository entry
2. `## Jira Configuration` -- containing at minimum: Project key, Cloud ID, and Feature issue type ID
3. `## Code Intelligence` -- with the tool naming convention

Without these, the skill cannot determine which Jira project to create the Feature in or how to connect to your Jira instance.

To set up your project configuration, run:

```
/sdlc-workflow:setup
```

Then re-run `/sdlc-workflow:define-feature`.
