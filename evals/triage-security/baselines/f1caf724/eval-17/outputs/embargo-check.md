# Step 1.7 -- Embargo Check

## Configuration

Embargo policy URL is configured: https://example.com/security/embargo-policy

Since the Embargo policy URL is present in Security Configuration, this step is **not skipped**.

## Severity Evaluation

- CVE ID: CVE-2026-31812
- CVSS score: 7.5
- Severity: **High** (Important)
- Trigger threshold: CVSS >= 7.0 (Critical or Important)
- Result: **Severity meets the threshold** -- the embargo warning gate is triggered.

CVSS 7.5 >= 7.0, so the embargo check warning gate must be presented to the engineer.

## Warning Gate

The following warning gate would be presented to the engineer before proceeding to Step 2:

```
EMBARGO CHECK -- CVE-2026-31812 (High / Important severity, CVSS 7.5)

High-severity vulnerabilities may be under embargo.
Before proceeding, verify with your security team that this CVE
is cleared for public triage.

Embargo policy: https://example.com/security/embargo-policy

Proceed with triage? (Yes / No)
```

## Decision

- If the engineer answers **Yes**: proceed to Step 2 (Version Impact Analysis).
- If the engineer answers **No**: stop execution immediately. The engineer must verify embargo status with their security team before re-running triage. No Jira mutations or triage output will occur.

## Rationale

This gate is consistent with the skill's guardrail pattern: every significant action requires engineer confirmation. The embargo check fires before any triage output is produced, so stopping is safe -- no data has been written to Jira or shared externally at this point. The gate is advisory only; it does not enforce embargo procedures but surfaces the warning and links to the organization's embargo policy for the engineer to verify.
