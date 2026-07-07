# Step 1.7 -- Embargo Check

## Configuration

Embargo policy URL is configured in Security Configuration:
- **Embargo policy URL**: https://example.com/security/embargo-policy

This step is **not skipped** because the Embargo policy URL is present.

## Severity Evaluation

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-31812 |
| CVSS Score | 7.5 |
| Severity | High |
| Threshold | >= 7.0 (Critical or Important) |
| Result | **TRIGGERS embargo warning gate** |

The CVSS score of 7.5 (High severity) meets the >= 7.0 threshold for Critical/Important severity. This is NOT a Low or Moderate CVE that would be silently skipped.

## Warning Gate

The following warning gate is presented to the engineer before proceeding to Step 2:

---

**EMBARGO CHECK -- CVE-2026-31812 (High severity, CVSS 7.5)**

High-severity vulnerabilities may be under embargo. Before proceeding, verify with your security team that this CVE is cleared for public triage.

Embargo policy: https://example.com/security/embargo-policy

Proceed with triage? (Yes / No)

---

## Gate Behavior

- If the engineer answers **"No"**: stop execution immediately. Inform the user to check embargo status with their security team before re-running triage. Do not proceed to Step 2.
- If the engineer answers **"Yes"**: proceed to Step 2 (Version Impact Analysis) as normal.

This gate fires before any triage output or Jira mutations, so stopping is safe. No data has been written to Jira at this point.

## Comparison: Low/Moderate Behavior

For reference, if the CVSS score were below 7.0 (e.g., CVSS 4.3, Moderate), this step would be **skipped silently** with no warning presented to the engineer. The embargo check only triggers for Critical or Important severity (CVSS >= 7.0).
