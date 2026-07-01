# Step 1.7 -- Embargo Check

## Step 0 -- Configuration Extraction

The Security Configuration in the project CLAUDE.md includes the following optional field:

- **Embargo policy URL**: `https://example.com/security/embargo-policy`

This field was extracted as an optional configuration value during Step 0 (Validate Project Configuration). Its absence would not raise an error -- if not configured, Step 1.7 would be skipped entirely. In this case, the field is present and its value is recorded for use in the embargo warning gate below.

## Severity Evaluation

The CVE severity was extracted from the Jira issue description in Step 1:

- **CVSS score**: 7.5
- **Severity level**: High

The embargo warning gate trigger threshold is **Critical or Important severity (CVSS >= 7.0)**.

**Evaluation**: CVSS 7.5 >= 7.0 -- the threshold **is met**. The embargo warning gate is triggered.

Note: For CVEs with Low or Moderate severity (CVSS < 7.0), this step would be skipped silently and triage would proceed directly to Step 2 without any warning or user prompt.

## Embargo Warning Gate

The following warning gate is presented to the engineer and requires explicit confirmation before triage can proceed:

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

## Confirmation Behavior

This is a **confirmation prompt**, not an informational message. The engineer must explicitly respond:

- **If "Yes"**: Triage proceeds to Step 2 (Version Impact Analysis) as normal. The embargo check is recorded as acknowledged.
- **If "No"**: Execution stops immediately. The engineer is informed to check embargo status with their security team before re-running triage. No Jira mutations occur, no version impact analysis is performed, and no remediation tasks are created.

This gate is consistent with the existing guardrail pattern that every significant triage action requires explicit engineer confirmation. Because no Jira mutations have occurred at this point in the flow (Step 1.7 fires before any triage output), stopping is safe and does not leave partial state.

## Outcome

For this triage session, we assume the engineer confirms **Yes** and triage proceeds to Step 2.
