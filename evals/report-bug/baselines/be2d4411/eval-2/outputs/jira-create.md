# Jira create_issue Call Parameters

- **Tool**: `mcp__jira__create_issue`
- **Project key**: `TC`
- **Issue type ID**: `10300`
- **Summary**: `Search results pagination returns duplicate entries`
- **Labels**: `["ai-generated-jira"]`
- **Description**: *(contents of preview.md)*

```json
{
  "project_key": "TC",
  "issue_type_id": "10300",
  "summary": "Search results pagination returns duplicate entries",
  "description": "### **Issue Description**\n\nWhen paginating through search results on the SBOM list page, some\nentries appear on both the current and next page. This happens\nconsistently when sorting by creation date descending. Approximately\n10-15% of entries are duplicated across page boundaries.\n\n### **Steps to Reproduce**\n\n1. Ingest at least 50 SBOMs into the system\n2. Navigate to the SBOM list page\n3. Set sort order to \"Created Date (Newest First)\"\n4. Scroll through pages using the pagination controls\n5. Compare entries on page 2 with entries on page 1\n\n### **Expected Result**\n\nEach SBOM appears exactly once across all pages. No duplicates when\npaginating through the full result set.\n\n### **Actual Result**\n\nSeveral SBOMs that appeared at the bottom of page 1 also appear at\nthe top of page 2. The total count shown in the pagination footer\nis correct, but the actual displayed items exceed this count due to\nduplicates.\n\n### **Attachments**\n\nNone — the issue is reproducible with any dataset of 50+ SBOMs.",
  "labels": ["ai-generated-jira"]
}
```
