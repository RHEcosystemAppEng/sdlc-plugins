# Step 1.7 -- Embargo Check

## Severity Evaluation

| Parameter | Value |
|-----------|-------|
| CVE ID | CVE-2026-31812 |
| CVSS Score | 7.5 |
| Severity | High |
| Embargo policy URL configured | Yes -- https://example.com/security/embargo-policy |
| Trigger threshold | Critical or Important (CVSS >= 7.0) |
| Threshold met | **Yes** (7.5 >= 7.0) |

## Warning Gate

Since the Embargo policy URL is configured in Security Configuration and the CVE severity (High, CVSS 7.5) meets the trigger threshold (CVSS >= 7.0), the following embargo warning gate is presented to the engineer:

```
EMBARGO CHECK -- CVE-2026-31812 (High severity)

High-severity vulnerabilities may be under embargo.
Before proceeding, verify with your security team that this CVE
is cleared for public triage.

Embargo policy: https://example.com/security/embargo-policy

Proceed with triage? (Yes / No)
```

## Decision Flow

1. **Configuration check**: Embargo policy URL is configured (`https://example.com/security/embargo-policy`) -- proceed with evaluation.
2. **Severity evaluation**: CVSS 7.5 (High) >= 7.0 threshold -- embargo warning is triggered.
3. **Warning gate presented**: The engineer must confirm whether this CVE is cleared for public triage before proceeding to Step 2 (Version Impact Analysis).
4. **If "Yes"**: Proceed to Step 2 as normal.
5. **If "No"**: Stop execution. The engineer must check embargo status with their security team before re-running triage.

This gate fires before any triage output or Jira mutations, so stopping is safe. No data has been written to Jira at this point.
