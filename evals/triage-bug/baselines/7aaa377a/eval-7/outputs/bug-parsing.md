# Bug Parsing — ACME-520 (Step 1)

## Metadata

| Field | Value |
|-------|-------|
| Issue Key | ACME-520 |
| Summary | Risk scores are computed with wrong denominator, producing inflated values |
| Issue Type | Bug (ID: 10020) |
| Status | New |
| Labels | reported-by-user |
| Component | risk-engine |
| Affects Version/s | (none — `affectsVersions` field is empty) |
| Web URL | https://mock-jira.example.com/browse/ACME-520 |

## Issue Type Validation

Bug Configuration specifies Bug issue type ID: **10020**.
The fetched issue has `issuetype.id = 10020`. Types match — proceed.

## Required Sections (from bug-template-mock.md)

All six required sections are present. No missing sections; proceed with investigation.

---

### Issue Description

The `compute_risk_score()` function in the risk engine divides by total dependencies
instead of vulnerable dependencies, producing inflated risk scores for all assessments.

---

### Steps to Reproduce

1. Ingest an SBOM with 100 total dependencies, 5 of which are vulnerable.
2. Create a risk assessment for the ingested SBOM.
3. Retrieve the risk assessment via `GET /api/v2/assessments/{id}`.
4. Inspect the `risk_score` field.

---

### Expected Result

The risk score should be `5 / 100 = 0.05` (vulnerable / total).

---

### Actual Result

The risk score is `100 / 5 = 20.0` (total / vulnerable). The numerator and
denominator are swapped.

---

### Environment / Version

Not specified.

---

### Attachments

None.

---

## Optional Sections

| Section | Present | Content |
|---------|---------|---------|
| Root Cause | No | — |
| Suggested Fix | No | — |

## Affects Version Resolution (Step 4.5 pre-check)

The `affectsVersions` field is **not populated**. The Environment / Version section
contains only "Not specified." — no version pattern can be extracted. Step 4.5 will
flag the gap and post a comment asking the reporter to set Affects Version manually.
