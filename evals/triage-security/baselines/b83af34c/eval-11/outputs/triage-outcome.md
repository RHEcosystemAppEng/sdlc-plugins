# Triage Outcome for TC-8021 (CVE-2026-55123)

## Summary

TC-8021 is a Vulnerability issue for CVE-2026-55123 (tokio use-after-free,
versions before 1.42.0) scoped to stream **rhtpa-2.1** (2.1.x).

## Preemptive Task Reconciliation

Step 4.4 found an existing preemptive remediation task **TC-8022** that was
created during a prior triage of TC-8020 (the companion CVE Jira for stream
rhtpa-2.2). TC-8022 was created as a proactive remediation task for the 2.1.x
stream via Case A cross-stream impact analysis.

### How the existing preemptive task was reconciled

1. **JQL Search**: Step 4.4 searched for preemptive tasks using:
   ```
   project = TC AND issuetype = Task AND labels = 'security-preemptive' AND labels = 'CVE-2026-55123'
   ```
   This returned TC-8022.

2. **Stream Matching**: TC-8022's summary ("Remediate CVE-2026-55123: bump tokio
   to 1.42.0 (rhtpa-2.1)") contains `(rhtpa-2.1)`, which matches the current
   issue's stream suffix `[rhtpa-2.1]`. This confirms TC-8022 was created for
   the same stream.

3. **Linkage**: TC-8021 was linked to TC-8022 with link type "Depend" -- the
   standard remediation linkage used when triage-security creates remediation
   tasks. This replaces the previous "Related" link (from TC-8020) as the
   primary CVE-to-task relationship. The "Related" link to TC-8020 remains
   intact for cross-stream traceability.

4. **Label Removal**: The `security-preemptive` label was removed from TC-8022.
   This label distinguished proactive tasks (created before a stream-specific
   CVE Jira existed) from standard remediation tasks. Now that TC-8021 exists
   as the proper CVE Jira for this stream, TC-8022 is a standard remediation
   task.

5. **Step 8 Skip**: Because Step 4.4 reconciliation successfully linked an
   existing remediation task (TC-8022) to the new CVE Jira (TC-8021), Step 8
   skips remediation task creation for the 2.1.x stream. No new tasks are
   created -- TC-8022 already covers the needed remediation (bump tokio to
   1.42.0 in the rhtpa-backend repository on the release/0.3.z branch).

## Final State

| Item | Value |
|------|-------|
| CVE Jira | TC-8021 (stream rhtpa-2.1, status: New -> Assigned) |
| Remediation Task | TC-8022 (reconciled from preemptive to standard) |
| Task Link | TC-8021 -> TC-8022 (Depend) |
| Cross-stream Link | TC-8022 -> TC-8020 (Related, retained from prior triage) |
| New tasks created | 0 (Step 8 skipped -- reconciliation covered this stream) |
| Labels removed | security-preemptive (from TC-8022) |

## Rationale

The preemptive task reconciliation mechanism (Step 4.4) exists to prevent
duplicate remediation work. When PSIRT creates per-stream CVE Jiras
sequentially, the first triage (TC-8020 for rhtpa-2.2) proactively creates
remediation tasks for other affected streams (Case A). When the second CVE
Jira arrives (TC-8021 for rhtpa-2.1), Step 4.4 detects the existing
preemptive task, links it properly, and converts it to a standard remediation
task. This avoids creating a second, duplicate remediation task for the same
CVE and stream.
