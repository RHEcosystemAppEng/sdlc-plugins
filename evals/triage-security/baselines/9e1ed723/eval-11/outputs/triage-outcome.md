# Triage Outcome: TC-8021 (CVE-2026-55123, tokio, [rhtpa-2.1])

## Summary

**Outcome: affected (Case B path), with remediation reconciled to the existing preemptive task TC-8022. No new remediation tasks are created.**

TC-8021 is the PSIRT-created stream-specific CVE Jira for 2.1.x. A prior triage of the companion issue TC-8020 ([rhtpa-2.2]) ran Case A cross-stream remediation. At that time 2.1.x had no CVE Jira of its own, so it created the preemptive task **TC-8022** ("Remediate CVE-2026-55123: bump tokio to 1.42.0 (rhtpa-2.1)"). That task carries the `security-preemptive` label and is linked to TC-8020 with **Related**.

Now that PSIRT has created TC-8021 for this stream, Step 4.4 reconciles the two.

## How the preemptive task was reconciled

1. **Found.** The JQL `labels = 'security-preemptive' AND labels = 'CVE-2026-55123'` returned TC-8022.
2. **Matched.** The TC-8022 summary contains `(rhtpa-2.1)`, which matches TC-8021's stream suffix `[rhtpa-2.1]` (stream 2.1.x). Its CVE label matches and its status is Open.
3. **Linked.** The proposal is to create a **Depend** link TC-8021 -> TC-8022, the standard remediation linkage between a CVE Jira and its own remediation task. TC-8021 had no existing links, so the idempotency check passes.
4. **Label removed.** The proposal is to remove `security-preemptive` from TC-8022. The resulting labels are `ai-generated-jira, Security, CVE-2026-55123`. The task becomes a standard remediation task for TC-8021, and its Related link to TC-8020 stays for cross-stream traceability.
5. **Recorded.** Stream 2.1.x is marked as reconciled to TC-8022, so Step 8 skips task creation for this stream.

## Remaining steps

| Step | Result |
|---|---|
| 0.3 Matrix staleness | Matrix is 148 days old (last updated 2026-06-28). The engineer is warned; this eval assumes "Proceed anyway" |
| 1.5 External enrichment | MITRE/OSV unavailable (external calls forbidden). Using the Jira threshold: fixed in tokio 1.42.0 |
| 1.7 Embargo | Skipped (no Embargo policy URL configured) |
| 2 Version impact | 2.1.0 (`v0.3.8`) and 2.1.1 (`v0.3.12`) are presumed affected. The mock data has no tokio lock-file entries, so `git show <tag>:Cargo.lock` confirmation is still pending. No version is fabricated |
| 3 Affects Versions | RHTPA 2.1.0 and 2.1.1 already match the stream scope, so no correction is needed |
| 4.1/4.2 Siblings | TC-8020 [rhtpa-2.2] is a cross-stream companion. A Related link is proposed |
| 4.3 Cross-CVE overlap | Skipped (custom field IDs not configured in Security Configuration) |
| 4.4 Preemptive reconciliation | **TC-8022 reconciled** (Depend link plus label removal) |
| 5 Lifecycle | Requires the Product pages fetch (not performed). Assumed supported unless shown otherwise |
| 6 Already fixed | No resolved same-CVE sibling covers 2.1.x |
| 7 Concurrent triage | Skipped (Upstream Affected Component field not configured) |
| 7.5 Release Jira | Find or create "RHTPA 2.1.x CVE triage" for the next 2.1 release. If active, propose linking TC-8022 -> release Task (Blocks; it is now non-preemptive) and TC-8021 -> release Task (Related) |
| 8 Remediation | Case B for 2.1.x. **Task creation is skipped because of the Step 4.4 reconciliation (TC-8022).** Case A does not apply: the out-of-scope stream 2.2.x already has its own CVE Jira, TC-8020 |

### Note on task count

For a Cargo source dependency the classification table normally calls for 2 tasks per stream (bump plus downstream propagation). The reconciled TC-8022 is the existing preemptive bump task for 2.1.x. The engineer should confirm whether TC-8020's Case A run also created a downstream-propagation preemptive task for rhtpa-2.1. Only TC-8022 came back from the JQL, so this run does not create a second one. The engineer can decide whether a downstream-propagation task is still missing.

## Post-triage actions (proposed, need confirmation)

1. Add the label `ai-cve-triaged` to TC-8021.
2. Post a summary comment on TC-8021 that includes:
   - the version impact table (2.1.0 and 2.1.1 presumed affected, lock-file confirmation pending)
   - "Affects Versions: no correction needed"
   - "Outcome: remediation tracked by existing task TC-8022, reconciled from preemptive (created via TC-8020 cross-stream analysis): Depend link added and `security-preemptive` label removed"
   - release Jira references, if Step 7.5 created or found any
   - an @mention of the TC-8021 reporter (ADF mention node)
   - the Comment Footnote for skill `triage-security`, per `shared/comment-footnote.md`
3. Assign TC-8021 to the current user and transition it to Assigned (Step 0.8).

None of these Jira mutations were executed. This eval forbids external calls, so all actions are recorded here as proposals.
