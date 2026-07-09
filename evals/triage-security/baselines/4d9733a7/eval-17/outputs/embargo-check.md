# Step 1.7 -- Embargo Check

## Configuration

Step 0 extracted the following embargo-related configuration from the Security Configuration in CLAUDE.md:

- **Embargo policy URL**: https://example.com/security/embargo-policy (configured as an optional field -- extracted without error, backward compatible)

## Severity Evaluation

- **CVE ID**: CVE-2026-31812
- **CVSS score**: 7.5
- **Severity level**: High
- **Threshold check**: CVSS 7.5 >= 7.0 (Critical/Important threshold) -- **MEETS THRESHOLD**

Since the severity is High (CVSS >= 7.0), the embargo warning gate is triggered.

## Warning Gate Presented to Engineer

```
EMBARGO CHECK -- CVE-2026-31812 (High severity, CVSS 7.5)

High-severity vulnerabilities may be under embargo.
Before proceeding, verify with your security team that this CVE
is cleared for public triage.

Embargo policy: https://example.com/security/embargo-policy

Proceed with triage? (Yes / No)
```

**This is a confirmation prompt, not an informational message.** The engineer must explicitly choose Yes or No before triage continues:

- **If "Yes"**: Proceed to Step 2 (Version Impact Analysis) as normal.
- **If "No"**: Stop execution and inform the user to check embargo status before re-running triage. Do not proceed to Step 2.

## Note on Low/Moderate Severity CVEs

For CVEs with CVSS < 7.0 (Low or Moderate severity), this embargo warning gate is **skipped silently** -- no warning is displayed and triage proceeds directly to Step 2 without any user prompt. The gate only fires for Critical or Important severity (CVSS >= 7.0).

## Outcome

Assuming the engineer confirms "Yes", triage proceeds to Step 2 with standard flow.
