# Step 1.7 -- Embargo Check

## Configuration

- Embargo policy URL: https://example.com/security/embargo-policy
- Embargo policy URL is **configured** in Security Configuration -- this step is active.

## Severity Evaluation

| Parameter | Value |
|-----------|-------|
| CVE ID | CVE-2026-31812 |
| CVSS Score | 7.5 |
| Severity | High |
| Trigger threshold | CVSS >= 7.0 (Critical or Important) |
| Threshold met? | **Yes** -- 7.5 >= 7.0 |

The vulnerability severity (High, CVSS 7.5) meets the embargo check threshold
(Critical or Important, CVSS >= 7.0). The warning gate must be presented to the
engineer before proceeding.

## Warning Gate

```
EMBARGO CHECK -- CVE-2026-31812 (High severity)

High-severity vulnerabilities may be under embargo.
Before proceeding, verify with your security team that this CVE
is cleared for public triage.

Embargo policy: https://example.com/security/embargo-policy

Proceed with triage? (Yes / No)
```

## Gate Behavior

- If the engineer answers **No**: Stop execution immediately. Inform the user to
  check embargo status with their security team before re-running triage. Do not
  proceed to Step 2.
- If the engineer answers **Yes**: Proceed to Step 2 (Version Impact Analysis).

This gate fires before any triage output or Jira mutations, so stopping is safe.
No data has been written to Jira at this point.
