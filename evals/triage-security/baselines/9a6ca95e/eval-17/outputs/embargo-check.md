# Step 1.7 -- Embargo Check

## Configuration

- Embargo policy URL: https://example.com/security/embargo-policy (configured in Security Configuration)
- Step 1.7 is **not skipped** because an Embargo policy URL is configured.

## Severity Evaluation

| Attribute | Value |
|-----------|-------|
| CVE ID | CVE-2026-31812 |
| CVSS Score | 7.5 |
| Severity | High |
| Trigger Threshold | Critical or Important (CVSS >= 7.0) |
| Threshold Met? | **YES** -- 7.5 >= 7.0 |

The CVSS score of 7.5 classifies this vulnerability as **High** severity, which meets the embargo check threshold of >= 7.0 (Critical or Important). The warning gate is triggered.

## Warning Gate Presented to Engineer

```
WARNING: EMBARGO CHECK -- CVE-2026-31812 (High severity, CVSS 7.5)

High-severity vulnerabilities may be under embargo.
Before proceeding, verify with your security team that this CVE
is cleared for public triage.

Embargo policy: https://example.com/security/embargo-policy

Proceed with triage? (Yes / No)
```

## Gate Behavior

- If the engineer responds **"Yes"**: proceed to Step 2 (Version Impact Analysis) as normal.
- If the engineer responds **"No"**: stop execution immediately. The engineer must verify the embargo status with their security team before re-running triage. No Jira mutations or further triage output will be produced.

This gate fires before any triage output is written to Jira, so stopping is safe -- no partial triage state exists. The gate is consistent with the existing guardrail pattern where every Jira mutation requires confirmation.
