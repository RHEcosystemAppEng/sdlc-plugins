# Step 1.7 -- Embargo Check: CVE-2026-31812

## Configuration Check

Embargo policy URL is configured in Security Configuration:
- **Embargo policy URL**: https://example.com/security/embargo-policy

Result: Embargo check is **enabled** (URL is configured). Proceeding to severity evaluation.

## Severity Evaluation

| Criterion | Value |
|-----------|-------|
| CVE ID | CVE-2026-31812 |
| CVSS score | 7.5 |
| Severity | High |
| Trigger threshold | Critical or Important (CVSS >= 7.0) |
| Threshold met? | **YES** -- 7.5 >= 7.0 |

The CVSS score of 7.5 classifies this vulnerability as **High** severity, which meets the embargo check threshold of CVSS >= 7.0 (Critical or Important).

## Warning Gate Presented to Engineer

Since the severity meets the threshold and an embargo policy URL is configured, the following warning gate is presented:

---

> **EMBARGO CHECK -- CVE-2026-31812 (High severity)**
>
> High-severity vulnerabilities may be under embargo.
> Before proceeding, verify with your security team that this CVE
> is cleared for public triage.
>
> Embargo policy: https://example.com/security/embargo-policy
>
> Proceed with triage? (Yes / No)

---

## Gate Behavior

- **If the engineer responds "Yes"**: Proceed to Step 2 (Version Impact Analysis) as normal. The embargo check is an advisory gate only -- it does not enforce embargo procedures, it surfaces a warning and links to the organization's embargo policy for the engineer to verify.

- **If the engineer responds "No"**: Stop execution immediately. Inform the user to check embargo status with their security team before re-running triage. Do not proceed to Step 2.

## Rationale

This gate is consistent with the skill's existing guardrail pattern: every Jira mutation requires confirmation. No Jira mutations have occurred at this point -- the gate fires before any triage output, so stopping is safe. The gate provides a checkpoint for the engineer to verify that the CVE is cleared for public triage before any further analysis or Jira changes are made.
