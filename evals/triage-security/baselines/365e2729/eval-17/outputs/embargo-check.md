# TC-8001 — Step 1.7 Embargo Check

## 1. Configuration check

- Security Configuration → Product Lifecycle has `Embargo policy URL: https://example.com/security/embargo-policy`.
- The URL is configured, so the step is **not skipped**. (If the URL were absent, Step 1.7 would be skipped silently and triage would go straight to Step 2.)

## 2. Severity evaluation

| Input | Value | Source |
|---|---|---|
| CVSS score | 7.5 | Jira description (Step 1). Step 1.5 external data was unavailable in this eval |
| Severity label | High (Important) | Jira description |
| Trigger threshold | Critical or Important, CVSS >= 7.0 | SKILL.md Step 1.7 |
| Comparison | 7.5 >= 7.0 | — |
| **Result** | **Threshold met. Embargo warning gate triggered** | — |

Below-threshold behavior: Low or Moderate severity (CVSS < 7.0) skips this step **silently**, with no warning and no prompt, and goes on to Step 2. That path does not apply to this CVE.

## 3. Warning gate presented to the engineer

```
⚠️ EMBARGO CHECK — CVE-2026-31812 (High severity)

High-severity vulnerabilities may be under embargo.
Before proceeding, verify with your security team that this CVE
is cleared for public triage.

Embargo policy: https://example.com/security/embargo-policy

Proceed with triage? (Yes / No)
```

This is a **blocking confirmation prompt**, not an informational notice. Triage does not continue to Step 2 until the engineer answers explicitly.

## 4. Gate outcomes

- **No**: stop execution. Tell the engineer: "Triage halted. Please confirm the embargo status of CVE-2026-31812 with your security team (see https://example.com/security/embargo-policy) before re-running `/sdlc-workflow:triage-security TC-8001`." Step 2 is not run.
- **Yes**: go on to Step 2 (Version Impact Analysis).

No Jira mutations happen at this step. The gate fires before any triage output, so stopping is safe.

## 5. Simulated engineer response (eval)

Engineer response: **Yes**. The CVE is cleared for triage; it already has a public GHSA, a RUSTSEC advisory and a merged upstream PR. Triage goes on to Step 2.
