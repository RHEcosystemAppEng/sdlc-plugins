# Step 1.7 – Embargo Check: CVE-2026-31812 (TC-8001)

## 1. Configuration check

- Embargo policy URL in Security Configuration → Product Lifecycle: **https://example.com/security/embargo-policy**
- The URL is configured, so this step is **not skipped**.

## 2. Severity evaluation

| Input | Value |
|-------|-------|
| CVSS score | 7.5 (from the TC-8001 description; Step 1.5 external enrichment was unavailable in this eval) |
| Severity label | High. This maps to the Critical/Important band |
| Trigger threshold | Critical or Important severity (CVSS >= 7.0) |
| Comparison | 7.5 >= 7.0 |
| **Result** | **Threshold met, so the embargo warning gate is presented** |

The skip rule does not apply here. It only covers Low or Moderate severity (CVSS < 7.0).

## 3. Warning gate presented to the engineer

```
⚠️ EMBARGO CHECK — CVE-2026-31812 (High severity, CVSS 7.5)

High-severity vulnerabilities may be under embargo.
Before proceeding, verify with your security team that this CVE
is cleared for public triage.

Embargo policy: https://example.com/security/embargo-policy

Proceed with triage? (Yes / No)
```

## 4. Gate behaviour

- **No**: stop execution. Tell the engineer to confirm the embargo status with the security team before re-running `/sdlc-workflow:triage-security TC-8001`. Do not proceed to Step 2.
- **Yes**: proceed to Step 2 (Version Impact Analysis).
- No Jira mutations happen at this step. The gate fires before any triage output, so stopping is safe.
- The gate is advisory. The skill does not enforce embargo procedures; it only shows the warning and links to the policy.

## 5. Outcome in this eval

The gate is presented above. This is a non-interactive eval run, so the rest of the analysis (version-impact.md, remediation.md) assumes the engineer answered **Yes**. In a real session, the skill must wait for an explicit answer before going any further.
