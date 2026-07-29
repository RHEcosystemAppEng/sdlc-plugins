# Validation Result -- Step 1: Bug Description Parsing

## Step 0 -- Validate Project Configuration

Configuration validated successfully from CLAUDE.md:

- **Project key**: ACME
- **Cloud ID**: mock-cloud-id-for-eval
- **Bug issue type ID**: 10020
- **Bug template path**: docs/templates/bug-template.md
- **Bug-to-Task link type**: Blocks

All required sections (Repository Registry, Jira Configuration, Code Intelligence, Bug Configuration) are present and complete.

## Step 1 -- Fetch Bug (ACME-501)

### Issue Type Validation

The issue's type ID (`10020`) matches the Bug issue type ID from Bug Configuration (`10020`). Validation passed.

### Bug Description Parsing

The bug template at `docs/templates/bug-template.md` defines the following **Required Sections**:

| Section | Heading Format |
|---------|----------------|
| Description | `### **Issue Description**` |
| Steps to reproduce | `### **Steps to Reproduce**` |
| Expected Result | `### **Expected Result**` |
| Actual Result | `### **Actual Result**` |
| Environment / Version | `### **Environment / Version**` |
| Attachments | `### **Attachments**` |

And the following **Optional Sections**:

| Section | Heading Format |
|---------|----------------|
| Root Cause | `### **Root Cause**` |
| Suggested Fix | `### **Suggested Fix**` |

#### Sections found in ACME-501 description

The bug description was parsed by matching headings against the template. The following sections were found:

1. `### **Issue Description**` -- PRESENT. Content: "The API gateway returns HTTP 500 when receiving a malformed JSON payload instead of returning a 400 Bad Request with a descriptive error message."
2. `### **Actual Result**` -- PRESENT. Content: "HTTP 500 Internal Server Error with a stack trace in the response body."
3. `### **Attachments**` -- PRESENT. Content: "None."

#### Missing required sections

Three required sections are **missing** from the bug description:

1. **Steps to Reproduce** (`### **Steps to Reproduce**`) -- not present in the description
2. **Expected Result** (`### **Expected Result**`) -- not present in the description
3. **Environment / Version** (`### **Environment / Version**`) -- not present in the description

No optional sections (Root Cause, Suggested Fix) were present either.

### Outcome

Bug ACME-501 is missing required sections: **Steps to Reproduce**, **Expected Result**, **Environment / Version**. The bug description does not follow the template at `docs/templates/bug-template.md`.

**Execution stopped.** Per the triage-bug skill specification, the skill must not attempt to investigate an incomplete bug report. The reporter must update the bug description to include all required sections before triage can proceed.

### Metadata Extracted (before halt)

Despite the parsing failure, the following metadata was extracted from the issue for completeness:

- **Issue key**: ACME-501
- **Web URL**: https://mock-jira.example.com/browse/ACME-501
- **Summary**: API returns 500 on malformed input
- **Labels**: production-incident
- **Component**: api-gateway
- **Status**: New
- **Affects Version/s**: not set
