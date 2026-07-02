This skill requires Bug Configuration in your CLAUDE.md. Please run `/setup` first to configure your project, then re-run this skill.

Your CLAUDE.md has a **Jira Configuration** section but is missing the required **Bug Configuration** section. The `report-bug` skill needs at minimum:

- **Bug issue type ID** — the Jira issue type ID for Bug issues
- **Bug template path** — the path to the bug description template file

Run `/setup` to add the Bug Configuration section to your CLAUDE.md, then re-run `/sdlc-workflow:report-bug`.
