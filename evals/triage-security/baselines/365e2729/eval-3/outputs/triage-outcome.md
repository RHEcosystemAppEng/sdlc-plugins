# Triage Outcome: TC-8003

## Decision: Close as Duplicate of TC-7999

TC-8003 (CVE-2026-31812, quinn-proto < 0.11.14, `[rhtpa-2.2]`) duplicates TC-7999. TC-7999 tracks the same CVE for the same stream (2.2.x) and is already **In Progress**. Under Step 4.1, an open or in-progress same-stream sibling means the current issue is closed as Duplicate. **No remediation tasks are created** from TC-8003.

## Rationale

1. **Same CVE, same stream.** Both issues carry label CVE-2026-31812, component `pscomponent:org/rhtpa-server`, and stream suffix `[rhtpa-2.2]`, which maps to stream 2.2.x.
2. **The sibling is active.** TC-7999 is In Progress, so remediation is already owned. A second tracker would split ownership and risk duplicate remediation tasks.
3. **The analysis confirms the overlap.** The 2.2.x lock file evidence shows 2.2.0 (0.11.9), 2.2.1 (0.11.12), and 2.2.2 (retag of 2.2.1) are affected, while 2.2.3 and 2.2.4 (0.11.14) are not. TC-7999 already covers 2.2.0 and 2.2.1, which includes TC-8003's only Affects Version (2.2.0).
4. **Resolution is Duplicate, not Not a Bug.** The product is affected, so no VEX Justification is set.

## Effect on later steps

- **Step 3 (Affects Versions correction):** not applied to TC-8003 because it is being closed. The proposed set [2.2.0, 2.2.1, 2.2.2] is redirected to TC-7999 as a recommendation to add **RHTPA 2.2.2**.
- **Step 5 (Lifecycle):** not needed for the duplicate closure. External lookups were not made in this eval.
- **Step 6 (Already fixed):** TC-7999 is not resolved (In Progress), so this is not an already-fixed case.
- **Steps 7 and 7.5:** Step 7 is skipped (Upstream Affected Component field not configured). Release Jira orchestration and Step 8 remediation are **not performed** for TC-8003. Remediation (Cargo, fix available upstream on `release/0.4.z` since v0.4.11: dependency bump plus downstream propagation) belongs to TC-7999.

## Proposed Jira mutations (none executed; each needs engineer confirmation)

| # | Issue | Action |
|---|-------|--------|
| 1 | TC-8003 | Assign to current user (Step 0.8) |
| 2 | TC-8003 | Transition New → Assigned (Step 0.8) |
| 3 | TC-8003 | Comment: "Duplicate of TC-7999 — same CVE tracked for the same stream 2.2.x. Version impact analysis confirms overlap." plus impact table and Comment Footnote |
| 4 | TC-8003 | Optional Duplicate link to TC-7999 |
| 5 | TC-8003 | Transition to Closed, resolution **Duplicate** |
| 6 | TC-8003 | Add label `ai-cve-triaged` |
| 7 | TC-8003 | Post-triage summary comment: version impact table, outcome (closed as Duplicate of TC-7999), no Affects Versions correction applied, no remediation tasks or release Jira created, @mention of the PSIRT reporter (account ID from issue data; not in the mock), Comment Footnote |
| 8 | TC-7999 | Advisory comment, if the engineer approves: add RHTPA 2.2.2 to Affects Versions (retag of 2.2.1, quinn-proto 0.11.12); stream 2.1.x (2.1.0 and 2.1.1, quinn-proto 0.11.9) is also affected and has no CVE tracker, so cross-stream handling should happen in TC-7999's triage |

## Warnings and caveats

- **Stale matrix:** security-matrix Last-Updated is 2026-06-28, about 151 days old (threshold 14 days). It may be missing newer 2.2.x releases. Refreshing it is recommended before TC-7999's remediation triage.
- **External enrichment skipped:** MITRE and OSV were not queried, so the fix threshold (0.11.14) comes from the Jira description only.
- **Development stream unknown:** Jira was not queried for unreleased versions. The upstream `release/0.4.z` already ships 0.11.14.
