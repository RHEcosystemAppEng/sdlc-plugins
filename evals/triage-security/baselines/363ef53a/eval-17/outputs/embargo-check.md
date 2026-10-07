# Step 1.7 -- Embargo Check for CVE-2026-31812

## Configuration Check

- Embargo policy URL: **configured** -- https://example.com/security/embargo-policy
- Step 1.7 is **not skipped** (Embargo policy URL is present in Security Configuration)

## Severity Evaluation

- CVE: CVE-2026-31812
- CVSS score: **7.5**
- Severity: **High**
- Trigger threshold: CVSS >= 7.0 (Critical or Important severity)
- Result: **Severity meets the threshold** (7.5 >= 7.0)

Step is **not skipped** -- the severity is High, which meets the Critical/Important threshold.

## Warning Gate Presented to Engineer

```
WARNING -- EMBARGO CHECK -- CVE-2026-31812 (High severity)

High-severity vulnerabilities may be under embargo.
Before proceeding, verify with your security team that this CVE
is cleared for public triage.

Embargo policy: https://example.com/security/embargo-policy

Proceed with triage? (Yes / No)
```

## Decision Flow

- If "Yes": proceed to Step 2 (Version Impact Analysis)
- If "No": stop execution; inform the user to check embargo status before re-running triage

This gate fires before any triage output or Jira mutations, so stopping is safe. It is consistent with the existing guardrail pattern (every Jira mutation requires confirmation).
