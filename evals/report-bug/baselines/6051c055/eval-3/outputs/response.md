## Bug Configuration Missing

This skill requires **Bug Configuration** in your project's CLAUDE.md. The current CLAUDE.md has Jira Configuration but does not include the required Bug Configuration section.

Bug Configuration must include:
- **Bug issue type ID** -- the Jira issue type ID for Bug issues
- **Bug template path** -- the path to the bug description template file
- **Bug-to-Task link type** -- the Jira link type used to connect bugs to tasks

Please run `/setup` first to configure your project's Bug Configuration, then re-run this skill.
