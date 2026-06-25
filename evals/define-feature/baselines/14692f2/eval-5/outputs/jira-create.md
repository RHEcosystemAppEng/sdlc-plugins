# Jira Create Issue Parameters

The following parameters would be passed to `createJiraIssue`:

```
createJiraIssue(
  cloudId = "2b9e35e3-6bd3-4cec-b838-f4249ee02432",
  projectKey = "TC",
  issueTypeId = "10142",
  summary = "Add automated PR review posting for eval results",
  description = <composed-description-from-preview>,
  contentFormat = "markdown",
  additional_fields = {
    "labels": ["ai-generated-jira"]
  }
)
```

## Parameter Details

| Parameter | Value | Source |
|---|---|---|
| cloudId | `2b9e35e3-6bd3-4cec-b838-f4249ee02432` | CLAUDE.md Jira Configuration |
| projectKey | `TC` | CLAUDE.md Jira Configuration |
| issueTypeId | `10142` | CLAUDE.md Jira Configuration (Feature issue type ID) |
| summary | `Add automated PR review posting for eval results` | User input |
| contentFormat | `markdown` | Skill default |
| labels | `["ai-generated-jira"]` | Skill default |
| assignee | _(omitted -- user left Feature unassigned)_ | User choice |
| priority | _(omitted -- not set)_ | User skipped |
| fixVersions | _(omitted -- not set)_ | User skipped |

## Description Content

The description field contains the composed Markdown from the preview, including only the non-skipped sections:

- **Feature Overview** -- included
- **Requirements** -- included (with corrected API claim language)
- Background and Strategic Fit -- SKIPPED (omitted)
- Goals -- SKIPPED (omitted)
- Non-Functional Requirements -- SKIPPED (omitted)
- Use Cases -- SKIPPED (omitted)
- Customer Considerations -- SKIPPED (omitted)
- Customer Information/Supportability -- SKIPPED (omitted)
- Documentation Considerations -- SKIPPED (omitted)
