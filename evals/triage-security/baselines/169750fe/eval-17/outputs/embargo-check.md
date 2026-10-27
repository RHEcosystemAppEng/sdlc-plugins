# Step 1.7 -- Embargo Check

## Configuration

- Embargo policy URL: https://example.com/security/embargo-policy (configured in Security Configuration)

Since an Embargo policy URL **is** configured, this step is **not** skipped.

## Severity Evaluation

| Metric | Value |
|--------|-------|
| CVE ID | CVE-2026-31812 |
| CVSS Score | 7.5 |
| Severity | High |
| Threshold | >= 7.0 (Critical/Important) |
| Threshold met? | **YES** -- 7.5 >= 7.0 |

The CVSS score of 7.5 (High severity) meets the Critical/Important threshold (>= 7.0). The embargo warning gate is triggered.

## Embargo Warning Gate

The following warning gate is presented to the engineer for confirmation before proceeding:

---

**EMBARGO CHECK -- CVE-2026-31812 (High severity)**

High-severity vulnerabilities may be under embargo.
Before proceeding, verify with your security team that this CVE
is cleared for public triage.

Embargo policy: https://example.com/security/embargo-policy

Proceed with triage? (Yes / No)

---

## Gate Behavior

- If the engineer responds **"Yes"**: proceed to Step 2 (Version Impact Analysis) as normal.
- If the engineer responds **"No"**: stop execution immediately. The engineer must check embargo status with their security team before re-running triage. No triage output, Jira mutations, or version analysis occurs.

## Low/Moderate Severity Behavior

For reference: if this CVE had a CVSS score below 7.0 (Low or Moderate severity), this step would be **skipped silently** -- no warning gate would be presented and triage would proceed directly to Step 2 without interruption. The embargo check only triggers for Critical/Important severity (CVSS >= 7.0).
