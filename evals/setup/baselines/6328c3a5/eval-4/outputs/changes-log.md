# Setup Changes Log

## Summary

Updated Project Configuration section in CLAUDE.md based on MCP tool discovery and user input.

## Changes Made

### 1. Repository Registry: Added serena_ui entry

**Action:** Added new row to Repository Registry table.

| Field | Value |
|---|---|
| Repository | trustify-ui |
| Role | TypeScript frontend |
| Serena Instance | serena_ui |
| Path | /home/user/trustify-ui |

**Reason:** Serena instance `serena_ui` was discovered in the MCP tool listing but had no corresponding entry in the Repository Registry. User provided repository details.

### 2. Jira Field Defaults: Added section

**Action:** Added Jira Field Defaults subsection under Jira Configuration with standard defaults.

- Default priority: (none)
- fixVersion scope: both
- Prompt for priority: true
- Prompt for fixVersion: true

**Reason:** Section was missing from existing configuration. Added with standard defaults per template.

### 3. Code Intelligence: Added usage example

**Action:** Added code example showing how to invoke Serena tools using the `serena_backend` instance name.

**Reason:** Template includes a usage example to help users invoke Code Intelligence tools correctly.

### 4. Bug Configuration: Added section

**Action:** Added new Bug Configuration section.

- Bug issue type ID: 10001
- Bug template: docs/bug-template.md
- Bug-to-Task link type: Blocks

**Reason:** Bug Configuration was not present in existing configuration. Bug issue type ID discovered from Jira metadata. User accepted default template path and link type.

### 5. Hierarchy Configuration: Added section

**Action:** Added Hierarchy Configuration section with default epic grouping strategy.

- Default epic grouping strategy: by-sub-feature

**Reason:** Section was missing from existing configuration. Added with standard default.

## Preserved (No Changes)

- **Repository Registry row for trustify-backend/serena_backend:** Existing entry preserved verbatim.
- **Jira Configuration:** All existing field values preserved verbatim (project key, cloud ID, feature issue type ID, custom fields).
- **Code Intelligence body text:** Existing content preserved verbatim.
- **Limitations entries for serena_backend:** Both existing limitation entries preserved verbatim.

## Not Added

- **Security Configuration:** User declined when prompted whether to enable security triage. Section omitted per user preference.
