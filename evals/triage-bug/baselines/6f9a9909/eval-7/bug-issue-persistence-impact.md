<!-- SYNTHETIC TEST DATA — Bug issue where buggy output is persisted to database, for triage-bug persistence-impact eval testing -->

# Mock Jira Bug Issue

**Key**: ACME-520
**Summary**: Risk scores are computed with wrong denominator, producing inflated values
**Issue Type**: Bug (ID: 10020)
**Status**: New
**Labels**: reported-by-user
**Component**: risk-engine
**Affects Version/s**: (none)
**Web URL**: https://mock-jira.example.com/browse/ACME-520

---

## Description

### **Issue Description**

The `compute_risk_score()` function in the risk engine divides by total dependencies
instead of vulnerable dependencies, producing inflated risk scores for all assessments.

### **Steps to Reproduce**

1. Ingest an SBOM with 100 total dependencies, 5 of which are vulnerable.
2. Create a risk assessment for the ingested SBOM.
3. Retrieve the risk assessment via `GET /api/v2/assessments/{id}`.
4. Inspect the `risk_score` field.

### **Expected Result**

The risk score should be `5 / 100 = 0.05` (vulnerable / total).

### **Actual Result**

The risk score is `100 / 5 = 20.0` (total / vulnerable). The numerator and
denominator are swapped.

### **Environment / Version**

Not specified.

### **Attachments**

None.
