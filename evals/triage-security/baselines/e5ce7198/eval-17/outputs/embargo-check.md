# Step 1.7 -- Embargo Check: CVE-2026-31812

## Configuration Check

Embargo policy URL is configured in Security Configuration:
- **Embargo policy URL**: https://example.com/security/embargo-policy

Embargo check is **active** (URL is configured).

## Severity Evaluation

| Attribute | Value |
|-----------|-------|
| CVE ID | CVE-2026-31812 |
| CVSS Score | 7.5 |
| Severity Level | High |
| Embargo Threshold | CVSS >= 7.0 (Critical or Important) |
| Threshold Met? | **YES** -- 7.5 >= 7.0 |

The CVE severity (High, CVSS 7.5) meets the embargo check threshold (CVSS >= 7.0). The warning gate must be presented to the engineer before proceeding.

## Warning Gate

```
================================================
  EMBARGO CHECK -- CVE-2026-31812 (High severity)
================================================

High-severity vulnerabilities may be under embargo.
Before proceeding, verify with your security team that this CVE
is cleared for public triage.

  CVE:      CVE-2026-31812
  Severity: High (CVSS 7.5)
  Risk:     This vulnerability may be under embargo restrictions.
            Proceeding with triage before embargo clearance could
            violate disclosure policies.

  Embargo policy: https://example.com/security/embargo-policy

Proceed with triage? (Yes / No)
================================================
```

## Gate Behavior

- **If "No"**: Stop execution immediately. Inform the engineer to check embargo status with the security team before re-running triage. No Jira mutations will occur. No triage output will be generated.
- **If "Yes"**: Proceed to Step 2 (Version Impact Analysis) as normal.

This gate is consistent with the existing guardrail pattern -- every Jira mutation requires confirmation. No Jira mutations occur at this step. The gate fires before any triage output, so stopping is safe.
