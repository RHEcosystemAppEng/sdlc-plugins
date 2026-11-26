# Triage Outcome: TC-8001 (Re-run)

## Result: No new Jira mutations executed

| Mutation type | Count this run |
|---------------|----------------|
| Remediation Tasks created | 0 |
| Issue links created | 0 |
| Comments posted (digest, summary, correction, cross-stream) | 0 |
| Labels added or removed | 0 |
| Status transitions | 0 |
| Field edits (assignee, Affects Versions, VEX) | 0 |

## Why the second run is a no-op

1. **The triage marker is already present.** `ai-cve-triaged` is on the issue, so re-adding it would change nothing. The label exists to stop the same issue from being triaged again.
2. **The workflow state is already advanced.** Status is `In Progress`, later than Assigned, so Step 0.8 skips the transition silently. The status-aware gate warns that the issue may be in active work and runs this pass as verification only. The issue is already assigned, so no assignment change is needed when the re-runner is the current assignee.
3. **Remediation already exists for the scoped stream.** The issue is scoped to `[rhtpa-2.2]`, which maps to stream 2.2.x. Cargo is a source-dependency ecosystem, so Case B needs exactly 2 tasks for that stream. Both exist and are linked via Depend: TC-8100 (upstream backport, In Progress) and TC-8101 (downstream propagation, Open), plus the Blocks relationship between them. Creating them again would duplicate active work. The skill already checks `issuelinks` before creating a link, so every existing link is skipped.
4. **The description digest is tied to task creation.** A digest is posted only right after a remediation task is created. No task is created, so no digest is posted. The existing `sha256-md:` digest comment stays the single integrity anchor for `/implement-task`.
5. **The post-triage summary already exists.** A footnoted summary from the prior run documents version impact, the Affects Versions correction, the label, the tasks, and the transition. Posting it again would add duplicate audit noise.
6. **Several steps have nothing to act on.** Embargo (1.7) is skipped because no policy URL is configured. Cross-CVE overlap (4.3) and concurrent triage (7) are skipped because the Upstream Affected Component field is not configured. No sibling, preemptive, already-fixed, or release-Jira evidence calls for a new link or closure.

## Items surfaced for engineer confirmation (not executed)

Re-triage still re-checks the evidence (Important Rule 3: do not trust earlier Affects Versions without checking the lock files). It found one real discrepancy. Under the confirmation guardrail, that can only be a proposal:

- **Affects Versions are missing RHTPA 2.2.2.** RHTPA 2.2.2 is a backend retag of 2.2.1 (`v0.4.8`, quinn-proto 0.11.12 < 0.11.14), so it is affected. The prior summary wrongly lists it as not affected.
  Proposed: `[RHTPA 2.2.0, RHTPA 2.2.1]` → `[RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]`. If approved, the engineer would also get a footnoted Step 3 correction comment. No new remediation task is needed, because TC-8100 and TC-8101 already cover release/0.4.z.
- **The 2.1.x stream is also affected** (2.1.0 and 2.1.1 ship quinn-proto 0.11.9). Step 4 should confirm whether a 2.1.x sibling CVE Jira exists. If none exists, Case A would propose a cross-stream comment and preemptive tasks, gated on confirmation.
- **Matrix staleness.** The security matrix is 151 days old, so a refresh is recommended before relying on the impact table.
- **Minor details.** The TC-8100/TC-8101 Blocks direction looks reversed relative to the upstream → downstream convention. The due date (2026-07-15) has passed. The "backport" task may in practice be a dependency bump, because v0.4.11 already ships 0.11.14.

## Summary

The re-run detected every artifact from the prior triage: the label, the status, two Depend-linked remediation tasks, the Blocks link, the digest comment, and the summary comment. It skipped each one, so no duplicate Jira writes happened. Its only new output is a proposed Affects Versions correction for RHTPA 2.2.2, backed by the evidence and waiting on explicit engineer approval.
