# Step 1.7 -- Embargo Check

## Configuration

- Embargo policy URL: https://example.com/security/embargo-policy (configured in Security Configuration)
- Step 1.7 is active because Embargo policy URL is configured.

## Severity Evaluation

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-31812 |
| CVSS Score | 7.5 |
| Severity | High |
| Trigger Threshold | CVSS >= 7.0 (Critical or Important) |
| Threshold Met? | **YES** -- 7.5 >= 7.0 |

Because the CVSS score of 7.5 meets the threshold of >= 7.0, the embargo warning gate is triggered.

## Warning Gate

The following warning gate is presented to the engineer for confirmation:

```
EMBARGO CHECK -- CVE-2026-31812 (High severity)

High-severity vulnerabilities may be under embargo.
Before proceeding, verify with your security team that this CVE
is cleared for public triage.

Embargo policy: https://example.com/security/embargo-policy

Proceed with triage? (Yes / No)
```

### Gate Behavior

- If the engineer responds **"Yes"**: proceed to Step 2 (Version Impact Analysis) as normal.
- If the engineer responds **"No"**: stop execution and inform the user to check embargo status before re-running triage. Do not proceed to Step 2.

## Threshold Logic

This gate does **NOT** trigger for CVSS < 7.0. Vulnerabilities with Low or Moderate severity (CVSS below 7.0) skip Step 1.7 silently and proceed directly to Step 2. The gate only fires for Critical or Important severity (CVSS >= 7.0) when an Embargo policy URL is configured.

If no Embargo policy URL were configured in Security Configuration, Step 1.7 would be skipped entirely regardless of severity.
