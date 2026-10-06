# Step 1.7 -- Embargo Check

## Configuration

- **Embargo policy URL**: https://example.com/security/embargo-policy (configured in Security Configuration)

Since the Embargo policy URL is configured, this step is **not skipped**.

## Severity Evaluation

| Attribute | Value |
|-----------|-------|
| CVE ID | CVE-2026-31812 |
| CVSS Score | 7.5 |
| Severity | High |
| Embargo threshold | CVSS >= 7.0 (Critical or Important) |
| Threshold met? | **YES** (7.5 >= 7.0) |

The CVSS score of 7.5 (High severity) meets the embargo trigger threshold of >= 7.0. The warning gate must be presented to the engineer.

## Warning Gate

The following warning gate is presented to the engineer before proceeding:

```
WARNING: EMBARGO CHECK -- CVE-2026-31812 (High severity, CVSS 7.5)

High-severity vulnerabilities may be under embargo.
Before proceeding, verify with your security team that this CVE
is cleared for public triage.

Embargo policy: https://example.com/security/embargo-policy

Proceed with triage? (Yes / No)
```

## Decision

- If **"Yes"**: Proceed to Step 2 (Version Impact Analysis) as normal.
- If **"No"**: Stop execution. The engineer must check embargo status with the security team before re-running triage. No Jira mutations or further triage output will be produced.

This gate fires before any triage output is written to Jira, so stopping is safe -- no data has been published or mutated at this point.
