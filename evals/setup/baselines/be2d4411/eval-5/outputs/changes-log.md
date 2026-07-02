# Changes Log

## What was added

All sections are newly created (greenfield project with no existing Project Configuration).

### Sections added

1. **Repository Registry** — New table with two repositories (backend, frontend-ui) mapped to their Serena instances, roles, and paths.
2. **Jira Configuration** — New section with project key (TC), cloud ID, feature issue type ID (10142), and two custom fields (Git Pull Request, GitHub Issue).
3. **Code Intelligence** — New section documenting the `mcp__<instance>__<tool>` naming convention. No limitations listed for either Serena instance.
4. **Bug Configuration** — New section with bug issue type ID (10001), default bug template path (docs/bug-template.md), and default link type (Blocks).
5. **Security Configuration** — New section (user accepted opt-in) with three subsections:
   - Product Lifecycle: all five fields populated including VEX Justification custom field
   - Version Streams: one stream (2.1.x) with Konflux release repo, local path, and security matrix path
   - Source Repositories: two repositories (backend, frontend-ui) with their URLs

## What was preserved

- No existing Project Configuration to preserve (greenfield setup).

## What was skipped

- Supportability matrix population (user declined).
- security-matrix.md scaffolding (user skipped).
