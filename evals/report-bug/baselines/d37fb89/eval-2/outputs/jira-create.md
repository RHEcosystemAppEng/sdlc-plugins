# Jira Create Issue Parameters

- **Project key**: TC
- **Summary**: Search results pagination returns duplicate entries
- **Issue type ID**: 10300
- **Labels**: bug
- **Content format**: Atlassian Document Format (ADF)

## Description

### **Issue Description**

When paginating through search results on the SBOM list page, some
entries appear on both the current and next page. This happens
consistently when sorting by creation date descending. Approximately
10-15% of entries are duplicated across page boundaries.

### **Steps to Reproduce**

1. Ingest at least 50 SBOMs into the system
2. Navigate to the SBOM list page
3. Set sort order to "Created Date (Newest First)"
4. Scroll through pages using the pagination controls
5. Compare entries on page 2 with entries on page 1

### **Expected Result**

Each SBOM appears exactly once across all pages. No duplicates when
paginating through the full result set.

### **Actual Result**

Several SBOMs that appeared at the bottom of page 1 also appear at
the top of page 2. The total count shown in the pagination footer
is correct, but the actual displayed items exceed this count due to
duplicates.

### **Attachments**

None — the issue is reproducible with any dataset of 50+ SBOMs.

## MCP Call Format

```
mcp__jira__create_issue({
  "cloudId": "2b9e35e3-6bd3-4cec-b838-f4249ee02432",
  "projectKey": "TC",
  "issueTypeId": "10300",
  "summary": "Search results pagination returns duplicate entries",
  "labels": ["bug"],
  "descriptionAdf": {
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
          { "type": "text", "text": "When paginating through search results on the SBOM list page, some entries appear on both the current and next page. This happens consistently when sorting by creation date descending. Approximately 10-15% of entries are duplicated across page boundaries." }
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
          { "type": "listItem", "content": [{ "type": "paragraph", "content": [{ "type": "text", "text": "Ingest at least 50 SBOMs into the system" }] }] },
          { "type": "listItem", "content": [{ "type": "paragraph", "content": [{ "type": "text", "text": "Navigate to the SBOM list page" }] }] },
          { "type": "listItem", "content": [{ "type": "paragraph", "content": [{ "type": "text", "text": "Set sort order to \"Created Date (Newest First)\"" }] }] },
          { "type": "listItem", "content": [{ "type": "paragraph", "content": [{ "type": "text", "text": "Scroll through pages using the pagination controls" }] }] },
          { "type": "listItem", "content": [{ "type": "paragraph", "content": [{ "type": "text", "text": "Compare entries on page 2 with entries on page 1" }] }] }
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
          { "type": "text", "text": "Each SBOM appears exactly once across all pages. No duplicates when paginating through the full result set." }
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
          { "type": "text", "text": "Several SBOMs that appeared at the bottom of page 1 also appear at the top of page 2. The total count shown in the pagination footer is correct, but the actual displayed items exceed this count due to duplicates." }
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
        "type": "paragraph",
        "content": [
          { "type": "text", "text": "None — the issue is reproducible with any dataset of 50+ SBOMs." }
        ]
      }
    ]
  }
})
```
