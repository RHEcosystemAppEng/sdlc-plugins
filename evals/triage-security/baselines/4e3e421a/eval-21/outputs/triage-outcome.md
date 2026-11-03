# Triage Outcome: TC-8020 (CVE-2026-31812, quinn-proto, [rhtpa-2.2])

## Decision

**Affected. Remediation is required, but task creation is paused at the Step 7
concurrent-triage gate pending the engineer's choice.**

No Jira mutations were executed. Every change below is a proposal that needs
explicit engineer confirmation.

## Basis

- quinn-proto < 0.11.14 is vulnerable (CVSS 7.5, DoS).
- **2.2.x stream (in scope):** 2.2.0 (0.11.9), 2.2.1 (0.11.12), and 2.2.2 (retag of
  2.2.1) are **affected**. 2.2.3 and 2.2.4 ship 0.11.14 and are **not affected**.
- **2.1.x stream (out of scope):** 2.1.0 and 2.1.1 ship 0.11.9 and are
  **affected**. This is cross-stream impact.
- Caveat: the security matrix is 128 days old (Step 0.3 staleness warning), and
  external CVE enrichment (Step 1.5) and the lifecycle check (Step 5) were not
  performed.

## Proposed actions (pending confirmation)

1. **Step 0.8:** assign TC-8020 to the current user and transition it New to Assigned.
2. **Step 3:** correct Affects Versions from `[RHTPA 2.0.0]` to
   `[RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]`, and add a correction comment with the
   Comment Footnote. No ProdSec @mention, because none is configured.
3. **Step 4:** no siblings or cross-CVE coverage were supplied. The 2.1.x impact is
   handled in Case A.
4. **Step 7: concurrent triage detected.** TC-8019 (In Progress,
   engineer-b@example.com) is on the same upstream component, quinn-proto. The
   engineer must choose one of:
   - **Wait** (recommended): stop now and re-run once TC-8019 completes, so that
     Step 4.3 can detect whether its remediation covers >= 0.11.14.
   - **Skip:** no remediation tasks. Post an explanatory comment on TC-8020.
   - **Proceed:** add the `concurrent-triage-overlap` label to TC-8020 and continue.
5. **If the engineer chooses Proceed:**
   - **Step 7.5:** find or create the release Epic and Task (`RHTPA 2.2.x Release
     Tasks` / `RHTPA 2.2.x CVE triage`, with the version to be confirmed), then run
     the cross-CVE dedup check against TC-8019's tasks if any exist.
   - **Case A (scoped issue; 2.1.x also affected):** post a cross-stream impact
     comment. If 2.1.x has no CVE-2026-31812 Jira, create preemptive 2.1.x tasks
     (`security-preemptive` label, linked to TC-8020 as Related).
   - **Case B, 2.2.x (Cargo, so 2 tasks).** Step 2.5 shows release/0.4.z already
     ships 0.11.14 (released in 2.2.3 / v0.4.11 and later):
     1. Dependency bump / upstream reference task. The fix already exists upstream
        at v0.4.11+, so it can be referenced directly.
     2. Downstream propagation task in rhtpa-release.0.4.z, blocked by task 1.

     Both tasks are linked to TC-8020 (Depend), Block the release Task, and get a
     description-digest comment. In practice the remediation for supported 2.2.x
     customers is upgrading to 2.2.3 or later.
   - **Post-triage:** add the `ai-cve-triaged` label and a summary comment with the
     version impact table, the Affects Versions correction, task links, release
     Jira refs, an @mention of the reporter, and the Comment Footnote.
6. **If the engineer chooses Wait or Skip:** no remediation tasks are created
   in this run. Steps 0.8 and 3 can still be applied if confirmed.

## Not applicable

- Case C (Close as Not a Bug / VEX) does not apply, because supported 2.2.x
  versions are affected.
