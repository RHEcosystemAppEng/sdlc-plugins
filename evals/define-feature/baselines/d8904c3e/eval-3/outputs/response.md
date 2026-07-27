This skill requires Project Configuration in your CLAUDE.md. Please run `/setup` first to configure your project, then re-run this skill.

The following required sections are missing from your CLAUDE.md:

1. **Repository Registry** -- no `## Repository Registry` section found under `# Project Configuration`
2. **Jira Configuration** -- no `## Jira Configuration` section found (must contain at minimum: Project key, Cloud ID, Feature issue type ID)
3. **Code Intelligence** -- no `## Code Intelligence` section found

Without these sections, the define-feature skill cannot determine the Jira project key, cloud ID, or Feature issue type ID needed to create the issue.
