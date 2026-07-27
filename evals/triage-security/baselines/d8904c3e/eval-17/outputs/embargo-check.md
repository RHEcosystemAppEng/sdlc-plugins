# Step 1.7 -- Embargo Check

## Configuration

- Embargo policy URL: https://example.com/security/embargo-policy (configured in Security Configuration)

## Severity Evaluation

| Attribute | Value |
|-----------|-------|
| CVE ID | CVE-2026-31812 |
| CVSS Score | 7.5 |
| Severity | High |
| Trigger threshold | CVSS >= 7.0 (Critical or Important) |
| Threshold met? | **YES** -- 7.5 >= 7.0 |

The CVSS score of 7.5 (High severity) meets the embargo check trigger threshold of >= 7.0. The embargo warning gate must be presented to the engineer before proceeding.

## Warning Gate

```
EMBARGO CHECK -- CVE-2026-31812 (High severity)

High-severity vulnerabilities may be under embargo.
Before proceeding, verify with your security team that this CVE
is cleared for public triage.

Embargo policy: https://example.com/security/embargo-policy

Proceed with triage? (Yes / No)
```

## Behavior

- If the engineer answers **Yes**: proceed to Step 2 (Version Impact Analysis).
- If the engineer answers **No**: stop execution immediately. The engineer must verify embargo status with the security team before re-running triage. No Jira mutations or triage output will be produced.

This gate is consistent with the existing guardrail pattern -- every Jira mutation requires confirmation. No Jira mutations occur at this step, so stopping is safe. The gate fires before any triage output is generated.
