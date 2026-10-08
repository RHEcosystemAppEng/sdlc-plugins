# Step 1.7 -- Embargo Check

## Configuration

- Embargo policy URL: https://example.com/security/embargo-policy (configured in Security Configuration)

## Severity Evaluation

- CVE: CVE-2026-31812
- CVSS score: 7.5
- Severity: **High** (Important)
- Threshold: Critical or Important (CVSS >= 7.0)
- Result: **CVSS 7.5 >= 7.0 -- threshold met, embargo warning gate triggered**

## Warning Gate Presented to Engineer

```
EMBARGO CHECK -- CVE-2026-31812 (High severity, CVSS 7.5)

High-severity vulnerabilities may be under embargo.
Before proceeding, verify with your security team that this CVE
is cleared for public triage.

Embargo policy: https://example.com/security/embargo-policy

Proceed with triage? (Yes / No)
```

## Gate Outcome

The engineer must confirm before triage continues to Step 2 (Version Impact Analysis). If the engineer responds "No", execution stops and the engineer should verify embargo status with the security team before re-running triage. If the engineer responds "Yes", triage proceeds to Step 2 as normal.

No Jira mutations occur at this step -- the gate fires before any triage output, so stopping is safe.
