# Step 1.7 -- Embargo Check

## Configuration

Embargo policy URL is configured in Security Configuration:
- **Embargo policy URL**: https://example.com/security/embargo-policy

Step 1.7 is **not skipped** -- an Embargo policy URL is present.

## Severity Evaluation

| Parameter | Value |
|-----------|-------|
| CVE ID | CVE-2026-31812 |
| CVSS score | 7.5 |
| Severity | High |
| Embargo threshold | CVSS >= 7.0 (Critical or Important) |
| Threshold met? | **YES** (7.5 >= 7.0) |

The CVSS score of 7.5 (High severity) meets the embargo trigger threshold of >= 7.0. The embargo warning gate is activated.

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

- **If "Yes"**: Proceed to Step 2 (Version Impact Analysis) as normal.
- **If "No"**: Stop execution immediately. Inform the user to check embargo status with their security team before re-running triage. Do not proceed to Step 2.

This gate fires before any triage output or Jira mutations, so stopping is safe. No data has been written to Jira at this point -- only read operations (issue fetch, remote links) have been performed.

## Rationale

The embargo check is an advisory warning gate, not an enforcement mechanism. It surfaces a warning and links to the organization's embargo policy (https://example.com/security/embargo-policy) so the engineer can verify that the CVE is cleared for public triage. High-severity vulnerabilities (CVSS >= 7.0) are more likely to be under embargo restrictions, so this gate ensures the engineer consciously confirms before proceeding with triage actions that may generate Jira comments, task descriptions, or other artifacts visible to the team.

## Requires Explicit Confirmation

This step requires an explicit **Yes** or **No** response from the engineer before proceeding to Step 2. The skill does not auto-proceed past this gate.
