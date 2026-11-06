# Step 1.7 – Embargo Check: CVE-2026-31812 (TC-8001)

## 1. Configuration check

| Check | Result |
|-------|--------|
| Embargo policy URL configured in Security Configuration? | **Yes** — `https://example.com/security/embargo-policy` |
| Action | Step 1.7 is NOT skipped; proceed to severity evaluation |

## 2. Severity evaluation

| Input | Value |
|-------|-------|
| CVSS score (Jira description; Step 1.5 enrichment unavailable) | **7.5** |
| Severity label | **High** (maps to Important) |
| Trigger threshold | Critical or Important severity (CVSS >= 7.0) |
| Comparison | 7.5 >= 7.0 |
| Threshold met? | **YES** — the warning gate fires |

Because the severity is not Low/Moderate (CVSS < 7.0), the silent-skip path does not
apply.

## 3. Warning gate presented to the engineer

```
⚠️ EMBARGO CHECK — CVE-2026-31812 (High severity)

High-severity vulnerabilities may be under embargo.
Before proceeding, verify with your security team that this CVE
is cleared for public triage.

Embargo policy: https://example.com/security/embargo-policy

Proceed with triage? (Yes / No)
```

## 4. Gate outcome handling

- **If "No"**: stop execution. Inform the user to check embargo status with the
  security team (per https://example.com/security/embargo-policy) before re-running
  `/sdlc-workflow:triage-security TC-8001`. Do not proceed to Step 2.
- **If "Yes"**: proceed to Step 2 (Version Impact Analysis).

Eval simulation: the engineer's response is assumed to be **"Yes"** (CVE cleared for
public triage), so triage continues to Step 2.

## Notes

- This gate is advisory — it does not enforce embargo procedures; it surfaces the
  warning and links the policy for engineer verification.
- No Jira mutations have occurred before or at this step (Step 0.8 assignment is
  simulated only), so stopping here would be safe.
- Public-facing artifacts (e.g., the upstream PR to rhtpa-backend) must respect the
  embargo policy if the CVE is not yet public.
