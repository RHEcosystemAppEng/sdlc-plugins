# Jira Feature Creation Request

## API Call (simulated — not executed)

**Endpoint**: `POST /rest/api/3/issue`

**Cloud ID**: 2b9e35e3-6bd3-4cec-b838-f4249ee02432

**Request Body**:

```json
{
  "fields": {
    "project": {
      "key": "TC"
    },
    "issuetype": {
      "id": "10142"
    },
    "summary": "Add automated PR review posting for eval results",
    "description": {
      "type": "doc",
      "version": 1,
      "content": [
        {
          "type": "heading",
          "attrs": { "level": 2 },
          "content": [{ "type": "text", "text": "Feature Overview" }]
        },
        {
          "type": "paragraph",
          "content": [
            {
              "type": "text",
              "text": "Add a CI workflow step that posts eval results as a PR review comment on pull requests that modify skill definitions. When a PR changes a SKILL.md file, the CI pipeline should run the corresponding eval suite and post a summary of pass/fail assertions as a PR review. This gives reviewers immediate visibility into whether skill behavior changes break existing eval expectations."
            }
          ]
        },
        {
          "type": "heading",
          "attrs": { "level": 2 },
          "content": [{ "type": "text", "text": "Requirements" }]
        },
        {
          "type": "table",
          "content": [
            {
              "type": "tableRow",
              "content": [
                { "type": "tableHeader", "content": [{ "type": "paragraph", "content": [{ "type": "text", "text": "Requirement" }] }] },
                { "type": "tableHeader", "content": [{ "type": "paragraph", "content": [{ "type": "text", "text": "Notes" }] }] },
                { "type": "tableHeader", "content": [{ "type": "paragraph", "content": [{ "type": "text", "text": "Is MVP?" }] }] }
              ]
            },
            {
              "type": "tableRow",
              "content": [
                { "type": "tableCell", "content": [{ "type": "paragraph", "content": [{ "type": "text", "text": "Post eval results as a GitHub PR review when SKILL.md files change" }] }] },
                { "type": "tableCell", "content": [{ "type": "paragraph", "content": [{ "type": "text", "text": "Use the GitHub REST API to create a review with pass/fail summary" }] }] },
                { "type": "tableCell", "content": [{ "type": "paragraph", "content": [{ "type": "text", "text": "Yes" }] }] }
              ]
            },
            {
              "type": "tableRow",
              "content": [
                { "type": "tableCell", "content": [{ "type": "paragraph", "content": [{ "type": "text", "text": "Include per-assertion results in the review body" }] }] },
                { "type": "tableCell", "content": [{ "type": "paragraph", "content": [{ "type": "text", "text": "Format as a Markdown checklist" }] }] },
                { "type": "tableCell", "content": [{ "type": "paragraph", "content": [{ "type": "text", "text": "Yes" }] }] }
              ]
            },
            {
              "type": "tableRow",
              "content": [
                { "type": "tableCell", "content": [{ "type": "paragraph", "content": [{ "type": "text", "text": "Handle the case where no evals exist for the modified skill" }] }] },
                { "type": "tableCell", "content": [{ "type": "paragraph", "content": [{ "type": "text", "text": "Post an informational comment instead of a review" }] }] },
                { "type": "tableCell", "content": [{ "type": "paragraph", "content": [{ "type": "text", "text": "Yes" }] }] }
              ]
            },
            {
              "type": "tableRow",
              "content": [
                { "type": "tableCell", "content": [{ "type": "paragraph", "content": [{ "type": "text", "text": "PR reviews cannot be updated after initial submission so always create a new review" }] }] },
                { "type": "tableCell", "content": [{ "type": "paragraph", "content": [{ "type": "text", "text": "The GitHub API does not support modifying a submitted review [UNVERIFIED CLAIM - see api-claim-verification.md]" }] }] },
                { "type": "tableCell", "content": [{ "type": "paragraph", "content": [{ "type": "text", "text": "Yes" }] }] }
              ]
            }
          ]
        }
      ]
    },
    "assignee": null
  }
}
```

**Result**: Simulated -- Jira issue not actually created. Would create Feature issue in project TC with summary "Add automated PR review posting for eval results", unassigned.
