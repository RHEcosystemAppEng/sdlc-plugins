# Step 1.7 -- Embargo Check: CVE-2026-31812

## Configuration Check

- Embargo policy URL: **configured** -- `https://example.com/security/embargo-policy`
- Since the embargo policy URL is configured, this step proceeds (not skipped).

## Severity Evaluation

| Criterion | Value | Source |
|-----------|-------|--------|
| CVSS Score | 7.5 | Issue description / Step 1 extraction |
| Severity | High | Derived from CVSS 7.5 |
| Trigger threshold | CVSS >= 7.0 (Critical or Important) | SKILL.md Step 1.7 |
| Threshold met? | **YES** (7.5 >= 7.0) | Comparison |

The CVE severity is **High** (CVSS 7.5), which meets the embargo check threshold of CVSS >= 7.0. The warning gate must be presented to the engineer.

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

- If the engineer responds **"Yes"**: Proceed to Step 2 (Version Impact Analysis) as normal.
- If the engineer responds **"No"**: Stop execution immediately. Inform the engineer to check embargo status with ProdSec before re-running triage. No Jira mutations, no version impact analysis, no remediation tasks -- nothing proceeds until embargo clearance is confirmed.

## Rationale

This gate is consistent with the guardrail pattern that every Jira mutation requires confirmation. No Jira mutations occur at this step -- the gate fires before any triage output, so stopping is safe. The gate is advisory only; it does not enforce embargo procedures. It surfaces a warning and links to the organization's embargo policy for the engineer to verify independently.

## Note

This is a non-blocking advisory gate. The skill does not determine embargo status automatically -- it relies on the engineer to verify with their security team. The embargo policy URL (`https://example.com/security/embargo-policy`) provides the organizational procedures for embargo handling.
