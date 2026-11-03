# Step 4 – Duplicate, Sibling, and Overlap Check: TC-8003

## JQL search (simulated)

```
project = TC AND labels = 'CVE-2026-31812' AND issuetype = 10024 AND key != TC-8003
```

Result (given by the eval): 1 issue.

| Issue | Summary suffix | Stream | Status | Affects Versions |
|---|---|---|---|---|
| TC-7999 | [rhtpa-2.2] | 2.2.x | In Progress | RHTPA 2.2.0, RHTPA 2.2.1 |
| TC-8003 ← (current) | [rhtpa-2.2] | 2.2.x | New | RHTPA 2.2.0 |

## Classification

- TC-7999 has the same stream suffix `[rhtpa-2.2]` as TC-8003, so it is a **same-stream sibling**.
- TC-7999 is open (In Progress), so the **4.1 same-stream duplicate** rule applies.
- No different-stream siblings were found, so 4.2 cross-stream link creation does not apply.

## 4.1 – Same-stream duplicate verdict

**TC-8003 is a duplicate of TC-7999.** Both issues track CVE-2026-31812 (quinn-proto < 0.11.14) for the same component (`pscomponent:org/rhtpa-server`) and the same stream (2.2.x). TC-7999 is already being worked on.

Version impact overlap check:

| Version | Affected (lock file evidence) | On TC-7999 | On TC-8003 |
|---|---|---|---|
| RHTPA 2.2.0 | YES (0.11.9) | yes | yes |
| RHTPA 2.2.1 | YES (0.11.12) | yes | no |
| RHTPA 2.2.2 | YES (retag of 2.2.1) | **no** | no |
| RHTPA 2.2.3 | NO (0.11.14) | no | no |
| RHTPA 2.2.4 | NO (0.11.14) | no | no |

- TC-8003's Affects Versions (2.2.0) is a strict subset of TC-7999's, which confirms the overlap.
- **Gap found on TC-7999:** RHTPA 2.2.2 ships the vulnerable quinn-proto 0.11.12, because its backend is a retag of 2.2.1. TC-7999 does not list it. The engineer should add RHTPA 2.2.2 to TC-7999's Affects Versions. This needs confirmation, a comment, and the comment footnote.

## Proposed actions (each needs engineer confirmation; none were executed)

1. Add a comment to TC-8003:
   > Duplicate of TC-7999 — same CVE (CVE-2026-31812) tracked for the same stream [rhtpa-2.2]. Version impact analysis confirms overlap: lock file evidence shows RHTPA 2.2.0, 2.2.1 and 2.2.2 (retag of 2.2.1) ship quinn-proto < 0.11.14; 2.2.3+ ship 0.11.14 (fixed). TC-8003's Affects Versions [RHTPA 2.2.0] is fully covered by TC-7999.
   >
   > _(Comment footnote per shared/comment-footnote.md, skill: triage-security)_
2. Transition TC-8003 to **Closed**, resolution **Duplicate**.
3. Assign TC-8003 to the current user.
4. Recommended follow-up on TC-7999: add RHTPA 2.2.2 to Affects Versions and post a comment with the footnote explaining the retag evidence.
5. Optionally, add a Duplicate/Related link from TC-8003 to TC-7999 so the two issues stay connected.

## 4.2 – Cross-stream note

Lock file evidence shows that **stream 2.1.x is also affected** (RHTPA 2.1.0 and 2.1.1 ship quinn-proto 0.11.9). The JQL search found no 2.1.x companion tracker for this CVE. Under Rule 7, this skill does not create Vulnerability issues. Cross-stream impact should be reported in a comment on the surviving issue (TC-7999), so PSIRT can create or adjust a 2.1.x tracker. Do not put it on TC-8003, which will be closed.

## 4.3 / 4.4

- 4.3 cross-CVE overlap: this needs the Upstream Affected Component field, which is not configured. Skipped.
- 4.4 preemptive task reconciliation: no data was provided. Not applicable, because remediation stays with TC-7999.
