# Step 1.7 -- Embargo Check: TC-8001

## Configuration Check

- Embargo policy URL: **configured** -- https://example.com/security/embargo-policy
- Result: Embargo check is **active** (policy URL is configured in Security Configuration)

## Severity Evaluation

| Parameter | Value |
|-----------|-------|
| CVE ID | CVE-2026-31812 |
| CVSS Score | 7.5 |
| Severity | **High** |
| Embargo trigger threshold | Critical or Important (CVSS >= 7.0) |
| Threshold met? | **YES** (7.5 >= 7.0) |

The vulnerability severity (CVSS 7.5 / High) meets the embargo trigger threshold of CVSS >= 7.0. The embargo warning gate must be presented to the engineer before proceeding.

## Warning Gate Presented to Engineer

```
WARNING: EMBARGO CHECK -- CVE-2026-31812 (High severity, CVSS 7.5)

High-severity vulnerabilities may be under embargo.
Before proceeding, verify with your security team that this CVE
is cleared for public triage.

Embargo policy: https://example.com/security/embargo-policy

Proceed with triage? (Yes / No)
```

## Gate Behavior

- If the engineer responds **"Yes"**: Proceed to Step 2 (Version Impact Analysis) as normal.
- If the engineer responds **"No"**: Stop execution immediately. Inform the engineer to check embargo status with their security team before re-running triage. No Jira mutations occur -- the gate fires before any triage output.

## Rationale

This gate is consistent with the skill's guardrail pattern (every Jira mutation requires confirmation). No Jira mutations have occurred at this step. The gate ensures that engineers verify embargo clearance for high-severity CVEs before triage results are written to Jira, which could inadvertently disclose embargoed vulnerability details.

The embargo policy URL (https://example.com/security/embargo-policy) links to the organization's embargo procedures. The engineer should consult this document and their ProdSec team to confirm the CVE is cleared for triage before proceeding.
