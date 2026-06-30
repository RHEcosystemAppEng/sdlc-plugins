# Step 1.7 — Embargo Check

## Configuration

Embargo policy URL is configured in Security Configuration: `https://example.com/security/embargo-policy`

## Severity Evaluation

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-31812 |
| CVSS Score | 7.5 |
| Severity | High |
| Embargo threshold | CVSS >= 7.0 (Critical or Important) |
| Threshold met? | **YES** (7.5 >= 7.0) |

The CVSS score of 7.5 meets the embargo check threshold (>= 7.0). The warning gate must be presented to the engineer before proceeding with triage.

## Warning Gate

```
⚠️ EMBARGO CHECK — CVE-2026-31812 (High severity)

High-severity vulnerabilities may be under embargo.
Before proceeding, verify with your security team that this CVE
is cleared for public triage.

Embargo policy: https://example.com/security/embargo-policy

Proceed with triage? (Yes / No)
```

## Gate Outcome

This gate requires explicit engineer confirmation before proceeding to Step 2 (Version Impact Analysis).

- If **"Yes"**: proceed to Step 2 as normal.
- If **"No"**: stop execution. The engineer must verify embargo status with the security team before re-running triage. No Jira mutations will have occurred at this point — the gate fires before any triage output, so stopping is safe.
