# Step 1 -- Bug Description Parsing

## Issue Metadata

| Field | Value |
|-------|-------|
| Issue Key | ACME-520 |
| Summary | Risk scores are computed with wrong denominator, producing inflated values |
| Issue Type | Bug (ID: 10020) |
| Status | New |
| Labels | reported-by-user |
| Component | risk-engine |
| Affects Version/s | (none) |
| Web URL | https://mock-jira.example.com/browse/ACME-520 |

### Issue Type Validation

Bug issue type ID from Bug Configuration: **10020**
Issue's issuetype.id: **10020**
Result: **Match** -- issue is confirmed as a Bug.

## Bug Template Validation

Template path: `docs/templates/bug-template.md`

### Required Sections

| Section | Heading Format | Present |
|---------|----------------|---------|
| Description | `### **Issue Description**` | Yes |
| Steps to Reproduce | `### **Steps to Reproduce**` | Yes |
| Expected Result | `### **Expected Result**` | Yes |
| Actual Result | `### **Actual Result**` | Yes |
| Environment / Version | `### **Environment / Version**` | Yes |

All required sections are present.

### Optional Sections

| Section | Heading Format | Present |
|---------|----------------|---------|
| Root Cause | `### **Root Cause**` | No |
| Suggested Fix | `### **Suggested Fix**` | No |

### Attachments

Section present with value: None.

## Parsed Sections

### Issue Description

The `compute_risk_score()` function in the risk engine divides by total dependencies
instead of vulnerable dependencies, producing inflated risk scores for all assessments.

### Steps to Reproduce

1. Ingest an SBOM with 100 total dependencies, 5 of which are vulnerable.
2. Create a risk assessment for the ingested SBOM.
3. Retrieve the risk assessment via `GET /api/v2/assessments/{id}`.
4. Inspect the `risk_score` field.

### Expected Result

The risk score should be `5 / 100 = 0.05` (vulnerable / total).

### Actual Result

The risk score is `100 / 5 = 20.0` (total / vulnerable). The numerator and
denominator are swapped.

### Environment / Version

Not specified.
