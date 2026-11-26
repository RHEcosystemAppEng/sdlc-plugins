# Step 1.7 – Embargo Check: CVE-2026-31812 (TC-8001)

## 1. Configuration check

Embargo policy URL **is configured** in Security Configuration -> Product Lifecycle:

- `Embargo policy URL: https://example.com/security/embargo-policy`

Step 1.7 is therefore **not skipped**.

## 2. Severity evaluation

| Input | Value |
|---|---|
| CVSS score (issue description; Step 1.5 external enrichment unavailable) | 7.5 |
| Severity label | High (maps to Important) |
| Jira priority field | not set on the issue |
| Trigger threshold | Critical or Important (CVSS >= 7.0) |
| Comparison | 7.5 >= 7.0 -> **meets threshold** |

The severity is not Low/Moderate (CVSS < 7.0), so the step is not skipped silently. The warning gate fires.

## 3. Warning gate presented to the engineer

```
⚠️ EMBARGO CHECK — CVE-2026-31812 (High severity)

High-severity vulnerabilities may be under embargo.
Before proceeding, verify with your security team that this CVE
is cleared for public triage.

Embargo policy: https://example.com/security/embargo-policy

Proceed with triage? (Yes / No)
```

## 4. Outcome handling

- **No** -> stop execution; tell the engineer to check embargo status with the security team before re-running triage. Do not go on to Step 2.
- **Yes** -> go on to Step 2 (Version Impact Analysis).

No Jira mutations happen at this step. The gate fires before any triage output, so stopping here is safe.
The gate is advisory only. It shows the warning and links the organization's policy; it does not enforce embargo procedures.

**Eval simulation:** this is a non-interactive eval, so the engineer's answer is taken to be **Yes** (cleared for public triage).
The analysis below (version-impact.md, remediation.md) assumes that answer. If the real answer is **No**, everything after this step must be thrown away and not acted on.
