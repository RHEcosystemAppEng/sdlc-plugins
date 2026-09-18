# Step 1.7 -- Embargo Check

## Configuration

Embargo policy URL is configured in Security Configuration:
- **Embargo policy URL**: https://example.com/security/embargo-policy

Since an Embargo policy URL is configured, this step is **not skipped**.

## Severity Evaluation

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-31812 |
| CVSS Score | 7.5 |
| Severity | High |
| Trigger threshold | Critical or Important (CVSS >= 7.0) |
| Threshold met? | **YES** -- CVSS 7.5 >= 7.0 |

The CVE severity is **High** (CVSS 7.5), which meets the trigger threshold of CVSS >= 7.0. The embargo warning gate must be presented to the engineer.

## Warning Gate

The following warning gate is presented to the engineer before proceeding:

```
WARNING: EMBARGO CHECK -- CVE-2026-31812 (High severity, CVSS 7.5)

High-severity vulnerabilities may be under embargo.
Before proceeding, verify with your security team that this CVE
is cleared for public triage.

Embargo policy: https://example.com/security/embargo-policy

Proceed with triage? (Yes / No)
```

## Decision Point

- If the engineer responds **"No"**: execution stops immediately. The engineer must check embargo status with their security team before re-running triage. No Jira mutations occur, no version impact analysis is performed.
- If the engineer responds **"Yes"**: triage proceeds to Step 2 (Version Impact Analysis) as normal.

This gate is consistent with the existing guardrail pattern -- every Jira mutation requires confirmation. No Jira mutations occur at this step. The gate fires before any triage output, so stopping is safe.
