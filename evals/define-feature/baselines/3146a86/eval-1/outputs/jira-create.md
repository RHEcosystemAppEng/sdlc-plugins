# Jira Create Issue Parameters

The following parameters would be passed to `createJiraIssue`:

```
cloudId: 2b9e35e3-6bd3-4cec-b838-f4249ee02432
projectKey: TC
issueTypeId: 10142
summary: Add SBOM dependency graph visualization
description: <composed Feature description from preview>
contentFormat: markdown
additional_fields:
  labels: ["ai-generated-jira"]
  assignee:
    accountId: "<current-user-account-id>"
```

## Parameter Details

| Parameter | Value |
|---|---|
| `cloudId` | `2b9e35e3-6bd3-4cec-b838-f4249ee02432` |
| `projectKey` | `TC` |
| `issueTypeId` | `10142` |
| `summary` | `Add SBOM dependency graph visualization` |
| `description` | Full composed description (all 9 sections, see preview.md) |
| `contentFormat` | `markdown` |
| `labels` | `["ai-generated-jira"]` |
| `assignee` | Self-assigned -- `{ "accountId": "<current-user-account-id>" }` (retrieved via `atlassianUserInfo()`) |

## Notes

- The user chose self-assignment, so the `assignee` field is included with the user's `accountId` (retrieved from `atlassianUserInfo()` at runtime).
- The `description` field contains the full Markdown-formatted Feature description with all 9 sections as composed in the preview.
- The `contentFormat` is set to `markdown` so Jira converts the Markdown description to ADF for storage.
