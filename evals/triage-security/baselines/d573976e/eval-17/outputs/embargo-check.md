# Step 1.7 -- Embargo Check

## Configuration Check

The Embargo policy URL is configured in Security Configuration:
- **Embargo policy URL**: https://example.com/security/embargo-policy

Since the Embargo policy URL is present, this step is NOT skipped.

## Severity Evaluation

The CVE severity is determined from the extracted data in Step 1:

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-31812 |
| CVSS Score | 7.5 |
| Severity | High |
| Threshold | CVSS >= 7.0 (Critical or Important) |
| Triggers gate? | **YES** -- 7.5 >= 7.0 |

The CVSS score of 7.5 (High severity) meets the Critical/Important threshold (CVSS >= 7.0). The embargo warning gate is triggered.

**Note**: For Low or Moderate severity CVEs (CVSS < 7.0), this step would be skipped silently and triage would proceed directly to Step 2. The gate only fires for Critical/Important severity (CVSS >= 7.0).

## Warning Gate Presented to Engineer

The following warning is presented to the engineer and requires explicit confirmation before proceeding:

```
EMBARGO CHECK -- CVE-2026-31812 (High severity, CVSS 7.5)

High-severity vulnerabilities may be under embargo.
Before proceeding, verify with your security team that this CVE
is cleared for public triage.

Embargo policy: https://example.com/security/embargo-policy

Proceed with triage? (Yes / No)
```

## Confirmation Gate Behavior

This is a **confirmation prompt**, not an informational message. The skill MUST wait for the engineer's explicit response before continuing:

- **If the engineer responds "Yes"**: Proceed to Step 2 (Version Impact Analysis) as normal. The rest of the triage follows the standard flow.
- **If the engineer responds "No"**: Stop execution immediately. Inform the engineer to check embargo status with the security team before re-running triage. Do not proceed to Step 2 or any subsequent step.

No Jira mutations occur at this step -- the gate fires before any triage output, so stopping is safe. This is consistent with the existing guardrail pattern where every Jira mutation requires confirmation.

## Outcome (for this eval)

Assuming the engineer confirms "Yes", triage proceeds to Step 2 (Version Impact Analysis).
