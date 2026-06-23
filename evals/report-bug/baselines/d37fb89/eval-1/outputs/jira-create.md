## Jira Create Issue Parameters

- **Project key:** TC
- **Summary:** Advisory upload fails with 500 when filename contains spaces
- **Issue type ID:** 10300
- **Labels:** bug
- **Content format:** Atlassian Document Format (ADF)

## Description

### **Issue Description**

Uploading an advisory file whose filename contains spaces causes the
server to return a 500 Internal Server Error. The upload succeeds for
filenames without spaces. This affects both the web UI and the REST API
endpoint `POST /api/v2/advisory`. The error appears in server logs as a
path-parsing failure in the ingestion pipeline.

### **Steps to Reproduce**

1. Log in to the Trustify web UI as any user with upload permissions
2. Navigate to Advisories > Upload
3. Select a file named "my advisory 2024.json" (note the spaces)
4. Click the Upload button
5. Observe the error response

### **Expected Result**

The advisory file is uploaded and ingested successfully, regardless of
whether the filename contains spaces. The advisory appears in the
advisory list with the correct metadata.

### **Actual Result**

The server returns HTTP 500 Internal Server Error. The browser shows a
generic error message. The server log contains:

```
ERROR trustify_module_ingestor::service: Failed to parse advisory path
  path="my advisory 2024.json"
  error=InvalidPath: path contains unescaped spaces
```

No advisory is created in the database.

### **Attachments**

- Screenshot of the 500 error in the browser
- Server log excerpt showing the path-parsing failure
- Sample advisory file "my advisory 2024.json" used for reproduction

### **Root Cause**

The ingestion pipeline passes the original filename directly to
`std::path::Path::new()` without sanitizing whitespace. The custom path
validator rejects paths with unescaped spaces as a safety measure, but
this validation is overly strict for uploaded filenames which commonly
contain spaces.

### **Suggested Fix**

URL-encode or sanitize the filename before passing it to the path
validator. Alternatively, relax the path validator to allow spaces in
uploaded filenames while still rejecting other unsafe characters. The
fix should be applied in `modules/ingestor/src/service/mod.rs` in the
`validate_path()` function.

## MCP Call

```json
mcp__jira__createJiraIssue({
  "cloudId": "2b9e35e3-6bd3-4cec-b838-f4249ee02432",
  "projectKey": "TC",
  "summary": "Advisory upload fails with 500 when filename contains spaces",
  "issueTypeId": "10300",
  "labels": ["bug"],
  "description": {
    "version": 1,
    "type": "doc",
    "content": [
      {
        "type": "heading",
        "attrs": { "level": 3 },
        "content": [
          { "type": "text", "text": "Issue Description", "marks": [{ "type": "strong" }] }
        ]
      },
      {
        "type": "paragraph",
        "content": [
          { "type": "text", "text": "Uploading an advisory file whose filename contains spaces causes the server to return a 500 Internal Server Error. The upload succeeds for filenames without spaces. This affects both the web UI and the REST API endpoint POST /api/v2/advisory. The error appears in server logs as a path-parsing failure in the ingestion pipeline." }
        ]
      },
      {
        "type": "heading",
        "attrs": { "level": 3 },
        "content": [
          { "type": "text", "text": "Steps to Reproduce", "marks": [{ "type": "strong" }] }
        ]
      },
      {
        "type": "orderedList",
        "attrs": { "order": 1 },
        "content": [
          { "type": "listItem", "content": [{ "type": "paragraph", "content": [{ "type": "text", "text": "Log in to the Trustify web UI as any user with upload permissions" }] }] },
          { "type": "listItem", "content": [{ "type": "paragraph", "content": [{ "type": "text", "text": "Navigate to Advisories > Upload" }] }] },
          { "type": "listItem", "content": [{ "type": "paragraph", "content": [{ "type": "text", "text": "Select a file named \"my advisory 2024.json\" (note the spaces)" }] }] },
          { "type": "listItem", "content": [{ "type": "paragraph", "content": [{ "type": "text", "text": "Click the Upload button" }] }] },
          { "type": "listItem", "content": [{ "type": "paragraph", "content": [{ "type": "text", "text": "Observe the error response" }] }] }
        ]
      },
      {
        "type": "heading",
        "attrs": { "level": 3 },
        "content": [
          { "type": "text", "text": "Expected Result", "marks": [{ "type": "strong" }] }
        ]
      },
      {
        "type": "paragraph",
        "content": [
          { "type": "text", "text": "The advisory file is uploaded and ingested successfully, regardless of whether the filename contains spaces. The advisory appears in the advisory list with the correct metadata." }
        ]
      },
      {
        "type": "heading",
        "attrs": { "level": 3 },
        "content": [
          { "type": "text", "text": "Actual Result", "marks": [{ "type": "strong" }] }
        ]
      },
      {
        "type": "paragraph",
        "content": [
          { "type": "text", "text": "The server returns HTTP 500 Internal Server Error. The browser shows a generic error message. The server log contains:" }
        ]
      },
      {
        "type": "codeBlock",
        "attrs": {},
        "content": [
          { "type": "text", "text": "ERROR trustify_module_ingestor::service: Failed to parse advisory path\n  path=\"my advisory 2024.json\"\n  error=InvalidPath: path contains unescaped spaces" }
        ]
      },
      {
        "type": "paragraph",
        "content": [
          { "type": "text", "text": "No advisory is created in the database." }
        ]
      },
      {
        "type": "heading",
        "attrs": { "level": 3 },
        "content": [
          { "type": "text", "text": "Attachments", "marks": [{ "type": "strong" }] }
        ]
      },
      {
        "type": "bulletList",
        "content": [
          { "type": "listItem", "content": [{ "type": "paragraph", "content": [{ "type": "text", "text": "Screenshot of the 500 error in the browser" }] }] },
          { "type": "listItem", "content": [{ "type": "paragraph", "content": [{ "type": "text", "text": "Server log excerpt showing the path-parsing failure" }] }] },
          { "type": "listItem", "content": [{ "type": "paragraph", "content": [{ "type": "text", "text": "Sample advisory file \"my advisory 2024.json\" used for reproduction" }] }] }
        ]
      },
      {
        "type": "heading",
        "attrs": { "level": 3 },
        "content": [
          { "type": "text", "text": "Root Cause", "marks": [{ "type": "strong" }] }
        ]
      },
      {
        "type": "paragraph",
        "content": [
          { "type": "text", "text": "The ingestion pipeline passes the original filename directly to std::path::Path::new() without sanitizing whitespace. The custom path validator rejects paths with unescaped spaces as a safety measure, but this validation is overly strict for uploaded filenames which commonly contain spaces." }
        ]
      },
      {
        "type": "heading",
        "attrs": { "level": 3 },
        "content": [
          { "type": "text", "text": "Suggested Fix", "marks": [{ "type": "strong" }] }
        ]
      },
      {
        "type": "paragraph",
        "content": [
          { "type": "text", "text": "URL-encode or sanitize the filename before passing it to the path validator. Alternatively, relax the path validator to allow spaces in uploaded filenames while still rejecting other unsafe characters. The fix should be applied in modules/ingestor/src/service/mod.rs in the validate_path() function." }
        ]
      }
    ]
  }
})
```
