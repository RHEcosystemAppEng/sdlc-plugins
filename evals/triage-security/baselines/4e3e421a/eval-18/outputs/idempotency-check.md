# TC-8001: Idempotency Check (Re-run)

Before proposing any write, each mutation the triage-security workflow could make was compared against the artifacts already on TC-8001 from the earlier run (2026-07-01, skill v0.11.1).

## Summary of detected artifacts

| # | Artifact | Evidence on the issue | Workflow step that would create it | Re-run decision |
|---|---|---|---|---|
| 1 | `ai-cve-triaged` label | Labels: `CVE-2026-31812, pscomponent:org/rhtpa-server, ai-cve-triaged` | Post-Triage Summary §1 | **SKIP**: label already present; nothing is added |
| 2 | Status In Progress | Status: In Progress | Step 0.8 (transition to Assigned); earlier run also moved it to In Progress | **SKIP**: issue is already past Assigned, so no transition is made |
| 3 | Assignee | engineer-a@example.com | Step 0.8 (assign to current user) | **NO-OP**: the issue is already assigned to the triaging engineer. A re-assign to the same account changes nothing. If a different engineer re-ran this, reassignment would be the only change and would need explicit confirmation |
| 4 | Remediation task: upstream backport | Depend link to **TC-8100** ("Backport quinn-proto fix to >= 0.11.14 on release/0.4.z [rhtpa-2.2]", In Progress, labels ai-generated-jira/Security/CVE-2026-31812) | Step 8 Case B, task 1 for stream 2.2.x | **SKIP**: remediation already exists for stream 2.2.x; no new task is created |
| 5 | Remediation task: downstream propagation | Depend link to **TC-8101** ("Propagate quinn-proto bump to rhtpa-server release branch [rhtpa-2.2]", Open) | Step 8 Case B, task 2 for stream 2.2.x | **SKIP**: already exists; no new task is created |
| 6 | Depend links CVE to tasks | Depend: TC-8001 to TC-8100, TC-8001 to TC-8101 | Step 8 Case B "Link each Task to the Vulnerability issue" | **SKIP**: `issuelinks` already has `type.name = "Depend"` for both keys (same existing-link check as Steps 4.2 and 4.3b) |
| 7 | Blocks link upstream to downstream | TC-8101 is blocked by TC-8100 | Step 8 linkage (upstream Blocks downstream) | **SKIP**: link already exists |
| 8 | Description digest comment | Comment 1: `[sdlc-workflow] Description digest: sha256-md:a1b2c3d4...a1b2`, posted by sdlc-workflow/triage-security | Remediation Task Creation (posted right after each task is created) | **SKIP**: the digest is posted only as part of creating a task. No task is created, so no digest is posted, and the existing digest is not duplicated |
| 9 | Post-triage summary comment | Comment 2: "Triage complete for CVE-2026-31812 (quinn-proto)…" with Comment Footnote (`sdlc-workflow/triage-security` v0.11.1) | Post-Triage Summary §2 | **SKIP**: a triage-security summary already exists; no second summary is posted |
| 10 | Affects Versions correction and its comment | Affects Versions = RHTPA 2.2.0, RHTPA 2.2.1; summary says "Affects Versions corrected to RHTPA 2.2.0, RHTPA 2.2.1" | Step 3.2 | **SKIP re-applying the earlier correction**: the field already holds the values the earlier run set, so the same edit and comment are not repeated. See the evidence note below about RHTPA 2.2.2 |

## Steps that produce no mutation for other reasons

| Step | Result |
|---|---|
| 0.3 Matrix staleness | 128 days old; warning only. A refresh would write only the local matrix, never Jira |
| 1.5 Enrichment | External sources unavailable in this eval; Jira description threshold 0.11.14 used |
| 1.7 Embargo | Skipped (no policy URL configured) |
| 4.1 / 4.2 Siblings | JQL not run (no Jira calls in this eval). The Related-link check is idempotent: any sibling already linked through `Related` is skipped. This issue has no Related links, so one could not be confirmed either way |
| 4.3 Cross-CVE overlap | Skipped: the Upstream Affected Component, PS Component and Stream field IDs are not configured in Security Configuration |
| 4.4 Preemptive reconciliation | Not applicable: TC-8100 and TC-8101 carry no `security-preemptive` label and are already linked through Depend |
| 5 Lifecycle | Not fetched in this eval; no closure is proposed |
| 6 Already fixed | No resolved sibling evidence available; not triggered |
| 7 Concurrent triage | Skipped (Upstream Affected Component field not configured) |
| 7.5.3 Cross-CVE dedup | Same result as artifacts 4 and 5: existing remediation for this CVE and stream means "dedup'd", so no task creation |

## Evidence notes for the engineer (not executed; listed for transparency)

These are findings, not idempotent re-applications. Under the skill guardrails each would need explicit engineer confirmation and is **not** carried out in this run:

1. **RHTPA 2.2.2 looks affected but is missing from Affects Versions.** The matrix shows 2.2.2 uses backend `v0.4.8`, a retag of 2.2.1, which ships quinn-proto 0.11.12. Under Important Rule 5, retag results carry forward, so 2.2.2 is YES. The earlier summary says "RHTPA 2.2.2 and later ship quinn-proto 0.11.14", which contradicts the current matrix. A Step 3.2 "correct but incomplete" proposal would be `[RHTPA 2.2.0, RHTPA 2.2.1] -> [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]`. It is shown for confirmation and not applied. The existing tasks TC-8100 and TC-8101 already cover stream 2.2.x, so no extra remediation task would be needed either way.
2. **Upstream fix appears to have shipped already.** `release/0.4.z` ships quinn-proto 0.11.14 from v0.4.11 (RHTPA 2.2.3) onward. TC-8100's backport may already be satisfied. The engineer may want to check TC-8100 and TC-8101 status. The skill does not change existing tasks.
3. **Cross-stream (2.1.x) impact.** RHTPA 2.1.0 and 2.1.1 ship 0.11.9, so they are affected. The earlier summary does not record Case A handling. Whether a 2.1.x sibling CVE Jira exists needs Step 4 JQL, which this eval forbids. Any Case A comment or preemptive task would also need confirmation.
4. **Release Jira (Step 7.5).** The earlier summary records no release Epic or Task. Find-or-create needs Jira queries and per-item confirmation, so none was done here.
5. The digest comment in the mock sits on TC-8001. The protocol posts digests on each remediation task. Whether TC-8100 and TC-8101 each have their own digest cannot be checked without Jira. The re-run creates no tasks, so it posts no digests.
