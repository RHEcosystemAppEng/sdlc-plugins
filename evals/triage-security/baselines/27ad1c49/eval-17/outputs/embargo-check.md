# Step 1.7 -- Embargo Check: CVE-2026-31812

## Configuration Check

Embargo policy URL is configured in Security Configuration:
**https://example.com/security/embargo-policy**

Since the Embargo policy URL is configured, this step proceeds (if it were not configured, this step would be skipped entirely).

## Severity Evaluation

| Criterion | Value |
|-----------|-------|
| CVE ID | CVE-2026-31812 |
| CVSS Score | 7.5 |
| Severity | High |
| Embargo trigger threshold | CVSS >= 7.0 (Critical or Important/High) |
| Threshold met? | **YES** -- 7.5 >= 7.0 |

The CVSS score of 7.5 (High severity) meets the embargo trigger threshold of >= 7.0. The warning gate must be presented to the engineer before proceeding.

## Warning Gate Presented to Engineer

```
EMBARGO CHECK -- CVE-2026-31812 (High severity, CVSS 7.5)

High-severity vulnerabilities may be under embargo.
Before proceeding, verify with your security team that this CVE
is cleared for public triage.

Embargo policy: https://example.com/security/embargo-policy

Proceed with triage? (Yes / No)
```

## Gate Behavior

- If the engineer responds **"Yes"**: proceed to Step 2 (Version Impact Analysis) as normal.
- If the engineer responds **"No"**: stop execution immediately and inform the user to check embargo status with their security team before re-running triage. No further triage steps are executed, and no Jira mutations occur.

This gate fires before any triage output or Jira mutations, so stopping is safe. The gate is consistent with the existing guardrail pattern (every Jira mutation requires confirmation).
