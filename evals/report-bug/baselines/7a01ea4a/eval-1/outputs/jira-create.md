# Jira create_issue Call Parameters

```
createJiraIssue(
  cloudId="2b9e35e3-6bd3-4cec-b838-f4249ee02432",
  projectKey="TC",
  issueTypeId="10300",
  summary="Advisory upload fails with 500 when filename contains spaces",
  description="### **Issue Description**\n\nUploading an advisory file whose filename contains spaces causes the server to return a 500 Internal Server Error. The upload succeeds for filenames without spaces. This affects both the web UI and the REST API endpoint `POST /api/v2/advisory`. The error appears in server logs as a path-parsing failure in the ingestion pipeline.\n\n### **Steps to Reproduce**\n\n1. Log in to the Trustify web UI as any user with upload permissions\n2. Navigate to Advisories > Upload\n3. Select a file named \"my advisory 2024.json\" (note the spaces)\n4. Click the Upload button\n5. Observe the error response\n\n### **Expected Result**\n\nThe advisory file is uploaded and ingested successfully, regardless of whether the filename contains spaces. The advisory appears in the advisory list with the correct metadata.\n\n### **Actual Result**\n\nThe server returns HTTP 500 Internal Server Error. The browser shows a generic error message. The server log contains:\n\n```\nERROR trustify_module_ingestor::service: Failed to parse advisory path\n  path=\"my advisory 2024.json\"\n  error=InvalidPath: path contains unescaped spaces\n```\n\nNo advisory is created in the database.\n\n### **Environment / Version**\n\nRHTPA 1.4.2, installed via Helm on OpenShift 4.14. The issue affects the Advisory ingestion pipeline. Observed on both Firefox 128 and Chrome 126 on Fedora 40.\n\n### **Attachments**\n\n- Screenshot of the 500 error in the browser\n- Server log excerpt showing the path-parsing failure\n- Sample advisory file \"my advisory 2024.json\" used for reproduction\n\n### **Root Cause**\n\nThe ingestion pipeline passes the original filename directly to `std::path::Path::new()` without sanitizing whitespace. The custom path validator rejects paths with unescaped spaces as a safety measure, but this validation is overly strict for uploaded filenames which commonly contain spaces.\n\n### **Suggested Fix**\n\nURL-encode or sanitize the filename before passing it to the path validator. Alternatively, relax the path validator to allow spaces in uploaded filenames while still rejecting other unsafe characters. The fix should be applied in `modules/ingestor/src/service/mod.rs` in the `validate_path()` function.",
  contentFormat="markdown",
  additional_fields={ "labels": ["ai-generated-jira"] }
)
```

## Parameters Summary

| Parameter | Value |
|-----------|-------|
| Project Key | TC |
| Summary | Advisory upload fails with 500 when filename contains spaces |
| Issue Type ID | 10300 |
| Labels | ai-generated-jira |
| Content Format | markdown |
| Cloud ID | 2b9e35e3-6bd3-4cec-b838-f4249ee02432 |
