# Step 1.7 -- Embargo Check: CVE-2026-31812

## Configuration

- Embargo policy URL: https://example.com/security/embargo-policy
- Embargo policy URL configured: **Yes**

## Severity Evaluation

| Criterion | Value |
|-----------|-------|
| CVE ID | CVE-2026-31812 |
| CVSS Score | 7.5 |
| Severity | High |
| Trigger threshold | Critical or Important (CVSS >= 7.0) |
| Threshold met? | **YES** (7.5 >= 7.0) |

The CVSS score of 7.5 meets the embargo check trigger threshold of >= 7.0.
This step is NOT skipped -- the warning gate must be presented to the engineer.

## Warning Gate

The following warning gate is presented to the engineer before proceeding:

```
EMBARGO CHECK -- CVE-2026-31812 (High severity, CVSS 7.5)

High-severity vulnerabilities may be under embargo.
Before proceeding, verify with your security team that this CVE
is cleared for public triage.

Embargo policy: https://example.com/security/embargo-policy

Proceed with triage? (Yes / No)
```

## Decision Flow

- If the engineer answers **Yes**: proceed to Step 2 (Version Impact Analysis)
- If the engineer answers **No**: stop execution immediately; inform the user
  to check embargo status with their security team before re-running triage.
  No Jira mutations have occurred at this point, so stopping is safe.

## Rationale

This gate is triggered because:
1. An Embargo policy URL is configured in the project's Security Configuration
2. The CVE severity (CVSS 7.5 / High) meets the threshold (>= 7.0)
3. High-severity vulnerabilities are more likely to be under embargo restrictions
4. The gate fires before any triage output or Jira mutations, consistent with
   the skill's guardrail pattern requiring engineer confirmation before actions
