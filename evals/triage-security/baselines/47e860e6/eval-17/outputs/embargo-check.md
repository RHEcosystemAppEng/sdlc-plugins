# TC-8001 — Step 1.7 Embargo Check

## 1. Configuration check
Security Configuration → Product Lifecycle has
`Embargo policy URL: https://example.com/security/embargo-policy`.
The URL is configured, so the step runs. It is not skipped.

## 2. Severity evaluation

| Input | Value |
|---|---|
| CVSS score | 7.5 (from issue description; Step 1.5 external sources unavailable) |
| Severity label | High (Important) |
| Trigger threshold | Critical or Important, i.e. CVSS >= 7.0 |
| Result | 7.5 >= 7.0, so the threshold is **MET** and the warning gate fires |

For contrast, a Low or Moderate CVE (CVSS < 7.0) would skip this step silently and go straight to
Step 2. Nothing would be shown to the engineer. That is not the case here.

## 3. Warning gate presented to the engineer

```
⚠️ EMBARGO CHECK — CVE-2026-31812 (High severity, CVSS 7.5)

High-severity vulnerabilities may be under embargo.
Before proceeding, verify with your security team that this CVE
is cleared for public triage.

Embargo policy: https://example.com/security/embargo-policy

Proceed with triage? (Yes / No)
```

This is a blocking confirmation prompt, not an informational notice. Execution stops here until
the engineer gives an explicit answer.

- **No**: stop execution. Tell the engineer to confirm the embargo status with the security
  team before re-running triage. Step 2 does not run and nothing is written to Jira.
- **Yes**: proceed to Step 2 (Version Impact Analysis).

No Jira mutations happen at this step, so stopping here is safe.

## 4. Engineer response (simulated for eval)
In this eval the engineer answers **Yes**, confirming that CVE-2026-31812 is cleared for public
triage. The triage then continues to Step 2. The gate is advisory: the skill links the policy but
does not enforce embargo procedures itself.
