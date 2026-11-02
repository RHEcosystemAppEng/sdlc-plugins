# Step 0 — Configuration Extraction

The Security Configuration in the CLAUDE.md includes the following optional field:

- **Embargo policy URL**: `https://example.com/security/embargo-policy`

This field is extracted as an optional configuration value during Step 0. Its presence enables Step 1.7 (Embargo Check). If this field were absent, Step 1.7 would be skipped entirely.

# Step 1.7 — Embargo Check

## Severity Evaluation

The CVE severity is determined from the data extracted in Step 1:

- **CVSS Score**: 7.5
- **Severity Level**: High
- **Threshold**: Critical or Important severity (CVSS >= 7.0)
- **Result**: **CVSS 7.5 >= 7.0 — threshold met, embargo warning gate triggered**

## Embargo Warning Gate

The following warning gate is presented to the engineer. This is a **confirmation prompt** that requires explicit Yes/No input before triage can proceed to Step 2:

```
⚠️ EMBARGO CHECK — CVE-2026-31812 (High severity, CVSS 7.5)

High-severity vulnerabilities may be under embargo.
Before proceeding, verify with your security team that this CVE
is cleared for public triage.

Embargo policy: https://example.com/security/embargo-policy

Proceed with triage? (Yes / No)
```

## Decision Handling

- **If "Yes"**: Proceed to Step 2 (Version Impact Analysis) as normal. No Jira mutations occur at this step — the gate fires before any triage output, so stopping is safe.
- **If "No"**: Stop execution immediately and inform the user to check embargo status before re-running triage. Do not proceed to Step 2.

## Severity Threshold Behavior

The embargo warning gate is threshold-based:
- **CVSS >= 7.0** (Critical/Important): Gate **triggers** — warning presented, confirmation required
- **CVSS < 7.0** (Low/Moderate): Gate is **skipped silently** — no warning, no user prompt, triage proceeds directly to Step 2

For this CVE (CVSS 7.5, High severity), the gate is triggered because 7.5 >= 7.0.

## Consistency with Guardrails

This gate follows the existing guardrail pattern: every significant triage action requires engineer confirmation. No Jira mutations occur at Step 1.7 — the gate fires before any triage output, making it safe to stop without side effects.
