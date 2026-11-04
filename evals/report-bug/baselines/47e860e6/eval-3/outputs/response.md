# report-bug — Step 0: Validate Project Configuration

I checked the project's CLAUDE.md (`claude-md-missing-bug-config.md`) for the configuration this skill needs:

| Required Section | Status |
|---|---|
| `## Repository Registry` | Present (1 entry: trustify-backend) |
| `## Jira Configuration` (Project key, Cloud ID) | Present (Project key: TC, Cloud ID: 2b9e35e3-6bd3-4cec-b838-f4249ee02432) |
| `## Bug Configuration` (Bug issue type ID, Bug template path) | **Missing** |

The `## Bug Configuration` section is missing under `# Project Configuration`. That means there is no **Bug issue type ID** and no **Bug template path**.

This skill requires Bug Configuration in your CLAUDE.md. Please run `/setup` first to configure your project, then re-run this skill.

**Execution stopped.** I did not create a Jira issue, post a comment, or try to fill in the missing configuration myself.
