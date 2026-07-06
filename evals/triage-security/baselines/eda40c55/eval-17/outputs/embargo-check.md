# Step 1.7 -- Embargo Check

## Configuration

Embargo policy URL is configured in Security Configuration:
- **Embargo policy URL**: https://example.com/security/embargo-policy

Step 1.7 is not skipped because the Embargo policy URL is present.

## Severity Evaluation

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-31812 |
| CVSS score | 7.5 |
| Severity | High |
| Embargo threshold | CVSS >= 7.0 (Critical or Important) |
| Threshold met? | YES -- 7.5 >= 7.0 |

The CVSS score of 7.5 (High severity) meets the embargo trigger threshold of >= 7.0. The warning gate is triggered.

## Warning Gate Presented to Engineer

```
EMBARGO CHECK -- CVE-2026-31812 (High severity)

High-severity vulnerabilities may be under embargo.
Before proceeding, verify with your security team that this CVE
is cleared for public triage.

Embargo policy: https://example.com/security/embargo-policy

Proceed with triage? (Yes / No)
```

## Gate Behavior

- If the engineer answers **Yes**: proceed to Step 2 (Version Impact Analysis).
- If the engineer answers **No**: stop execution immediately. Inform the engineer to verify embargo status with the security team before re-running triage. Do not proceed to Step 2 or any subsequent steps.

## Decision Logic Summary

1. Embargo policy URL is configured (`https://example.com/security/embargo-policy`) -- Step 1.7 is NOT skipped.
2. CVE-2026-31812 has CVSS 7.5 (High severity), which is >= 7.0 threshold -- the gate TRIGGERS.
3. The warning gate is presented to the engineer with the CVE ID, severity level, embargo risk statement, and a link to the configured embargo policy URL.
4. The gate requires explicit Yes/No confirmation before the skill proceeds to Step 2.

Note: If the CVSS were below 7.0 (Low or Moderate severity), this step would be skipped silently and triage would proceed directly to Step 2 without any embargo warning.
