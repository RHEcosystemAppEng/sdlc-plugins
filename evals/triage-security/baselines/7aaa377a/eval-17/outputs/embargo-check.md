# Step 1.7 -- Embargo Check

## Configuration

- **Embargo policy URL**: https://example.com/security/embargo-policy (configured in Security Configuration)
- Embargo policy URL is an optional field and was extracted from Security Configuration without raising an error (backward compatible extraction).

## Severity Evaluation

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-31812 |
| CVSS Score | 7.5 |
| Severity Level | High |
| Embargo Threshold | Critical/Important (CVSS >= 7.0) |
| Threshold Met? | **YES** -- CVSS 7.5 >= 7.0 |

The CVE severity is **High** (CVSS 7.5), which meets the Critical/Important threshold (CVSS >= 7.0). The embargo warning gate is triggered.

## Warning Gate Presented to Engineer

```
EMBARGO CHECK -- CVE-2026-31812 (High severity, CVSS 7.5)

High-severity vulnerabilities may be under embargo.
Before proceeding, verify with your security team that this CVE
is cleared for public triage.

Embargo policy: https://example.com/security/embargo-policy

Proceed with triage? (Yes / No)
```

This is a **confirmation prompt** that requires explicit engineer input (Yes or No) before the triage can proceed to Step 2 (Version Impact Analysis). It is not merely an informational message -- the triage halts at this gate until the engineer responds.

- If the engineer selects **"Yes"**: triage proceeds to Step 2 (Version Impact Analysis) as normal.
- If the engineer selects **"No"**: execution stops immediately. The engineer is informed to check embargo status before re-running triage. No Jira mutations occur, and Step 2 is not reached.

## Threshold Behavior Notes

The embargo warning gate only triggers for **Critical or Important** severity CVEs (CVSS >= 7.0). For Low or Moderate severity CVEs (CVSS < 7.0), this step is skipped silently -- no warning is displayed, no user prompt is presented, and triage proceeds directly to Step 2 without interruption.

| Severity | CVSS Range | Gate Behavior |
|----------|------------|---------------|
| Critical | 9.0 - 10.0 | Triggers embargo warning gate |
| Important/High | 7.0 - 8.9 | Triggers embargo warning gate |
| Moderate/Medium | 4.0 - 6.9 | Skipped silently |
| Low | 0.1 - 3.9 | Skipped silently |

## Assumption for This Eval

For the purposes of this eval, we assume the engineer confirmed **"Yes"** and triage proceeds to Step 2.
