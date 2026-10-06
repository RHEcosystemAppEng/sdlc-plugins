# Triage Bug: ACME-501 -- Validation Result

## Step 0: Configuration Validation

Extracted Bug Configuration from project CLAUDE.md:

| Field                  | Value                          |
|------------------------|--------------------------------|
| Project key            | ACME                           |
| Cloud ID               | mock-cloud-id-for-eval         |
| Bug issue type ID      | 10020                          |
| Bug template path      | docs/templates/bug-template.md |
| Bug-to-Task link type  | Blocks                         |

Configuration validation: **PASSED** -- all required Bug Configuration fields are present.

---

## Step 1: Fetch Bug Issue and Validate

### Issue Metadata

| Field       | Value                                              |
|-------------|----------------------------------------------------|
| Key         | ACME-501                                           |
| Summary     | API returns 500 on malformed input                 |
| Issue Type  | Bug (ID: 10020)                                    |
| Status      | New                                                |
| Labels      | production-incident                                |
| Component   | api-gateway                                        |
| Web URL     | https://mock-jira.example.com/browse/ACME-501      |

### Issue Type Validation

- Expected Bug issue type ID (from config): **10020**
- Actual issue type ID: **10020**
- Result: **PASSED** -- issue type ID 10020 matches configured Bug issue type ID 10020.

### Bug Description Parsing

Required sections defined by the bug template at `docs/templates/bug-template.md`:

| # | Required Section       | Heading Format                    | Status      |
|---|------------------------|-----------------------------------|-------------|
| 1 | Issue Description      | `### **Issue Description**`       | **FOUND**   |
| 2 | Steps to Reproduce     | `### **Steps to Reproduce**`      | **MISSING** |
| 3 | Expected Result        | `### **Expected Result**`         | **MISSING** |
| 4 | Actual Result          | `### **Actual Result**`           | **FOUND**   |
| 5 | Environment / Version  | `### **Environment / Version**`   | **MISSING** |
| 6 | Attachments            | `### **Attachments**`             | **FOUND**   |

Sections found (3 of 6): Issue Description, Actual Result, Attachments.

Sections missing (3 of 6): **Steps to Reproduce**, **Expected Result**, Environment / Version.

### Validation Result: FAILED

Bug ACME-501 is missing required sections: Steps to Reproduce, Expected Result. The bug description does not follow the template at docs/templates/bug-template.md.

**Execution stopped at Step 1** due to bug description validation failure. The bug issue does not conform to the required template and cannot be triaged until the missing sections are provided.

---

## Steps NOT Executed

The following steps were **not executed** because validation failed in Step 1:

- **Step 2**: Not executed -- Identify affected component and owning repository
- **Step 3**: Not executed -- Reproduce and gather code intelligence
- **Step 4**: Not executed -- Severity and priority assessment
- **Step 5**: Not executed -- Create linked implementation task(s)
- **Step 6**: Not executed -- Update bug issue with triage results
- **Step 7**: Not executed -- Summary and next steps
