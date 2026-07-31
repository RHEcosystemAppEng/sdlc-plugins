# Step 1.7 -- Embargo Check

## Configuration

Embargo policy URL is configured in Security Configuration:
- **Embargo policy URL**: https://example.com/security/embargo-policy

Since the Embargo policy URL is present, Step 1.7 is activated (not skipped).

## Severity Evaluation

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-31812 |
| CVSS Score | 7.5 |
| Severity Level | High |
| Embargo Threshold | CVSS >= 7.0 (Critical or Important/High) |
| Threshold Met? | **YES** -- 7.5 >= 7.0 |

The CVE severity is **High** (CVSS 7.5), which meets the Critical/Important
threshold (CVSS >= 7.0). The embargo warning gate is triggered.

## Warning Gate Presented to Engineer

The following confirmation prompt is presented to the engineer before proceeding
to Step 2 (Version Impact Analysis):

```
WARNING: EMBARGO CHECK -- CVE-2026-31812 (High severity, CVSS 7.5)

High-severity vulnerabilities may be under embargo.
Before proceeding, verify with your security team that this CVE
is cleared for public triage.

Embargo policy: https://example.com/security/embargo-policy

Proceed with triage? (Yes / No)
```

This is a **confirmation gate**, not an informational message. The triage
**halts at this point** and waits for the engineer's explicit response:

- **If "Yes"**: Proceed to Step 2 (Version Impact Analysis) as normal.
  The engineer has confirmed the CVE is cleared for public triage.
- **If "No"**: Stop execution immediately. Inform the user to check
  embargo status with their security team before re-running triage.
  No Jira mutations occur, no version impact analysis is performed.

## Threshold Behavior

The embargo warning gate applies **only** to Critical and Important/High severity
CVEs (CVSS >= 7.0). For Low or Moderate severity CVEs (CVSS < 7.0), this step
is **skipped silently** -- no warning is displayed, no confirmation is requested,
and triage proceeds directly to Step 2 without interruption.

| Severity | CVSS Range | Embargo Gate |
|----------|------------|--------------|
| Critical | 9.0 - 10.0 | TRIGGERED -- confirmation required |
| High/Important | 7.0 - 8.9 | TRIGGERED -- confirmation required |
| Medium/Moderate | 4.0 - 6.9 | Skipped silently |
| Low | 0.1 - 3.9 | Skipped silently |

## Outcome

For this triage (assuming engineer confirms "Yes"), execution proceeds to
Step 2 -- Version Impact Analysis. The embargo check is consistent with
the existing guardrail pattern where every Jira mutation requires confirmation.
No Jira mutations occur at this step -- the gate fires before any triage
output, so stopping is safe.
