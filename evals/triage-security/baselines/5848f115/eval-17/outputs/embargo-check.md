# Step 1.7 -- Embargo Check

## Configuration

- **Embargo policy URL**: https://example.com/security/embargo-policy (configured in Security Configuration)

Since an Embargo policy URL is configured, this step is **not skipped**.

## Severity Evaluation

| Attribute | Value |
|-----------|-------|
| CVE ID | CVE-2026-31812 |
| CVSS Score | 7.5 |
| Severity | High |
| Trigger Threshold | CVSS >= 7.0 (Critical or Important) |
| Threshold Met? | **YES** (7.5 >= 7.0) |

The severity is High (CVSS 7.5), which meets the embargo check threshold of CVSS >= 7.0.

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

## Decision Point

- If the engineer responds **"Yes"**: proceed to Step 2 (Version Impact Analysis).
- If the engineer responds **"No"**: stop execution. The engineer must verify embargo status with the security team and re-run triage after clearance.

No Jira mutations have occurred at this point -- stopping is safe. This gate is consistent with the existing guardrail pattern (every Jira mutation requires confirmation).
