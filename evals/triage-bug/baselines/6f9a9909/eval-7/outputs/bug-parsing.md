# Bug Parsing: ACME-520

## Parsed Description Sections

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

## Template Conformance

All required sections from the bug template are present:

| Section | Present |
|---------|---------|
| Issue Description | Yes |
| Steps to Reproduce | Yes |
| Expected Result | Yes |
| Actual Result | Yes |
| Environment / Version | Yes (not specified) |
| Attachments | Yes (none) |

No optional sections (Root Cause, Suggested Fix) are provided.
