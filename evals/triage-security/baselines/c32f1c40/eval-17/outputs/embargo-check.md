# Step 1.7 -- Embargo Check

## Configuration

Embargo policy URL is configured in Security Configuration:
- **Embargo policy URL**: https://example.com/security/embargo-policy

This is an optional field. It was extracted from the Security Configuration without raising an error (backward compatible extraction). If it were absent, Step 1.7 would be skipped entirely.

## Severity Evaluation

The CVE severity is determined from the Jira description and/or Step 1.5 enrichment:

- **CVE ID**: CVE-2026-31812
- **CVSS Score**: 7.5
- **Severity Level**: High

**Threshold check**: The trigger threshold is Critical or Important severity (CVSS >= 7.0). CVSS 7.5 **meets** this threshold.

Note: For Low or Moderate severity CVEs (CVSS < 7.0), this step would be skipped silently -- no warning gate would be presented, and triage would proceed directly to Step 2.

## Embargo Warning Gate

Since the CVE severity (CVSS 7.5, High) meets the Critical/Important threshold (>= 7.0), the following warning gate is presented to the engineer:

---

> **EMBARGO CHECK -- CVE-2026-31812 (High severity, CVSS 7.5)**
>
> High-severity vulnerabilities may be under embargo.
> Before proceeding, verify with your security team that this CVE
> is cleared for public triage.
>
> Embargo policy: https://example.com/security/embargo-policy
>
> **Proceed with triage? (Yes / No)**

---

This is a **confirmation prompt**, not an informational message. The engineer must explicitly respond with Yes or No before triage can proceed.

- **If "Yes"**: Proceed to Step 2 (Version Impact Analysis) as normal.
- **If "No"**: Stop execution and inform the user to check embargo status before re-running triage. No Jira mutations occur, and no further steps are executed.

This gate fires before any triage output or Jira mutations, so stopping is safe. It is consistent with the existing guardrail pattern (every Jira mutation requires confirmation).

## Outcome

For this analysis, we assume the engineer confirms "Yes" and triage proceeds to Step 2.
