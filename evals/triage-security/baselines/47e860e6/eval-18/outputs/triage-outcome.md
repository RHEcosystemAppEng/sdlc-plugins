# Triage Outcome: TC-8001 (CVE-2026-31812, quinn-proto, [rhtpa-2.2]) re-run

## Outcome

**No new Jira mutations were executed.** The re-run is idempotent: TC-8001 was already
triaged on 2026-07-01, and every artifact a triage would create already exists.

## Why the second run creates nothing

1. **Triaged marker is present.** The `ai-cve-triaged` label is already on the issue. The
   label exists to "prevent re-triaging the same issue", and the re-run does not add it again.
2. **Status is already past Assigned.** The issue is In Progress, so Step 0.8 skips the
   transition. Status-aware handling only issues a warning ("already in In Progress, may be
   actively worked on"). The engineer chose to proceed for verification.
3. **Remediation for the scoped stream already exists.** The issue is scoped to 2.2.x and
   the library is Cargo, a source dependency, which needs 2 tasks per stream. Both exist and
   are Depend-linked:
   - TC-8100: upstream backport to >= 0.11.14 on release/0.4.z (In Progress)
   - TC-8101: downstream propagation to rhtpa-server (Open), Blocks TC-8100

   The task count, link types (Depend, Blocks) and labels (ai-generated-jira, Security,
   CVE-2026-31812) match the pre-creation checklist. Step 8 Case B creates no new tasks.
4. **Links are checked before creation.** Matching Depend and Blocks links are found in
   `issuelinks`, so link creation is skipped.
5. **Digest is posted exactly once.** A `[sdlc-workflow] Description digest` comment already
   exists. No task is created, so no digest comment is posted.
6. **The summary is already recorded.** The post-triage summary comment, with its footnote,
   exists. Posting it again would duplicate the audit trail.
7. **Conditional steps don't apply.** The Embargo policy URL and Upstream Affected Component
   field are not configured, so Steps 1.7, 4.3, 7 and 7.5.3 are skipped. No same-stream duplicate
   or resolved-sibling closure path is triggered.

## Mutation ledger for this run

| Mutation | Executed? |
|---|---|
| Assign / transition | No (already In Progress; assignment is a no-op if the runner is engineer-a) |
| Affects Versions edit | No (only proposed for confirmation, see below) |
| Comments (correction, cross-stream, digest, summary) | No |
| Issue links (Depend / Blocks / Related) | No |
| Remediation Tasks | No |
| Labels | No |
| Release Epic / Task | No |

## Items for engineer confirmation (not executed)

The re-run produces no duplicate mutations, but checking the version impact against
the evidence again turned up two things for the engineer to decide. Under the skill's guardrails these
are recommendations and are never written automatically:

1. **RHTPA 2.2.2 appears affected.** The matrix marks 2.2.2 as a backend retag of 2.2.1
   (`v0.4.8`, quinn-proto 0.11.12 < 0.11.14). Retags carry forward the original result. The
   proposal is `[RHTPA 2.2.0, RHTPA 2.2.1] -> [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]`. This
   contradicts the prior summary's "2.2.2 and later … not affected". This needs explicit approval. If
   approved, it would also need a correction comment with the footnote. The existing
   TC-8100/TC-8101 already target the 0.4.z branch fix, so no new tasks are needed either way.
2. **Cross-stream impact on 2.1.x (Case A).** 2.1.0 and 2.1.1 ship quinn-proto 0.11.9. Confirming
   whether a 2.1.x sibling CVE Jira, Related link, cross-stream comment or preemptive task exists
   needs a Jira JQL lookup, which this eval does not allow. Verify this before any Case A action.

If the engineer declines both, the run finishes with zero changes to TC-8001.
