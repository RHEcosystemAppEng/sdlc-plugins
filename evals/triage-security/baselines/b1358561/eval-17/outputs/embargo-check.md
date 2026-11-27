# Step 1.7 – Embargo Check: CVE-2026-31812 (TC-8001)

## 1. Configuration check

- Embargo policy URL configured in Security Configuration > Product Lifecycle:
  **https://example.com/security/embargo-policy**
- Result: **configured**, so the step is not skipped.

## 2. Severity evaluation

| Input | Value |
|-------|-------|
| CVSS score | 7.5 |
| Severity rating | High (Important) |
| Source | Jira description (`**CVSS**: 7.5 (High)`). Step 1.5 external enrichment was unavailable in this eval. |
| Trigger threshold | Critical or Important severity (CVSS >= 7.0) |
| Comparison | 7.5 >= 7.0 |
| **Threshold met?** | **YES** |

The CVSS score is not below 7.0 (Low/Moderate), so the step is not silently skipped.
The warning gate fires.

## 3. Warning gate presented to the engineer

```
⚠️ EMBARGO CHECK — CVE-2026-31812 (High severity)

High-severity vulnerabilities may be under embargo.
Before proceeding, verify with your security team that this CVE
is cleared for public triage.

Embargo policy: https://example.com/security/embargo-policy

Proceed with triage? (Yes / No)
```

## 4. Gate handling

- **If "No"**: stop execution. Tell the user to check embargo status with the security
  team, following https://example.com/security/embargo-policy, before re-running
  `/sdlc-workflow:triage-security TC-8001`. Do not continue to Step 2. Nothing has
  changed in Jira at this point, so stopping is safe.
- **If "Yes"**: continue to Step 2 (Version Impact Analysis).

This gate is advisory. It does not enforce the embargo procedure. It shows the warning
and links to the organization's policy so the engineer can verify the CVE's status. No
Jira mutations happen at this step.

## 5. Eval note

No interactive engineer is available in this eval run. The remaining outputs
(`version-impact.md`, `remediation.md`) show the analysis **as it would continue after
the engineer answers "Yes"**. Nothing should be published to Jira until the engineer
confirms the embargo clearance.

The CVE has public references (GHSA advisory, cve.org record, RustSec advisory, and a
public upstream PR, quinn-rs/quinn#2048). These suggest the CVE is already public.
That is context for the engineer only. It does not replace the confirmation.
