# Triage Outcome: TC-8020 (CVE-2026-31812, quinn-proto)

## Decision

**Paused at Step 7: concurrent triage detected.** Remediation (Step 7.5 / Step 8) is not executed until the engineer chooses Wait, Skip, or Proceed. Recommended: **Wait**, and coordinate with engineer-b@example.com, who owns TC-8019 (In Progress, same upstream component quinn-proto).

## Step-by-step summary

| Step | Result |
|---|---|
| 0 Config | Valid. Upstream Affected Component field customfield_10632 assumed configured. |
| 0.3 Staleness | Matrix 151 days old (2026-06-28). Warning raised. Proceeded with the mock matrix for the eval. |
| 0.6 Mode | Interactive (no FULLSEND_OUTPUT_DIR). |
| 0.8 Assign | Would propose: assign to current user and move New -> Assigned. Not executed. |
| 1 Extraction | CVE-2026-31812, quinn-proto < 0.11.14, fix 0.11.14, CVSS 7.5. Scoped to stream 2.2.x. Ecosystem Cargo. |
| 1.5 Enrichment | Skipped (no external calls). Used Jira data only, at reduced confidence. |
| 1.7 Embargo | Skipped (no policy URL configured). |
| 2 Impact | 2.2.0, 2.2.1, 2.2.2 (retag of 2.2.1) affected. 2.2.3 and 2.2.4 not affected (0.11.14). 2.1.0 and 2.1.1 affected (cross-stream). |
| 3 Affects Versions | Proposed correction: `[RHTPA 2.0.0] -> [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]`. Needs confirmation. |
| 4 Siblings/overlap | No sibling data provided. 4.3 cross-CVE overlap needs the PS Component and Stream fields, which are not configured, so it is skipped. |
| 5 Lifecycle | Not evaluated (no product-pages access). Assumed supported. |
| 6 Already fixed | No resolved siblings known. |
| **7 Concurrent triage** | **TC-8019 (In Progress, engineer-b@example.com) on quinn-proto. Execution halted pending engineer choice.** |
| 7.5 / 8 | Not reached. |

## What happens after each choice

- **Wait**: stop now. Re-run after TC-8019 completes, so that Step 4.3 and Step 7.5.3 can detect TC-8019's quinn-proto remediation and link TC-8020 to it instead of creating duplicates.
- **Skip**: no remediation tasks. Post an explanatory comment on TC-8020 (with Comment Footnote).
- **Proceed**: add the `concurrent-triage-overlap` label to TC-8020, then continue:
  - Step 7.5: find or create the release Epic/Task for the affected 2.2.x release (and 2.1.x for preemptive work). Each creation needs individual confirmation.
  - **Case A** (scoped issue, other stream affected): post a cross-stream impact comment saying quinn-proto < 0.11.14 also affects 2.1.x (2.1.0, 2.1.1). If no 2.1.x CVE Jira exists, create preemptive tasks labelled `security-preemptive` with a Related link.
  - **Case B** (2.2.x affected): 2 Cargo tasks for 2.2.x. The fix is already on `release/0.4.z` (v0.4.11+ ships 0.11.14), so use the dependency-bump/fix-available variant plus downstream propagation. Link both tasks to TC-8020 (Depend) and to the release Task (Blocks).
  - Note: 2.2.3 and later already ship the fix. The engineer may decide that shipping 2.2.3+ is enough for the 2.2.x stream. That is a remediation-scope judgment for the confirmation gate.
  - Post-triage: add the `ai-cve-triaged` label and post a summary comment with an @mention of the reporter and the Comment Footnote.

## Mutations performed

None. This eval forbids Jira/git calls, and the concurrent-triage gate needs an engineer decision first.
