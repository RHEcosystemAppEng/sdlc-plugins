# Jira Create Issue Call Parameters

## API Call: `create_issue`

**Cloud ID**: `2b9e35e3-6bd3-4cec-b838-f4249ee02432`

### Parameters

| Parameter | Value |
|---|---|
| **projectKey** | `TC` |
| **issueTypeId** | `10142` |
| **summary** | `Add SBOM dependency graph visualization` |
| **labels** | `["ai-generated-jira"]` |
| **assignee** | Self (current user — `self`) |

### Description

The `description` field contains the full composed Feature description in Jira-compatible format (ADF or Markdown, depending on API), including all 9 sections:

1. Feature Overview
2. Background and Strategic Fit
3. Goals
4. Requirements
5. Non-Functional Requirements
6. Use Cases (User Experience & Workflow)
7. Customer Considerations
8. Customer Information/Supportability
9. Documentation Considerations

(Full content as shown in outputs/preview.md, starting from "## Feature Overview" through "## Documentation Considerations")

### additional_fields

```json
{
  "priority": {
    "name": "Major"
  },
  "fixVersions": [
    {
      "name": "1.5.0"
    }
  ]
}
```

### Complete Call Representation

```
mcp__jira__create_issue(
  cloud_id: "2b9e35e3-6bd3-4cec-b838-f4249ee02432",
  project_key: "TC",
  issue_type_id: "10142",
  summary: "Add SBOM dependency graph visualization",
  description: "<full Feature description with all 9 sections>",
  labels: ["ai-generated-jira"],
  assignee: "self",
  additional_fields: {
    "priority": {
      "name": "Major"
    },
    "fixVersions": [
      {
        "name": "1.5.0"
      }
    ]
  }
)
```
