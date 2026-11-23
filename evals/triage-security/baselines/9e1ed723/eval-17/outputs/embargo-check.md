# Step 1.7 – Embargo Check: TC-8001 / CVE-2026-31812

## 1. Configuration check

- Embargo policy URL in Security Configuration: **https://example.com/security/embargo-policy**
- The URL is configured, so the step is **active** and is not skipped.

## 2. Severity evaluation

| Input | Value |
|-------|-------|
| CVSS score | 7.5 (from the TC-8001 description; Step 1.5 external enrichment was not available) |
| Severity label | High (maps to Critical/Important tier) |
| Trigger threshold | Critical or Important severity (CVSS >= 7.0) |
| Comparison | 7.5 >= 7.0 |
| Result | **Threshold met. Present the embargo warning gate.** |

The "below threshold, skip silently" path (CVSS < 7.0, Low/Moderate) does not apply.

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

- **If "No"**: stop. Tell the engineer to check embargo status with the security team before re-running `/sdlc-workflow:triage-security TC-8001`. Do not go on to Step 2.
- **If "Yes"**: continue to Step 2 (Version Impact Analysis).

No Jira mutations happen at this step. The gate runs before any triage output, so stopping here is safe. The gate is advisory: it surfaces the warning and the policy link but does not enforce embargo procedures.

Note: the CVE already has public references (a GHSA advisory, a RUSTSEC advisory, and a public upstream PR, quinn-rs/quinn#2048). That suggests the CVE is public, but the skill still requires the engineer to confirm explicitly.

**Eval assumption:** no engineer is available in this run. To produce the remaining outputs, the engineer's answer is treated as **"Yes"**. In a real run, execution would pause here until the engineer answers.
