# Step 1.7 -- Embargo Check

## Configuration

- Embargo policy URL: https://example.com/security/embargo-policy
- Embargo policy URL is **configured** -- Step 1.7 is active (not skipped).

## Severity Evaluation

| Criterion | Value |
|-----------|-------|
| CVE ID | CVE-2026-31812 |
| CVSS Score | 7.5 |
| Severity | High |
| Trigger threshold | Critical or Important (CVSS >= 7.0) |
| Threshold met? | **YES** -- 7.5 >= 7.0 |

The CVSS score of 7.5 (High severity) meets the embargo check threshold of >= 7.0. The warning gate must be presented to the engineer before proceeding.

## Warning Gate

The following warning gate is presented to the engineer:

```
EMBARGO CHECK -- CVE-2026-31812 (High severity, CVSS 7.5)

High-severity vulnerabilities may be under embargo.
Before proceeding, verify with your security team that this CVE
is cleared for public triage.

Embargo policy: https://example.com/security/embargo-policy

Proceed with triage? (Yes / No)
```

## Gate Outcome

- If the engineer answers **Yes**: proceed to Step 2 (Version Impact Analysis).
- If the engineer answers **No**: stop execution immediately. The engineer must verify embargo status with the security team before re-running triage.

## Rationale

This gate is consistent with the existing guardrail pattern (every Jira mutation requires confirmation). No Jira mutations occur at this step -- the gate fires before any triage output, so stopping is safe. The embargo policy URL provides the engineer with direct access to the organization's embargo procedures for verification.
