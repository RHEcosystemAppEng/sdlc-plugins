# Jira Feature Creation Parameters

## API Call Parameters

- **Endpoint**: `/rest/api/3/issue`
- **Method**: `POST`

## Request Body

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
          "attrs": { "isNumberColumnEnabled": false, "layout": "default" },
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
                { "type": "tableCell", "content": [{ "type": "paragraph", "content": [{ "type": "text", "text": "Update the existing PR review when re-running evals, or create a new review if none exists" }] }] },
                { "type": "tableCell", "content": [{ "type": "paragraph", "content": [{ "type": "text", "text": "Use PUT /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id} to update an existing review" }] }] },
                { "type": "tableCell", "content": [{ "type": "paragraph", "content": [{ "type": "text", "text": "Yes" }] }] }
              ]
            }
          ]
        }
      ]
    }
  }
}
```

## Notes

- **Project key**: TC
- **Issue type ID**: 10142 (Feature)
- **Assignee**: Unassigned (user did not specify an assignee)
- The description contains the corrected requirement language based on External API Claim Verification (the original incorrect claim about PR reviews not being updatable was corrected)
