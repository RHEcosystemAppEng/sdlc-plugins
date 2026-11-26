# Triage Outcome: TC-8001 (re-run)

## Result

**No new mutations.** The second run makes no Jira writes. The skill re-reads the issue
(Step 1), re-derives the expected triage end state (Steps 2–8), and finds that every
artifact the first run would produce already exists. Each corresponding write is
skipped (details in `idempotency-check.md`).

## Why the second run produces no new mutations

1. **Label is already set.** `ai-cve-triaged` is present. The Post-Triage label step is
   satisfied, and this label is also what discovery mode uses to exclude triaged issues
   (`labels NOT IN (ai-cve-triaged)`). TC-8001 is reached only because its key was given
   explicitly.
2. **Status is already past triage.** The issue is In Progress, which is later than
   Assigned. Step 0.8 skips the transition silently. Status-aware handling only warns
   that the issue may be in active work and asks whether to proceed. No transition is
   proposed.
3. **Remediation already exists for the scoped stream.** The issue is scoped to 2.2.x
   (`[rhtpa-2.2]`) and the ecosystem is Cargo, so the expected Case B output is two
   tasks: an upstream backport plus a downstream propagation blocked by it. Both exist
   (TC-8100, TC-8101). Both carry the expected labels (`ai-generated-jira, Security,
   CVE-2026-31812`) and are linked via Depend, with TC-8101 blocked by TC-8100. Step 8
   treats this stream as already remediated (the same effect as 7.5.3 dedup and the 4.4
   "record that remediation exists"), so no `create_issue` is made.
4. **Links already exist.** Each candidate link (Depend x2, Blocks) is checked against
   `issuelinks` first, using the skill's existing-link check, and is skipped.
5. **Comments are not duplicated.** The description digest is posted once, as part of
   creating a task. No task is created, so no digest is posted, and the existing digest
   comment stays the only one. A triage-security post-triage summary (with footnote,
   v0.11.1) already exists, so no second summary is posted.
6. **The Affects Versions correction from the first run is already applied.**
   `versions` = RHTPA 2.2.0, RHTPA 2.2.1, matching what the prior summary says it set.
   That correction and its comment are not repeated.

Mutations executed: **0 tasks, 0 labels, 0 transitions, 0 links, 0 comments, 0 field
edits.**

## Findings from re-verification (advisory, not executed)

Re-running Step 2 against the mock matrix turned up issues that the prior run's output
does not account for. Under the guardrail "every Jira mutation requires confirmation",
they go to the engineer as proposals. None is applied automatically, so they do not
change the "no new mutations" outcome of this run:

1. **RHTPA 2.2.2 appears to be affected.** The matrix row for 2.2.2 says "backend retag
   of 2.2.1" with backend tag `v0.4.8`, and `v0.4.8` ships quinn-proto **0.11.12**,
   which is below 0.11.14. Under Important Rule 5 (retags carry forward the original
   version's result), 2.2.2 is affected the same way 2.2.1 is. The prior summary says
   "2.2.2 and later ship 0.11.14 (not affected)". That holds only from 2.2.3 (`v0.4.11`)
   onward.
   - Candidate Step 3.2 correction: `Current: [RHTPA 2.2.0, RHTPA 2.2.1] -> Proposed:
     [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]`. It needs engineer confirmation and a
     correction comment with the Comment Footnote. The engineer should also check that
     a Jira version "RHTPA 2.2.2" exists (dynamic version discovery, Step 3.1).
   - This does not change the remediation: the 2.2.x fix tracked by TC-8100/TC-8101
     covers the stream.
2. **2.1.x stream is affected (cross-stream, Case A).** 2.1.0 and 2.1.1 (`v0.3.8`,
   `v0.3.12`) ship quinn-proto 0.11.9. The prior summary records no cross-stream
   comment or preemptive tasks. A real run would search for a 2.1.x sibling CVE issue
   (Step 4 JQL). If one exists, it only needs a Related link, after an existing-link
   check. If none exists, Case A proposes a cross-stream comment plus preemptive 2.1.x
   tasks. This could not be evaluated here because no Jira search was run.
3. **Upstream fix may already be on release/0.4.z.** `v0.4.11` and `v0.4.12` already
   ship quinn-proto 0.11.14, so Step 2.5 would likely find the fix on the upstream
   branch. In that case TC-8100 is closer to the "dependency bump" variant than to a
   backport. This is informational only, and existing tasks are not edited.
4. **Matrix staleness.** The matrix `Last-Updated` is 2026-06-28, older than 14 days.
   Step 0.3 would offer Refresh / Proceed / Stop before relying on it.

## Final recommendation to the engineer

> TC-8001 was already triaged on 2026-07-01 by triage-security v0.11.1. All triage
> artifacts are present: `ai-cve-triaged` label, In Progress status, remediation tasks
> TC-8100 / TC-8101 (Depend), the description digest comment, and the post-triage
> summary. No duplicate tasks, labels, transitions, links, or comments will be created.
> Optional follow-up for your decision: add RHTPA 2.2.2 to Affects Versions (retag of
> 2.2.1, which ships quinn-proto 0.11.12), and confirm that the 2.1.x stream is tracked
> by a companion CVE issue.
