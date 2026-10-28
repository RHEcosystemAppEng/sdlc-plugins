# Step 1.7 -- Embargo Check

## Configuration

- Embargo policy URL: https://example.com/security/embargo-policy
- Embargo policy URL configured: **Yes**
- Step 1.7 applies (not skipped)

## Severity Evaluation

| Criterion | Value |
|-----------|-------|
| CVE ID | CVE-2026-31812 |
| CVSS Score | 7.5 |
| Severity | High |
| Trigger threshold | CVSS >= 7.0 (Critical or Important) |
| Threshold met? | **Yes** (7.5 >= 7.0) |

The CVSS score of 7.5 classifies this vulnerability as **High** severity, which meets the embargo check trigger threshold of CVSS >= 7.0.

## Warning Gate Presented to Engineer

Since the severity meets the threshold and an embargo policy URL is configured, the following warning gate is presented to the engineer before proceeding:

```
EMBARGO CHECK -- CVE-2026-31812 (High severity, CVSS 7.5)

High-severity vulnerabilities may be under embargo.
Before proceeding, verify with your security team that this CVE
is cleared for public triage.

Embargo policy: https://example.com/security/embargo-policy

Proceed with triage? (Yes / No)
```

## Gate Behavior

- If the engineer responds **"Yes"**: proceed to Step 2 (Version Impact Analysis) as normal.
- If the engineer responds **"No"**: stop execution immediately. The engineer must check embargo status with the security team before re-running triage. No Jira mutations, version impact analysis, or remediation tasks will be created.

## Rationale

This gate is an advisory warning, not an enforcement mechanism. It surfaces the embargo risk for high-severity CVEs and links to the organization's embargo policy so the engineer can verify clearance. No Jira mutations occur at this step -- the gate fires before any triage output, making it safe to stop without side effects.

The gate is consistent with the existing guardrail pattern where every significant action requires engineer confirmation before proceeding.
