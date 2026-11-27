# Triage Outcome: TC-8001 (CVE-2026-31812, quinn-proto) — re-run

## Result: no new mutations executed

| Mutation category | Count this run |
|-------------------|----------------|
| Issues created (remediation tasks) | 0 |
| Issue links created | 0 |
| Comments posted (digest, correction, summary, task list) | 0 |
| Labels added/removed | 0 |
| Field edits (Affects Versions, assignee, VEX) | 0 |
| Status transitions | 0 |

## Why the second run is a no-op

Each triage-security step checks for existing state before it writes. The prior
run already reached the terminal triaged state:

1. **Triaged marker.** `ai-cve-triaged` is already present. This label exists to
   "prevent re-triaging the same issue". Discovery mode would never list TC-8001 as
   untriaged, and it is not "triaged but still New".
2. **Status.** The issue is In Progress. The Step 0.8 transition to Assigned and the
   post-creation transition to In Progress are both conditional ("if not already" /
   "already in Assigned or later status: skip silently"). The status-aware gate
   warned that the issue may be actively worked on, and the run continued only as
   a verification re-triage.
3. **Remediation already exists.** The 2.2.x stream is a scoped Cargo (source
   dependency) stream, which needs exactly 2 tasks. Both exist and are Depend-linked:
   TC-8100 (upstream backport, In Progress) and TC-8101 (downstream propagation,
   Open, blocked by TC-8100). Step 7.5.3 dedup and Step 4.3 link checks find
   existing coverage for upstream component `quinn-proto`. Case B therefore skips
   task creation, which also skips every follow-on action: digest comments, Depend
   and Blocks links, and the "Remediation tasks created" comment.
4. **Digest.** A `[sdlc-workflow] Description digest` comment already exists.
   Digests are posted exactly once, when a task is created. No task is created, so
   no digest is posted.
5. **Summary.** A post-triage summary comment (with footnote, v0.11.1) already
   exists. Posting a second one would duplicate the audit trail.
6. **Assignee.** Already set (engineer-a). Reassignment only happens if a different
   engineer runs the skill and confirms it.

The re-run is idempotent: running the workflow again on an issue in its triaged
end state produces the same Jira state.

## Caveat: re-verification findings need engineer review

The skill requires re-verifying versions against lock files (Rules 3–5) instead of
trusting earlier conclusions. That check found issues the prior run missed. Because
every mutation needs explicit confirmation (Rule 11) and this eval forbids Jira
calls, they are **proposals, not executed mutations**:

- **D1:** RHTPA 2.2.2 is a backend retag of 2.2.1 (`v0.4.8`, quinn-proto 0.11.12),
  so it is **affected** and missing from Affects Versions. Proposed change:
  `[RHTPA 2.2.0, RHTPA 2.2.1] → [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]`, with a
  correction comment. The prior summary's claim that "2.2.2 and later ship 0.11.14"
  is incorrect. Only 2.2.3 and later do.
- **D2:** The 2.1.x stream (2.1.0 and 2.1.1, quinn-proto 0.11.9) is also affected.
  No Case A cross-stream impact comment or preemptive 2.1.x task is recorded. The
  engineer should check for a sibling 2.1.x CVE Jira (Step 4 JQL).
- **D3:** The digest comment is on the Vulnerability rather than on the remediation
  tasks. Check that TC-8100 and TC-8101 each have their own digest.

If the engineer declines these proposals, the run ends with zero mutations. If the
engineer confirms D1 and/or D2, those changes are new corrections of prior-run
errors. They are not repeats of artifacts that already exist, and no existing
artifact (tasks, links, label, digest, summary, status) would be recreated.
