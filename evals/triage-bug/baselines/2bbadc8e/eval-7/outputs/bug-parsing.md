# Step 1 -- Bug Parsing: ACME-520

## Metadata

- **Issue Key**: ACME-520
- **Web URL**: https://mock-jira.example.com/browse/ACME-520
- **Summary**: Risk scores are computed with wrong denominator, producing inflated values
- **Issue Type**: Bug (ID: 10020)
- **Status**: New
- **Labels**: reported-by-user
- **Component**: risk-engine
- **Affects Version/s**: (none) -- not populated

## Configuration Validation (Step 0)

Extracted from CLAUDE.md (`claude-md-bug-config.md`):

- **Project key**: ACME
- **Cloud ID**: mock-cloud-id-for-eval
- **Bug issue type ID**: 10020
- **Bug template path**: docs/templates/bug-template.md
- **Bug-to-Task link type**: Blocks

Issue type validation: Issue type ID `10020` matches Bug Configuration's Bug issue type ID `10020`. Confirmed as Bug.

## Bug Template Sections

Template file (`bug-template-mock.md`) defines the following section heading formats:

### Required Sections

| Section | Heading Format | Present in ACME-520 |
|---------|----------------|---------------------|
| Description | `### **Issue Description**` | Yes |
| Steps to reproduce | `### **Steps to Reproduce**` | Yes |
| Expected Result | `### **Expected Result**` | Yes |
| Actual Result | `### **Actual Result**` | Yes |
| Environment / Version | `### **Environment / Version**` | Yes |
| Attachments | `### **Attachments**` | Yes |

### Optional Sections

| Section | Heading Format | Present in ACME-520 |
|---------|----------------|---------------------|
| Root Cause | `### **Root Cause**` | No |
| Suggested Fix | `### **Suggested Fix**` | No |

All required sections are present. No missing sections.

## Parsed Required Sections

### Issue Description

The `compute_risk_score()` function in the risk engine divides by total dependencies instead of vulnerable dependencies, producing inflated risk scores for all assessments.

### Steps to Reproduce

1. Ingest an SBOM with 100 total dependencies, 5 of which are vulnerable.
2. Create a risk assessment for the ingested SBOM.
3. Retrieve the risk assessment via `GET /api/v2/assessments/{id}`.
4. Inspect the `risk_score` field.

### Expected Result

The risk score should be `5 / 100 = 0.05` (vulnerable / total).

### Actual Result

The risk score is `100 / 5 = 20.0` (total / vulnerable). The numerator and denominator are swapped.

### Environment / Version

Not specified.

### Attachments

None.

## Parsed Optional Sections

No optional sections (Root Cause, Suggested Fix) are present in the bug description.
