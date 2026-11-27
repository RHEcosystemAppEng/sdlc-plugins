# Triage Outcome: TC-8003 (CVE-2026-31812, quinn-proto)

## Decision

**Close TC-8003 as Duplicate of TC-7999.** No remediation tasks are created.

## Rationale

1. **Same CVE, same stream.** TC-8003 and TC-7999 both carry the label `CVE-2026-31812` and the component `pscomponent:org/rhtpa-server`, and both use the stream suffix `[rhtpa-2.2]` (stream 2.2.x). Under Step 4 these are same-stream siblings, not cross-stream companion trackers.
2. **The sibling is active.** TC-7999 is **In Progress**. Step 4.1 says that when a same-stream sibling is open or in progress, the current issue should close as Duplicate.
3. **Version impact confirms the overlap.** Lock file data at pinned commits shows quinn-proto < 0.11.14 in RHTPA 2.2.0 (0.11.9), 2.2.1 (0.11.12), and 2.2.2 (retag of 2.2.1). RHTPA 2.2.3 and 2.2.4 ship the fixed 0.11.14. TC-8003 claims only RHTPA 2.2.0, which TC-7999 (2.2.0, 2.2.1) already covers. TC-8003 adds no tracking scope.
4. **TC-7999 is the canonical tracker.** It is older and already being worked on. Creating remediation tasks from TC-8003 would duplicate TC-7999's remediation work, so Steps 5–8 (lifecycle, already-fixed, concurrent triage, release Jira, remediation) do not run for TC-8003.

## Proposed Jira Mutations on TC-8003 (interactive mode: each needs engineer confirmation; none executed in this eval)

| # | Operation | Detail |
|---|-----------|--------|
| 1 | Assign (Step 0.8) | Assign TC-8003 to the current user |
| 2 | Transition (Step 0.8) | New → Assigned |
| 3 | Comment (Step 4.1) | "Duplicate of TC-7999 — same CVE tracked for the same stream 2.2.x. Version impact analysis confirms overlap." Includes the version evidence and the Comment Footnote (`sdlc-workflow/triage-security v0.14.0`) |
| 4 | Link (recommended) | TC-8003 "Duplicate" link to TC-7999, created only if not already present |
| 5 | Transition (Step 4.1) | → Closed, resolution **Duplicate** |
| 6 | Label (Post-Triage) | Add `ai-cve-triaged` |
| 7 | Summary comment (Post-Triage) | Version impact table, outcome (closed as Duplicate of TC-7999), no remediation tasks, no release Jira, and an @mention of the TC-8003 reporter. The reporter account ID was not in the input, so it must be read from the issue at runtime. Includes the Comment Footnote |

Not applied:
- **Affects Versions correction on TC-8003** (`[RHTPA 2.2.0]` → `[RHTPA 2.2.0, 2.2.1, 2.2.2]`): not needed, because the issue closes as a duplicate.
- **VEX Justification:** not set. VEX applies only to "Not a Bug" (not affected) closures, and 2.2.x versions *are* affected.

## Follow-ups for the canonical issue TC-7999 (advisory; outside this triage's scope)

- **Add RHTPA 2.2.2 to Affects Versions.** It is a backend retag of 2.2.1 (`v0.4.8`, quinn-proto 0.11.12), so it is affected. TC-7999 currently lists only 2.2.0 and 2.2.1.
- **Cross-stream impact on 2.1.x.** RHTPA 2.1.0 and 2.1.1 ship quinn-proto 0.11.9 and are affected. The sibling search found no 2.1.x CVE Jira, so TC-7999's triage should apply Case A: a cross-stream comment plus a preemptive (`security-preemptive`, "Related") remediation task pair for 2.1.x.
- **Remediation path for 2.2.x.** The latest 2.2.x release (2.2.4, `v0.4.12`) already ships 0.11.14. The 2.2.x fix appears to be available upstream on `release/0.4.z` (branch HEAD was not verified), so remediation for older 2.2.x releases is effectively upgrade guidance to 2.2.3 or later.

## Caveats and Data Gaps

- **Stale matrix:** security-matrix.md Last-Updated is 2026-06-28, 152 days old (threshold 14). I proceeded without refreshing. This does not affect the duplicate decision.
- **No external enrichment:** I did not query MITRE or OSV (external calls were prohibited). The fix threshold (0.11.14) comes only from the Jira description.
- **Development stream:** not evaluated. Detecting it needs unreleased Jira versions, which were not available.
- **Due date** 2026-07-15 has passed. TC-7999's owner should be told the SLA is overdue.
- No Jira, git, or WebFetch calls were made. All values come from the provided input files and the given JQL result.
