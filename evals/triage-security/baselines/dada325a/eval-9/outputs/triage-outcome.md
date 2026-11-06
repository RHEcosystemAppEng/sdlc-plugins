# Triage Outcome: TC-8011 (CVE-2026-45678, webpack, [rhtpa-2.2])

## Decision

**Do NOT close TC-8011 as covered by the existing remediation. Proceed to new remediation task creation (Step 8, Case B) for stream 2.2.x.**

## Rationale

1. **Cross-CVE overlap found, but the fix does not cover this CVE.** TC-8012 (CVE-2026-43210) has the same Upstream Affected Component (webpack), PS Component (pscomponent:org/rhtpa-ui), and Stream (rhtpa-2.2). Its Depend-linked remediation task **TC-8013** bumps webpack to **5.96.1**.
2. **Version comparison:** 5.96.1 < **5.98.0**, which is CVE-2026-45678's fix threshold. After TC-8013, rhtpa-ui still ships a webpack version inside the affected range (< 5.98.0). The earlier bump fixed the ReDoS (needed >= 5.96.0) but not the loader-chain code execution flaw.
3. So the "covering remediation" branch of Step 4.3 does not apply. No close recommendation, no Depend link to TC-8013, no overlap-covered comment.

## Remaining steps (summary)

| Step | Result |
|---|---|
| 0.8 Assign / transition | Would assign TC-8011 to the current user and move it from New to Assigned (after confirmation) |
| 1.7 Embargo | Skipped: no Embargo policy URL configured (CVSS 7.8 would otherwise trigger the gate) |
| 2 Version impact | **Blocked on configuration.** npm/rhtpa-ui is not in the 2.2.x Ecosystem Mappings, and the mock data has no webpack lock-file versions. Versions must not be invented. Lock-file evidence is needed before PSIRT's Affects Versions (RHTPA 2.2.0) can be confirmed or corrected. Facts from the overlap check: TC-8013 shipped webpack 5.96.1 for rhtpa-2.2, so any 2.2.x build containing TC-8013 is still vulnerable, and builds before it (5.95.0) are vulnerable too. |
| 3 Affects Versions | Pending Step 2 evidence. Scoped to 2.2.x versions only (2.2.0–2.2.4) |
| 4.1/4.2 Siblings | None for CVE-2026-45678 |
| 4.3 Cross-CVE overlap | TC-8012 / TC-8013 found. **Not covering** (5.96.1 < 5.98.0) |
| 4.4 Preemptive reconciliation | None found |
| 5 Lifecycle | 2.2.x is the latest stream. Would be checked against product pages |
| 6 Already fixed | No resolved same-CVE siblings |
| 7 Concurrent triage | TC-8012 is Closed, not In Progress / Code Review, so it is not a concurrent triage |
| 7.5.3 Dedup | TC-8013 must **not** be treated as covering (closed, and its bump is below the threshold). No dedup skip |
| 8 Remediation | **Case B** (scoped to 2.2.x; Case A cross-stream check depends on whether 2.1.x ships rhtpa-ui/webpack) |

## Proposed remediation (Case B, npm = source dependency → 2 tasks for 2.2.x)

Pending engineer confirmation and Step 2/2.5 evidence:

1. **Upstream task** for rhtpa-ui (2.2.x branch): bump webpack to **>= 5.98.0**. This is a dependency bump if Step 2.5 confirms 5.98.0 is available upstream, otherwise an upstream backport. Labels include `CVE-2026-45678`. Linked to TC-8011 with **Depend**.
2. **Downstream propagation task** (rhtpa-release.0.4.z): pick up the fixed rhtpa-ui build. Blocked by task 1 (**Blocks**), linked to TC-8011 with **Depend**.
3. Link both tasks to the RHTPA 2.2.x release Task (Blocks) and link TC-8011 to the release Task (Related), per Step 7.5.
4. Optionally (informational), create a Related link TC-8011 ↔ TC-8012 because they share an upstream component. Mention TC-8013 in the task Implementation Notes as the previous bump (5.95.0 → 5.96.1), noting that the new bump must reach 5.98.0.

## Post-triage

- Add the `ai-cve-triaged` label to TC-8011.
- Post a summary comment with the version impact table, the overlap finding (TC-8013 at 5.96.1 does not cover the 5.98.0 threshold), the new remediation task keys, release Jira references, and an @mention of the reporter, plus the Comment Footnote.

No Jira mutations, git commands, or external calls were made, per eval instructions.
