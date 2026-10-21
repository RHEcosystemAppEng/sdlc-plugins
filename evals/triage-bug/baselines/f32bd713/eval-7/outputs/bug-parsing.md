# Step 1 -- Bug Parsing: ACME-520

## Configuration Validated (Step 0)

- **Project key**: ACME
- **Cloud ID**: mock-cloud-id-for-eval
- **Bug issue type ID**: 10020
- **Bug template path**: docs/templates/bug-template.md
- **Bug-to-Task link type**: Blocks

## Issue Metadata

- **Issue key**: ACME-520
- **Web URL**: https://mock-jira.example.com/browse/ACME-520
- **Summary**: Risk scores are computed with wrong denominator, producing inflated values
- **Issue Type**: Bug (ID: 10020) -- matches Bug Configuration
- **Status**: New
- **Labels**: reported-by-user
- **Component**: risk-engine
- **Affects Version/s**: (none) -- not populated

## Parsed Description Sections

### Required Sections

All required sections are present per the bug template at `docs/templates/bug-template.md`.

#### Issue Description (`### **Issue Description**`)

The `compute_risk_score()` function in the risk engine divides by total dependencies
instead of vulnerable dependencies, producing inflated risk scores for all assessments.

#### Steps to Reproduce (`### **Steps to Reproduce**`)

1. Ingest an SBOM with 100 total dependencies, 5 of which are vulnerable.
2. Create a risk assessment for the ingested SBOM.
3. Retrieve the risk assessment via `GET /api/v2/assessments/{id}`.
4. Inspect the `risk_score` field.

#### Expected Result (`### **Expected Result**`)

The risk score should be `5 / 100 = 0.05` (vulnerable / total).

#### Actual Result (`### **Actual Result**`)

The risk score is `100 / 5 = 20.0` (total / vulnerable). The numerator and
denominator are swapped.

#### Environment / Version (`### **Environment / Version**`)

Not specified.

#### Attachments (`### **Attachments**`)

None.

### Optional Sections

- **Root Cause**: not provided by reporter
- **Suggested Fix**: not provided by reporter

## Validation Result

All required sections are present. Proceeding to Step 2.
