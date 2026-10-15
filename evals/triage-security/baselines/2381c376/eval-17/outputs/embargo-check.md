# Step 1.7 -- Embargo Check

## Configuration

- Embargo policy URL: https://example.com/security/embargo-policy
- Configured: **Yes** (step is not skipped)

## Severity Evaluation

| Attribute | Value |
|-----------|-------|
| CVE ID | CVE-2026-31812 |
| CVSS Score | 7.5 |
| Severity | High |
| Trigger threshold | CVSS >= 7.0 (Critical or Important/High) |
| Threshold met? | **Yes** (7.5 >= 7.0) |

The CVSS score of 7.5 meets the embargo check threshold of >= 7.0. The warning gate must be presented to the engineer before proceeding.

## Warning Gate

The following warning would be presented to the engineer:

```
EMBARGO CHECK -- CVE-2026-31812 (High severity, CVSS 7.5)

High-severity vulnerabilities may be under embargo.
Before proceeding, verify with your security team that this CVE
is cleared for public triage.

Embargo policy: https://example.com/security/embargo-policy

Proceed with triage? (Yes / No)
```

## Gate Behavior

- If the engineer responds **"Yes"**: Proceed to Step 2 (Version Impact Analysis).
- If the engineer responds **"No"**: Stop execution. The engineer must verify embargo status with the security team before re-running triage. No Jira mutations or further analysis occurs.

## Notes

- This is an advisory warning gate only -- it does not enforce embargo procedures.
- No Jira mutations occur at this step. The gate fires before any triage output, so stopping is safe.
- The gate is consistent with the existing guardrail pattern (every Jira mutation requires confirmation).
