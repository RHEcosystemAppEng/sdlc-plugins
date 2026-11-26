# Idempotency Check: TC-8001 (re-run)

Before proposing any mutation, every Jira write the skill would make on a first run was
checked against the issue state captured in Step 1 (labels, status, `issuelinks`,
comment history). Wherever the prior run's artifact already exists, the write is
skipped. This follows the same pattern the skill uses for links ("Related/Depend link to
X already exists — skipping"). It also follows the Fullsend rule that existing
markers/artifacts mean "the action is omitted on retry".

## Pre-existing artifacts detected

| # | Artifact | Evidence on TC-8001 | First-run write it corresponds to | Re-run decision |
|---|---|---|---|---|
| 1 | `ai-cve-triaged` label | Labels: `CVE-2026-31812, pscomponent:org/rhtpa-server, ai-cve-triaged` | Post-Triage Summary §1, "Add the `ai-cve-triaged` label" | **SKIP**: label already present. Adding it again would be a no-op label edit, so no `edit_issue` call. |
| 2 | Status In Progress | Status: `In Progress` | Step 0.8 transition New -> Assigned, and the later move to In Progress | **SKIP**: the issue is already in a status later than Assigned. Step 0.8 says "skip the transition silently". Status-aware handling instead warns that the issue is already In Progress and asks the engineer to proceed or skip. No `transition_issue` call. |
| 3 | Remediation Task TC-8100 (upstream backport) | Depend link -> TC-8100, "Backport quinn-proto fix to >= 0.11.14 on release/0.4.z [rhtpa-2.2]", labels `ai-generated-jira, Security, CVE-2026-31812`, In Progress | Step 8 Case B task 1 for stream 2.2.x (Cargo, so upstream backport) | **SKIP**: remediation for (CVE-2026-31812, 2.2.x) already exists. No `create_issue`. |
| 4 | Remediation Task TC-8101 (downstream propagation) | Depend link -> TC-8101, "Propagate quinn-proto bump to rhtpa-server release branch [rhtpa-2.2]", same labels, Open | Step 8 Case B task 2 for stream 2.2.x | **SKIP**: already exists. No `create_issue`. |
| 5 | Depend links TC-8001 -> TC-8100 / TC-8101 | `issuelinks` with `type.name = "Depend"` matching both keys | Case B "Link each Task to the Vulnerability issue" | **SKIP**: a matching Depend link exists for each key ("Depend link to TC-8100 already exists — skipping", and the same for TC-8101). No `create_link`. |
| 6 | Blocks link TC-8100 -> TC-8101 | TC-8101 "Blocks: TC-8100" (downstream blocked by upstream) | Case B upstream -> downstream ordering link | **SKIP**: already present. No `create_link`. |
| 7 | Description digest comment | `[sdlc-workflow] Description digest: sha256-md:a1b2c3d4...a1b2`, posted by sdlc-workflow/triage-security, 2026-07-01T10:00:00Z | Digest comment posted after creating each remediation task (`shared/description-digest-protocol.md`) | **SKIP**: the digest is posted exactly once, at task creation. No task is created on this run, so no digest is generated, and the existing digest comment is not reposted. |
| 8 | Post-triage summary comment | "Triage complete for CVE-2026-31812 (quinn-proto)…" with Comment Footnote (triage-security v0.11.1), 2026-07-01T10:01:00Z | Post-Triage Summary §2 | **SKIP**: a summary comment from triage-security already exists. A duplicate summary is not posted. |
| 9 | Affects Versions correction | `versions` = RHTPA 2.2.0, RHTPA 2.2.1; the prior summary records "Affects Versions corrected to RHTPA 2.2.0, RHTPA 2.2.1" | Step 3.2 edit and correction comment | **No repeat of the prior correction.** The values the prior run set are still present, so the correction and its comment are not reapplied. Note: re-verification against the matrix flags 2.2.2 as possibly missing (see `triage-outcome.md`). That is a new finding for the engineer to confirm, not a repeat of the prior write. |
| 10 | Remote links (GHSA, CVE record, upstream PR) | Present on the issue | Read-only (the skill never creates remote links) | N/A, nothing to write. |

## Steps that produce no write on this issue

| Step | Reason no mutation is attempted |
|---|---|
| 0.8 Assignment | Already assigned to engineer-a@example.com. Interactive Step 0.8 re-asserts the current user as assignee. If the current user is engineer-a, this is a no-op. If not, it would be a reassignment of an In Progress issue owned by someone else. It is presented for confirmation and never done silently. |
| 1.7 Embargo | No Embargo policy URL configured, so skipped. |
| 4.1 / 4.2 Siblings | No Related links on the issue. The sibling JQL was not executed in this eval. Any companion 2.1.x issue found in a real run would be checked against `issuelinks` before linking. |
| 4.3 Cross-CVE overlap | The Upstream Affected Component field is not configured, so skipped. |
| 4.4 Preemptive reconciliation | Remediation for 2.2.x already exists through Depend links (TC-8100/TC-8101), so no preemptive task would be reconciled into a second remediation. |
| 7 Concurrent triage | The Upstream Affected Component field is not configured, so skipped. |
| 7.5 Release Jira | The prior summary records no release Epic/Task. In a real run, find-or-create looks for existing `RHTPA <version> CVE triage` items before creating any. That is not evaluable here, and nothing is created without individual confirmation. |
| 7.5.3 / 8 Dedup | The existing Depend-linked tasks cover quinn-proto for 2.2.x, so task creation is skipped for that stream. |

## Mutation tally for this re-run

| Mutation type | Count |
|---|---|
| Tasks created | 0 |
| Labels added | 0 |
| Status transitions | 0 |
| Links created | 0 |
| Digest comments | 0 |
| Summary comments | 0 |
| Field edits | 0 executed (1 candidate Affects Versions addition flagged for engineer review, see `triage-outcome.md`) |
