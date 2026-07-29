# Step 1 -- Bug Parsing: ACME-520

## Configuration (Step 0)

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
- **Affects Version/s**: (none) -- field is not populated

## Parsed Required Sections

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

### Attachments

None.

## Parsed Optional Sections

- **Root Cause**: Not present in description.
- **Suggested Fix**: Not present in description.

## Validation Result

All required sections are present. Bug description conforms to the template at
`docs/templates/bug-template.md`. Proceeding with investigation.
