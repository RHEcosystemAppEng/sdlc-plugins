# Step 1.7 -- Embargo Check for TC-8001

## Configuration Check

Embargo policy URL is configured in Security Configuration (extracted in Step 0 as an optional field):
- **Embargo policy URL**: https://example.com/security/embargo-policy

Embargo check is **enabled** (URL is present). If no Embargo policy URL were configured, this step would be skipped entirely -- the field is optional and its absence does not raise an error.

## Severity Evaluation

| Metric | Value |
|--------|-------|
| CVE ID | CVE-2026-31812 |
| CVSS Score | 7.5 |
| Severity | High |
| Trigger threshold | CVSS >= 7.0 (Critical or Important) |
| Threshold met? | **YES** (7.5 >= 7.0) |

The CVSS score of 7.5 meets the embargo check threshold of 7.0. The warning gate must be presented to the engineer.

### Threshold behavior for Low/Moderate severity CVEs

For CVEs with CVSS < 7.0 (Low or Moderate severity), the embargo check step is **skipped silently** -- no warning gate is presented to the engineer, and execution proceeds directly to Step 2 (Version Impact Analysis). The gate only fires for Critical or Important severity (CVSS >= 7.0). For example, a CVE with CVSS 4.3 (Medium) would bypass this step entirely without any user-facing output.

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

- If the engineer answers **Yes**: proceed to Step 2 (Version Impact Analysis).
- If the engineer answers **No**: stop execution immediately. The engineer must verify embargo status with their security team before re-running triage. No Jira mutations or triage output will be produced.

## Rationale

This gate is consistent with the skill's guardrail pattern requiring engineer confirmation before any triage actions. The gate fires before any triage output is produced (before Step 2), so stopping is safe -- no Jira mutations have occurred at this point. The embargo policy URL provides the engineer a direct reference to their organization's policy for verification.
