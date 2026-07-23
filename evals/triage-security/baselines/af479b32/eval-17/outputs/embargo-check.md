# Step 1.7 -- Embargo Check

## Configuration

- Embargo policy URL: https://example.com/security/embargo-policy
- Embargo policy URL is **configured** in Security Configuration -- this step is active.

## Severity Evaluation

| Criterion | Value |
|-----------|-------|
| CVE ID | CVE-2026-31812 |
| CVSS Score | 7.5 |
| Severity | High |
| Trigger threshold | CVSS >= 7.0 (Critical or Important) |
| Threshold met? | **YES** -- 7.5 >= 7.0 |

The CVSS score of 7.5 classifies this vulnerability as **High** severity, which meets the embargo check threshold of CVSS >= 7.0.

## Warning Gate

Because the severity meets the threshold, the following warning gate is presented to the engineer before proceeding:

```
EMBARGO CHECK -- CVE-2026-31812 (High severity, CVSS 7.5)

High-severity vulnerabilities may be under embargo.
Before proceeding, verify with your security team that this CVE
is cleared for public triage.

Embargo policy: https://example.com/security/embargo-policy

Proceed with triage? (Yes / No)
```

## Decision

- If the engineer selects **Yes**: proceed to Step 2 (Version Impact Analysis).
- If the engineer selects **No**: stop execution. The engineer must verify embargo status with the security team and re-run triage after clearance is confirmed.

## Rationale

This gate is an advisory warning for high-severity vulnerabilities that may be under embargo. It does not enforce embargo procedures -- it surfaces a warning and links to the organization's embargo policy for the engineer to verify. No Jira mutations occur at this step, so stopping is safe.

The gate is consistent with the existing guardrail pattern (every Jira mutation requires confirmation). It fires before any triage output is written to Jira, ensuring no information leakage occurs if the CVE is under embargo.
