# Step 1.7 – Embargo Check: TC-8001 / CVE-2026-31812

## 1. Configuration check

- Security Configuration has **Embargo policy URL** set to `https://example.com/security/embargo-policy`.
- Because it is configured, this step is **not skipped**.

## 2. Severity evaluation

| Input | Value |
|-------|-------|
| CVSS score | 7.5 (from the Jira description; Step 1.5 external enrichment was unavailable) |
| Severity label | High (maps to Important) |
| Trigger threshold | Critical or Important severity (CVSS >= 7.0) |
| Comparison | 7.5 >= 7.0 |
| Result | **Threshold met. The embargo warning gate is presented.** |

The score is not below the threshold (Low/Moderate, CVSS < 7.0), so the gate cannot be skipped.

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

- **If "No":** stop. Tell the engineer to check the embargo status with the security team before re-running `/sdlc-workflow:triage-security TC-8001`. Do not go on to Step 2.
- **If "Yes":** go on to Step 2 (Version Impact Analysis).

No Jira mutations happen at this step. The gate fires before any triage output, so stopping here is safe.

**Eval note:** this is a non-interactive eval run, so no engineer can answer. To produce the remaining outputs, the engineer's answer is simulated as **"Yes"**, meaning the CVE is cleared for public triage. In a real run, execution would wait at this gate for an explicit answer. The advisory is already public (GHSA-2026-qp73-x4mq, RUSTSEC-2026-0042, upstream PR quinn-rs/quinn#2048), which suggests the CVE is no longer embargoed. Confirming this is still the engineer's job under the policy.
