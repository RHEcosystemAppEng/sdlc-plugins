# Step 1.7 -- Embargo Check

## Configuration

- Embargo policy URL: https://example.com/security/embargo-policy (extracted from Security Configuration in Step 0)
- This is an optional field -- extracted without raising an error. If not configured, Step 1.7 would be skipped entirely.

## Severity Evaluation

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-31812 |
| CVSS Score | 7.5 |
| Severity Level | High |
| Trigger Threshold | Critical/Important (CVSS >= 7.0) |
| Threshold Met? | **YES** -- 7.5 >= 7.0 |

The CVE severity is High (CVSS 7.5), which meets the Critical/Important threshold (CVSS >= 7.0). This triggers the embargo warning gate.

Note: For Low or Moderate severity CVEs (CVSS < 7.0), this step is skipped silently -- no warning is presented and triage proceeds directly to Step 2. The embargo gate only fires for Critical (CVSS >= 9.0) and Important/High (CVSS >= 7.0) severity levels.

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

This is a **confirmation prompt**, not an informational message. The engineer must explicitly respond with Yes or No:

- **If "Yes"**: Triage proceeds to Step 2 (Version Impact Analysis) as normal.
- **If "No"**: Execution stops immediately. The engineer is informed to check embargo status with their security team before re-running triage. No Jira mutations occur, no triage output is generated beyond this point.

The gate fires before any triage output or Jira mutations, so stopping is always safe. This is consistent with the existing guardrail pattern where every significant action requires engineer confirmation.

## Decision

For this triage run, the engineer confirmed **Yes** -- proceeding to Step 2.
