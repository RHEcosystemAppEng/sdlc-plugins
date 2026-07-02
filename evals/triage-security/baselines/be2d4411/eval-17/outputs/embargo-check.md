# Step 1.7 -- Embargo Check

## Configuration

Embargo policy URL is configured in Security Configuration:
- **Embargo policy URL**: https://example.com/security/embargo-policy

Step 1.7 is **active** (not skipped).

## Severity Evaluation

| Parameter | Value |
|-----------|-------|
| CVE ID | CVE-2026-31812 |
| CVSS Score | 7.5 |
| Severity | High |
| Threshold | >= 7.0 (Critical/Important) |
| Meets threshold? | **YES** (7.5 >= 7.0) |

The CVSS score of 7.5 (High severity) meets the Critical/Important threshold of >= 7.0. The embargo warning gate **must be presented** to the engineer.

A Low or Moderate severity CVE (CVSS < 7.0) would NOT trigger this gate -- it would be skipped silently and triage would proceed directly to Step 2.

## Warning Gate

The following warning gate is presented to the engineer and requires explicit confirmation before proceeding:

```
WARNING: EMBARGO CHECK -- CVE-2026-31812 (High severity)

High-severity vulnerabilities may be under embargo.
Before proceeding, verify with your security team that this CVE
is cleared for public triage.

Embargo policy: https://example.com/security/embargo-policy

Proceed with triage? (Yes / No)
```

## Gate Behavior

- **If the engineer answers "Yes"**: proceed to Step 2 (Version Impact Analysis) as normal.
- **If the engineer answers "No"**: stop execution immediately. Inform the user to check embargo status with their security team before re-running triage. Do not proceed to Step 2 or any subsequent steps. No Jira mutations occur.

This gate fires before any triage output (no Jira writes have occurred yet), so stopping is safe and leaves the issue unchanged.
