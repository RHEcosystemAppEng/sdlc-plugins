# Step 1.7 -- Embargo Check

## Configuration

Embargo policy URL is configured in Security Configuration:
- **Embargo policy URL**: https://example.com/security/embargo-policy

Since an Embargo policy URL is configured, Step 1.7 is **not** skipped.

## Severity Evaluation

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-31812 |
| CVSS Score | 7.5 |
| Severity Level | High |
| Threshold | CVSS >= 7.0 (Critical/Important) |
| Threshold Met? | **YES** -- 7.5 >= 7.0 |

The CVE severity (CVSS 7.5, High) meets the Critical/Important threshold
(CVSS >= 7.0). This triggers the embargo warning gate.

**Note**: If the severity were Low or Moderate (CVSS < 7.0), this step would be
skipped silently and triage would proceed directly to Step 2 without presenting
any warning.

## Embargo Warning Gate

The following warning gate is presented to the engineer. Triage **does not proceed**
to Step 2 until the engineer provides an explicit Yes/No confirmation.

```
EMBARGO CHECK -- CVE-2026-31812 (High severity, CVSS 7.5)

High-severity vulnerabilities may be under embargo.
Before proceeding, verify with your security team that this CVE
is cleared for public triage.

Embargo policy: https://example.com/security/embargo-policy

Proceed with triage? (Yes / No)
```

## Behavior on Response

- **If "Yes"**: Proceed to Step 2 (Version Impact Analysis) as normal.
  The embargo check is complete and no further gates are presented.

- **If "No"**: Stop execution immediately. Inform the user:
  "Triage halted -- please verify embargo status for CVE-2026-31812 with your
  security team before re-running triage."
  No Jira mutations have occurred beyond Step 0.7 (assignment and Assigned transition),
  so stopping is safe.

## Confirmation

For this eval, we assume the engineer confirms **Yes** -- proceed with triage.
The embargo warning gate has been presented and acknowledged. Triage continues
to Step 2.

## Important Notes

- This gate is consistent with the existing guardrail pattern: every Jira mutation
  requires confirmation. No Jira mutations occur at this step -- the gate fires
  before any triage output, so stopping is safe.
- The gate is a **confirmation prompt**, not an informational message. The engineer
  must explicitly choose Yes or No before the skill proceeds.
- The embargo warning gate does NOT trigger for Low or Moderate severity CVEs
  (CVSS < 7.0). It is skipped silently when severity is below threshold.
