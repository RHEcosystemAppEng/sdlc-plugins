# Jira Create Issue Call

## Tool Call

```
mcp__jira__create_issue(
  projectKey: "TC",
  issueTypeId: "10142",
  summary: "Add bulk SBOM delete endpoint",
  description: "<full feature description>",
  labels: ["ai-generated-jira"],
  additional_fields: {
    "priority": {"name": "Normal"}
  }
)
```

## Parameters

- **projectKey:** TC
- **issueTypeId:** 10142
- **summary:** Add bulk SBOM delete endpoint
- **labels:** ["ai-generated-jira"]
- **assignee:** (not set — omitted from call)
- **priority:** {"name": "Normal"} (default applied silently from Jira Field Defaults)
- **fixVersions:** (not set — omitted from call; no default configured, prompt suppressed)

## Notes

- Priority "Normal" was applied from the `Default priority: Normal` setting in CLAUDE.md `### Jira Field Defaults` without prompting the user (`Prompt for priority: false`).
- fixVersions is omitted entirely because no `Default fixVersion` is configured and `Prompt for fixVersion: false` suppresses the prompt, so no value is available.
- Assignee is omitted because the user left the feature unassigned.
