# Triage Outcome: TC-8003 (CVE-2026-31812, quinn-proto, [rhtpa-2.2])

## Decision: Close as Duplicate of TC-7999

TC-8003 is a **same-stream duplicate**. The sibling search on label `CVE-2026-31812` returned TC-7999. TC-7999 has the same stream suffix `[rhtpa-2.2]`, is **In Progress**, and already carries Affects Versions [RHTPA 2.2.0, RHTPA 2.2.1]. That is a superset of TC-8003's [RHTPA 2.2.0]. Under Step 4.1, an open or in-progress same-stream sibling means the current issue is closed as Duplicate.

## Why

| Check | Result |
|---|---|
| CVE match | Both issues are CVE-2026-31812 |
| Component match | Both are `pscomponent:org/rhtpa-server` |
| Stream match | Both are `[rhtpa-2.2]`, which maps to 2.2.x |
| Sibling status | TC-7999 is In Progress, so it is open and being worked |
| Version overlap | TC-8003 {2.2.0} is a subset of TC-7999 {2.2.0, 2.2.1} |
| Is the CVE real for 2.2.x? | Yes. Lock files show quinn-proto 0.11.9 (2.2.0) and 0.11.12 (2.2.1, and 2.2.2 by retag), both below the 0.11.14 fix. 2.2.3 and 2.2.4 ship 0.11.14. |

The vulnerability does affect the product, so this is **not** a "Not a Bug" closure (Case C). It is already tracked by TC-7999.

## Actions on TC-8003 (proposed; each needs engineer confirmation; nothing executed)

1. Comment, with the comment footnote: "Duplicate of TC-7999 — same CVE tracked for the same stream [rhtpa-2.2]. Version impact analysis confirms overlap."
2. Transition to **Closed** with resolution **Duplicate**.
3. Assign to the current user.
4. Do **not** correct Affects Versions on TC-8003, because it is being closed. Do **not** create remediation Tasks from TC-8003. Steps 5–8 do not apply to a duplicate, and remediation stays with TC-7999. Creating Tasks here would duplicate TC-7999's work.
5. Post-triage: add the `ai-cve-triaged` label and a short summary comment with the footnote that references TC-7999.

## Recommended follow-ups (for the engineer, on TC-7999)

- **Affects Versions gap:** add **RHTPA 2.2.2**. Its backend is a retag of 2.2.1 (`v0.4.8`, quinn-proto 0.11.12), so it is affected, but TC-7999 does not list it.
- **Cross-stream impact:** the 2.1.x stream (RHTPA 2.1.0 and 2.1.1, quinn-proto 0.11.9) is also affected, and no 2.1.x tracker was found. Report this in a cross-stream comment on TC-7999 (Case A) so PSIRT can create a 2.1.x tracker. This skill does not create Vulnerability issues.
- **Fix status in 2.2.x:** the upstream `release/0.4.z` already ships quinn-proto 0.11.14 from 2.2.3 (`v0.4.11`) onward. Remediation for 2.2.x is mainly a matter of customers moving to 2.2.3 or later, or of confirming that TC-7999's work matches this.
- **Due date:** TC-8003's due date (2026-07-15) has passed. Check TC-7999's due date and SLA.

## Caveats

- MITRE and OSV enrichment was skipped because the eval does not allow external tools. The fix threshold comes only from the Jira description (< 0.11.14).
- The lifecycle check (Step 5) was not run, because there is no product pages access. It does not change the duplicate decision.
- The matrix is about 4 months old (Last-Updated 2026-06-28). Releases after 2.2.4 may be missing, but this does not change the duplicate decision.
